import logging
from .. import network
from . import aggregations, ego, pair

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__.split("/")[-1])


def calculate_aggregations(data):
    """
    Receives a dictionary where keys are measurement names and values are lists
    of measurements. Return a dictionary where keys are aggregations from the
    values from the input dictionary.
    """
    results = {}
    for metric_name, metric in data.items():
        metric = list(filter(lambda x: x is not None, metric))
        aggs = [getattr(aggregations, x) for x in aggregations.__all__]
        for agg in aggs:
            result = agg(metric) if metric else None
            results[f'{metric_name}_{agg.__name__}'] = result
    return results


def calc_ego(H, team, release, base_qry):
    """
    Given a graph and a team, calculates all ego metrics for each team member.
    Returns a dictionary where keys are ego metric names, and values are the
    computed values from each team member.
    """
    m = {}
    metrics = [getattr(ego, x) for x in ego.__all__]

    for metric in metrics:
        logger.debug(f"Calculating ego metric {metric.__name__}")
        values = []
        for member in team:
            values.append(metric(H, member, release, base_qry.copy()))
        m[f'ego_{metric.__name__}'] = values

    return calculate_aggregations(m)


def calc_pair(H, team):
    """
    Given a graph and a team, calculates all pair-wise metrics for possible
    team pairs. Returns a dictionary where keys are the pair metric names, and
    values are the computed values from each pair.
    """
    m = {}

    metrics = [getattr(pair, x) for x in pair.__all__]
    for metric in metrics:
        logger.debug(f"Calculating pair metric {metric.__name__}")
        m[f'pair_{metric.__name__}'] = metric(H, team)

    return calculate_aggregations(m)


def calc_team(H, team, release, base_qry):
    """
    Given a graph and a team, calculates all team-wise metrics Returns a
    dictionary where keys are the team metric names, and values are the
    computed metric values.
    """
    _H = network.contract_edges(H, team)

    m = {}
    metrics = [getattr(ego, x) for x in ego.__all__]
    for metric in metrics:
        logger.debug(f"Calculating team metric {metric.__name__}")
        qry = base_qry.copy()
        m[f'team_{metric.__name__}'] = metric(_H, 'contracted', release, qry)

    m['team_size'] = len(team)

    return m
