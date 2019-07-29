import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__.split("/")[-1])


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
