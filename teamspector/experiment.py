import sys
import logging
from datetime import datetime

from tqdm import tqdm
from pymongo import MongoClient

from teamspector import network, metrics, cache, datasets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__.split("/")[-1])


get_db = lambda exp: getattr(MongoClient(), exp['dataset'])


def _get_initial_components(exp):
    """
    Returns the state of the social network as a list of components. The
    network is built according to the experiment's specification from the
    oldest works up to the year prior to the experiment start. Caching is used
    to avoid repeating these calculations.
    """
    c = cache.load_components(exp, exp['year_start'] - 1)
    if c:
        return c[0]

    db = get_db(exp)
    first = db.productions.find_one(exp['filter'], sort=[('startYear', 1)])
    year = first['startYear']
    components = []
    while(year < exp['year_start']):
        components, _ = _components_update(exp, components, year)
        year += 1
    return components


def _components_update(exp, components, year):
    """
    Receives an experiment specification, a year, and the components in the
    year prior. Updates the components with works produced in the given year.
    Return updated components and a list of new works produced in the year.
    """
    c = cache.load_components(exp, year)
    if c:
        return c

    logger.info(f"Cache not found, updating components with {year} works.")
    db = get_db(exp)
    date = datetime(year, 1, 1)
    works_from_year = []
    qry = dict(exp['filter'], startYear={'$eq': year})
    cursor = db.productions.find(qry, no_cursor_timeout=True)
    prods = list(cursor.sort([('_id', 1)]).batch_size(0))
    components = network.prune_components(components, date)
    for prd in tqdm(prods):
        t = network.filter_team(prd['team'], exp['team'])
        if t:
            giant = network.update_components(components, t, prd['_id'], date)
            if giant:
                works_from_year.append((prd['_id'], t))

    cache.save_components(exp, year, components, works_from_year)
    return components, works_from_year

    if components:
        huge_comp = len(components[0])
        all_comps = huge_comp + sum([len(c) for c in components[1:]])
        x = 100 * (float(huge_comp) / all_comps)
        logger.info(f"There are {len(components)} components.")
        logger.info(f"Huge component has {huge_comp} nodes ({x:.2f}%).")


def _processed(work, experiment):
    if not work:
        return False
    for metric in experiment.get('metrics', []):
        if not any([metric in k for k in work.keys()]):
            return False
    return True


def _process_productions(experiment):
    """
    Calculate experiment metrics for all works encompassed by an experiment.
    Calculations are batched by year of works release. That's because the
    social network is updated only once yearly. Its state in the current year
    is kept in `components`.
    """
    db = get_db(experiment)
    target = db[f"exp_{experiment['id']}"]
    components = _get_initial_components(experiment)
    year = experiment['year_start']
    while(year <= experiment['year_end']):
        logger.info(f"Processing works from {year}.")
        components, works = _components_update(experiment, components, year)
        for work_id, team in tqdm(works):
            if(_processed(target.find_one({'_id': work_id}), experiment)):
                continue
            prd = db.productions.find_one({'_id': work_id})
            H = components[0]
            logger.debug(f"Calculate ego for {prd['primaryTitle']}.")
            m_ego = metrics.calc_ego(H, team, year, experiment)
            logger.debug(f"Calculate pair metrics for {prd['primaryTitle']}.")
            m_pair = metrics.calc_pair(H, team, experiment)
            logger.debug(f"Calculate team metrics for {prd['primaryTitle']}.")
            m_team = metrics.calc_team(H, team, year, experiment)
            logger.debug(f"Aggregate metrics for {prd['primaryTitle']}.")

            data = {'title': prd['primaryTitle'],
                    'year': year,
                    'ypct': prd['ypct'],
                    'ypct_votes': prd['ypct'],
                    'ypct_rating': prd['ypct'],
                    'top100': prd['top100']}

            data.update(m_team)
            data.update(m_ego)
            data.update(m_pair)
            target.update_one({'_id': prd['_id']}, {'$set': data}, upsert=True)
        year += 1


def main():
    """
    Fetch experiment id and dataset code as arguments. Load the given
    experiment spec from `teamspector.datasets`. Get the state of the network
    prior to the start of the experiment. Calculate the experiment's metrics
    for all works it specifies.
    """
    dataset_code = sys.argv[1] if len(sys.argv) > 1 else None
    exp_id = int(sys.argv[2]) if len(sys.argv) > 2 else None

    if dataset_code is None or exp_id is None:
        logger.error(f"Usage: {sys.argv[0]} <dataset_code> <experiment id>")
        sys.exit()

    try:
        experiment = getattr(datasets, dataset_code).experiments[exp_id]
    except KeyError:
        logger.error(f"Experiment {exp_id} not found in {dataset_code}.")
        sys.exit()
    except AttributeError:
        logger.error(f"The dataset {dataset_code} doesn't exist.")
        sys.exit()

    _process_productions(experiment, )


if __name__ == "__main__":
    main()
