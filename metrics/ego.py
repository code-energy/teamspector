# Functions for calculating ego-metrics from nodes in a social graph.

import math
import functools
import numpy as np
import networkx as nx

from pymongo import MongoClient

from . import structural_holes

db = MongoClient().imdbws


def closeness(G, v, startYear, base_qry):
    return nx.closeness_centrality(G, u=v)


@functools.lru_cache(maxsize=2)
def _cached_betweenness(G):
    """
    Per "Centrality Estimation in Large Networks", log(n) pivots are needed.
    """
    pivots = int(math.ceil(math.log(len(G), 2)))
    return nx.betweenness_centrality(G, k=pivots, normalized=True)


def betweenness(G, v, startYear, base_qry):
    return _cached_betweenness(G)[v]


def previous_rating(G, v, startYear, base_qry):
    """
    Calculate previous gross from team members. Returns None if there are no
    previous ratings.
    """
    x = []

    if v == 'contracted':
        v = {'$in': G.node[v]['original']}

    base_qry.update({'team': v, 'nrating': {'$ne': None},
                     'startYear': {'$lt': startYear}})

    movs = db.titles.find(base_qry)
    if movs.count():
        x.append(np.average([mov['nrating'] for mov in movs]))

    return np.average(x) if x else None


def previous_votes(G, v, startYear, base_qry):
    """
    Calculate previous votes from team members. Returns None if there are no
    previous votes.
    """
    x = []

    if v == 'contracted':
        v = {'$in': G.node[v]['original']}

    base_qry.update({'team': v, 'log_votes': {'$ne': None},
                     'startYear': {'$lt': startYear}})

    movs = db.titles.find(base_qry)
    if movs.count():
        x.append(np.average([math.log(mov['log_votes']) for mov in movs]))

    return np.average(x) if x else None


def clustering(G, v, startYear, base_qry):
    return nx.clustering(G, v)


def square_clustering(G, v, startYear, base_qry):
    return nx.square_clustering(G, nodes=[v])[v]


def previous_experience(G, v, startYear, base_qry):
    if v == 'contracted':
        v = {'$in': G.node[v]['original']}

    base_qry.update({'team': v, 'startYear': {'$lt': startYear}})

    return db.titles.find(base_qry).count()


def network_constraint(G, v, startYear, base_qry):
    return structural_holes.constraint(G, v)


def degree(G, v, startYear, base_qry):
    return G.degree(v)
