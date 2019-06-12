# Transforms movie data it into a collaborator's graph. Network metrics are
# calculated for each movie, and are recorded for further analysis.

# Standard libs.
import os
import pickle
import logging
from inspect import getmembers, isfunction
from datetime import datetime

# 3rd party libs.
from tqdm import tqdm
from pymongo import MongoClient

# This package.
from metrics import ego, pair
from bipartite import prune_components, update_components
import aggregations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__.split("/")[-1])

db = MongoClient().imdbws

# XXX: When there are more experiments, define them on an external .py source
# and import here. The ID of the experiment to be used can be passed through a
# command line argument.
EXP = {'id': 0,
       'team': ['producer', 'director', 'writer'],
       'year_start': 1985,
       'year_end': 2012,
       'filter': {'is_subject': True}}


IS_VALID_FUNCTION = lambda x: x[0][0] != '_' and isfunction(x[1])


def contract_edges(G, nodes):
    """
    Contracts edges of nodes in the graph. Returns the result in a new graph.
    """
    logger.debug(f"Contracting nodes.")

    G = G.copy()
    G.add_node('contracted')
    G.node['contracted']['original'] = nodes

    movies = set()
    [movies.update(G.node[n]['movies']) for n in nodes]
    G.node['contracted']['movies'] = list(movies)

    edges = G.edges(nodes, data=True)
    for e in [e for e in edges if not (e[0] in nodes and e[1] in nodes)]:
        oute = e[0] if e[1] in nodes else e[1]
        if not G.has_edge('contracted', oute):
            G.add_edge('contracted', oute, weight=0)
        G['contracted'][oute]['weight'] += e[2]['weight']

    G.remove_edges_from(list(edges) + list(nodes))
    return G


def calculate_aggregations(data):
    """
    Receives a dictionary where keys are measurement names and values are lists
    of measurements. Return a dictionary where keys are aggregations from the
    values from the input dictionary.
    """
    results = {}
    for metric_name, metric in data.items():
        metric = list(filter(lambda x: x is not None, metric))
        aggs = [o for o in getmembers(aggregations) if IS_VALID_FUNCTION(o)]
        for agg_name, agg_func in aggs:
            result = agg_func(metric) if metric else None
            results['%s_%s' % (metric_name, agg_name)] = result
    return results


def calc_ego_metrics(H, team, release, base_qry):
    """
    Given a graph and a team, calculates all ego metrics for each team member.
    Returns a dictionary where keys are ego metric names, and values are the
    computed values from each team member.
    """
    results = {}
    metrics = [o for o in getmembers(ego) if IS_VALID_FUNCTION(o)]

    for metric_name, metric_func in metrics:
        logger.debug(f"Calculating ego metric {metric_name}")
        values = []
        for member in team:
            values.append(metric_func(H, member, release, base_qry.copy()))
        results[metric_name] = values

    return results


def calc_pair_metrics(H, team):
    """
    Given a graph and a team, calculates all pair-wise metrics for possible
    team pairs. Returns a dictionary where keys are the pair metric names, and
    values are the computed values from each pair.
    """
    results = {}
    metrics = [o for o in getmembers(pair) if IS_VALID_FUNCTION(o)]

    for metric_name, metric_func in metrics:
        logger.debug(f"Calculating pair metric {metric_name}")
        results[metric_name] = metric_func(H, team)

    return results


def calc_team_metrics(H, team, release, base_qry):
    """
    Given a graph and a team, calculates all team-wise metrics Returns a
    dictionary where keys are the team metric names, and values are the
    computed metric values.
    """
    _H = contract_edges(H, team)

    results = {}
    metrics = [o for o in getmembers(ego) if IS_VALID_FUNCTION(o)]
    for metric_name, metric_func in metrics:
        logger.debug(f"Calculating team metric {metric_name}")
        qry = base_qry.copy()
        results[metric_name] = metric_func(_H, 'contracted', release, qry)

    results['team_size'] = len(team)

    return results


