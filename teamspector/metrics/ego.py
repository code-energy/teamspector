# Functions for calculating ego-metrics from nodes in a social graph.

import math
import functools
import numpy as np
import networkx as nx

from pymongo import MongoClient

from . import structural_holes

db = MongoClient().imdbws


__all__ = ['closeness', 'betweenness', 'previous_rating', 'previous_ypct',
           'previous_top100', 'previous_votes', 'clustering',
           'square_clustering', 'previous_experience', 'network_constraint',
           'degree']

_cache_closeness = {}


def closeness(G, v, startYear, base_qry):
    if not (v, startYear) in _cache_closeness:
        closeness = nx.closeness_centrality(G, u=v)
        _cache_closeness[(v, startYear)] = closeness
        return closeness

    return _cache_closeness[(v, startYear)]


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

    base_qry.update({'team.id': v, 'nrating': {'$ne': None},
                     'startYear': {'$lt': startYear}})

    movs = db.productions.find(base_qry)
    if movs.count():
        x.append(np.average([mov['nrating'] for mov in movs]))

    return np.average(x) if x else None


def previous_ypct(G, v, startYear, base_qry):
    """
    Calculate previous ypct from team members. Returns None if there are no
    previous ypct.
    """
    x = []

    if v == 'contracted':
        v = {'$in': G.node[v]['original']}

    base_qry.update({'team.id': v, 'ypct': {'$ne': None},
                     'startYear': {'$lt': startYear}})

    movs = db.productions.find(base_qry)
    if movs.count():
        x.append(np.average([mov['ypct'] for mov in movs]))
    return np.average(x) if x else None


def previous_top100(G, v, startYear, base_qry):
    """
    Gets the number of previous productions labeled top100 from team members.
    """
    if v == 'contracted':
        v = {'$in': G.node[v]['original']}

    base_qry.update({'team.id': v, 'top100': True,
                     'startYear': {'$lt': startYear}})

    return db.productions.find(base_qry).count()


def previous_votes(G, v, startYear, base_qry):
    """
    Calculate previous votes from team members. Returns None if there are no
    previous votes.
    """
    x = []

    if v == 'contracted':
        v = {'$in': G.node[v]['original']}

    base_qry.update({'team.id': v, 'log_votes': {'$ne': None},
                     'startYear': {'$lt': startYear}})

    movs = db.productions.find(base_qry)
    if movs.count():
        x.append(np.average([mov['log_votes'] for mov in movs]))

    return np.average(x) if x else None


def clustering(G, v, startYear, base_qry):
    return nx.clustering(G, v)


def square_clustering(G, v, startYear, base_qry):
    return nx.square_clustering(G, nodes=[v])[v]


def previous_experience(G, v, startYear, base_qry):
    if v == 'contracted':
        v = {'$in': G.node[v]['original']}

    base_qry.update({'team.id': v, 'startYear': {'$lt': startYear}})

    return db.productions.find(base_qry).count()


def network_constraint(G, v, startYear, base_qry):
    return structural_holes.constraint(G, v)


def degree(G, v, startYear, base_qry):
    return G.degree(v)
