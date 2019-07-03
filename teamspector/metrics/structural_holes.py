# Calculates Burt's "Network Constraint" structural hole measures in the
# context of a co-production network.


def tie_strength(G, a, b):
    """
    Returns the tie strength between A and B, with respect to A. It's the
    fraction of A's productions where B also participated.
    """
    if G.has_edge(a, b):
        return G[a][b]['weight'] / float(len(G.node[a]['movies']))
    return 0


def rel_tie_strength(G, a, b):
    """
    Returns the relative tie strength between A and B, with respect to A. It's
    the tie strength between A and B, divided by the sum of strengths from A's
    ties. It measures the relative social energy A invested in B.
    """
    a_b = tie_strength(G, a, b)
    if a_b:
        total = sum([tie_strength(G, a, x) for x in G.neighbors(a)])
        return a_b / float(total)
    return 0


def local_constraint(G, a, b):
    """
    Returns Burt's "local constraint" of B with respect to A. It captures the
    extent to which A constrains B's connectivity.
    """
    constraint = rel_tie_strength(G, a, b)
    for x in [x for x in G.neighbors(a) if x == b]:
        constraint += rel_tie_strength(G, a, x) * rel_tie_strength(G, x, b)
    return (constraint)**2


def constraint(G, a):
    """
    Burt's "network constraint" measure.
    """
    constraint = 0
    for b in G.neighbors(a):
        constraint += local_constraint(G, a, b)
    return constraint
