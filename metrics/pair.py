# Functions for calculating metrics related to pairs in a team.

import random
from itertools import combinations


def _random_pair(team):
    first, second = sorted(random.sample(range(len(team)), 2))
    return tuple(sorted([team[first], team[second]]))


def _generate_pairs(team):
    if len(team) <= 50:
        return combinations(team, 2)
    elif len(team) <= 90:
        return random.sample(list(combinations(team, 2)), 1225)
    else:
        pairs = set()
        while len(pairs) < 1225:
            pair = _random_pair(team)
            if pair not in pairs:
                pairs.add(pair)

        return tuple(pairs)


def neighbour_overlap(G, team):
    x = []

    for n1, n2 in _generate_pairs(team):
        n_n1 = set(G.neighbors(n1))
        n_n2 = set(G.neighbors(n2))
        intersect = n_n1.intersection(n_n2)
        union = n_n1.union(n_n2)

        x.append(len(intersect)/float(len(union)))

    return x


def past_experience(G, team):
    x = []
    for n1, n2 in _generate_pairs(team):
        x.append(G[n1][n2]['weight'] - 1)

    return x


def shared_collaborators(G, team):
    x = []

    for n1, n2 in _generate_pairs(team):
        n_n1 = set(G.neighbors(n1))
        n_n2 = set(G.neighbors(n2))
        x.append(len(n_n1.intersection(n_n2)))

    return x
