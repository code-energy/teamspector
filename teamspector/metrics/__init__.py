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
        for agg_name, agg_func in aggs:
            result = agg_func(metric) if metric else None
            results['%s_%s' % (metric_name, agg_name)] = result
    return results


def calc_ego(H, team, release, base_qry):
    """
    Given a graph and a team, calculates all ego metrics for each team member.
    Returns a dictionary where keys are ego metric names, and values are the
    computed values from each team member.
    """
    m = {}
    metrics = [getattr(ego, x) for x in ego.__all__]

    for metric_name, metric_func in metrics:
        logger.debug(f"Calculating ego metric {metric_name}")
        values = []
        for member in team:
            values.append(metric_func(H, member, release, base_qry.copy()))
        m[f'ego_{metric_name}'] = values

    return calculate_aggregations(m)


def calc_pair(H, team):
    """
    Given a graph and a team, calculates all pair-wise metrics for possible
    team pairs. Returns a dictionary where keys are the pair metric names, and
    values are the computed values from each pair.
    """
    m = {}

    metrics = [getattr(pair, x) for x in pair.__all__]
    for metric_name, metric_func in metrics:
        logger.debug(f"Calculating pair metric {metric_name}")
        m[f'pair_{metric_name}'] = metric_func(H, team)

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
    for metric_name, metric_func in metrics:
        logger.debug(f"Calculating team metric {metric_name}")
        qry = base_qry.copy()
        m[f'team_{metric_name}'] = metric_func(_H, 'contracted', release, qry)

    m['team_size'] = len(team)

    return m