def build_team(mov, specs):
    """
    Given a movie record and a list of valid roles, return a list of unique ids
    of team members that match any of the given roles.
    """
    team = set()
    for spec in specs:
        if(spec in ['writer', 'director'] and mov.get(spec + 's')):
            for agent in mov[spec + 's']:
                if agent not in team:
                    team.add(agent)

        matches = lambda p: p['job'] == spec or p['category'] == spec
        for agent in filter(matches, mov['principals']):
            if agent['nconst'] not in team:
                team.add(agent['nconst'])

    return tuple(team) if len(team) > 1 else None


def load_components_cache(year):
    """
    Load a list of components at a given year, along with all movies that were
    added to the giant component that year and their respective teams.
    """
    fname = f"cache/comp_{EXP['id']}_{year}.p"
    logger.info(f"Getting components cache (experiment {EXP['id']}, {year}).")
    if(os.path.isfile(fname)):
        return pickle.load(open(fname, 'rb'))
    return None


def save_components_cache(year, components, movies_to_process):
    """
    Saves a list of components at a given year, along with all movies that were
    added to the giant component that year and their respective teams.
    """
    logger.info(f"Saving components cache (experiment {EXP['id']}, {year}).")
    fname = f"cache/comp_{EXP['id']}_{year}.p"
    pickle.dump((components, movies_to_process), open(fname, 'wb'))


def describe_components(components):
    """Logs information about the current state of the components."""
    if components:
        huge_comp = len(components[0])
        all_comps = huge_comp + sum([len(c) for c in components[1:]])
        x = 100 * (float(huge_comp) / all_comps)
        logger.info(f"There are {len(components)} components.")
        logger.info(f"Huge component has {huge_comp} nodes, {x:.2f}% of all.")


def process_movies(components, year):
    cache = load_components_cache(year)
    date = datetime(year, 1, 1)
    if cache:
        components, movies_to_process = cache
    else:
        movies_to_process = []

        qry = dict(EXP['filter'], startYear={'$eq': year})
        cursor = db.titles.find(qry, no_cursor_timeout=True)
        movies = list(cursor.sort([('_id', 1)]).batch_size(0))

        components = prune_components(components, date)
        for mov in tqdm(movies):
            team = build_team(mov, EXP['team'])
            if team:
                giant = update_components(components, team, mov['_id'], date)
                if giant:
                    movies_to_process.append((mov['_id'], team))

        save_components_cache(year, components, movies_to_process)

    describe_components(components)

    if year < EXP['year_start']:
        return components

    for mov, team in tqdm(movies_to_process):
        target = db[f"exp_{EXP['id']}"]
        if(target.find_one({'_id': mov})):
            continue

        mov = db.titles.find_one({'_id': mov})
        H = components[0]

        logger.debug(f"Calculating ego for {mov['primaryTitle']}.")
        ego_metrics = calc_ego_metrics(H, team, year, EXP['filter'])
        logger.debug(f"Calculating pair metrics for {mov['primaryTitle']}.")
        pair_metrics = calc_pair_metrics(H, team)
        logger.debug(f"Calculating team metrics for {mov['primaryTitle']}.")
        team_metrics = calc_team_metrics(H, team, year, EXP['filter'])
        logger.debug(f"Aggregating metrics for {mov['primaryTitle']}.")
        ego_agg = calculate_aggregations(ego_metrics)
        pair_agg = calculate_aggregations(pair_metrics)

        exp = {'team_metrics': team_metrics,
               'ego_metrics': ego_agg,
               'pair_metrics': pair_agg,
               'title': mov['primaryTitle'],
               'year': year,
               'ypct': mov['ypct'],
               'ypct_votes': mov['ypct'],
               'ypct_rating': mov['ypct'],
               'top100': mov['top100']}

        target = db[f"exp_{EXP['id']}"]
        target.update_one({'_id': mov['_id']}, {'$set': exp}, upsert=True)

    return components


cache = load_components_cache(EXP['year_start'] - 1)
if cache:
    components, _ = cache
    year = EXP['year_start']
else:
    logger.info(f"Bootstrapping components for experiment {EXP['id']}.")
    logger.debug(f"Finding earliest movie in the dataset.")
    earliest = db.titles.find_one(EXP['filter'], sort=[('startYear', 1)])
    year = earliest['startYear']
    components = []

while(year <= EXP['year_end']):
    logger.info(f"Processing movies from {year}.")
    components = process_movies(components, year)
    year += 1
