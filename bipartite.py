# This appends teams from a bipartite graph into a one-mode-graph, keeping the
# degree information from the original (bipartite) network in the projected
# graphs.

from datetime import timedelta
from itertools import combinations
from functools import reduce

import networkx as nx


def sorted_append(components, to_insert):
    """
    Inserts a components in the list of components, in their size ordering.
    Returns the inserted position.
    """
    pos = len(components)
    for i, component in enumerate(list(components)):
        if len(to_insert) > len(component):
            pos = i
            break

    components.insert(pos, to_insert)

    return pos


def update_components(components, team, team_id, team_date):
    """
    Given a list of components representing a graph and a team (clique) to be
    inserted in the graph, calculate the new components. Keeps the list of
    components ordered by size.

    Returns True if the update happened in the giant component.
    """
    # Pick components to join, keeping the movies that made the new component.
    new_comp = []
    movies = {}
    for producer in team:
        for component in list(components):
            if producer in component:
                if component not in new_comp:
                    new_comp.append(component)
                    movies.update(component.graph['movies'])
                    components.remove(component)
                break

    # Actually join the components, with the new and updated movies index.
    new_comp = reduce(lambda x, y: nx.union(x, y), new_comp, nx.Graph())
    movies[team_id] = len(team)
    new_comp.graph['movies'] = movies

    # Add new edges, and update the node's internal movies index and timestamp.
    for p1, p2 in list(combinations(team, 2)):
        if new_comp.has_edge(p1, p2):
            new_comp[p1][p2]['weight'] += 1
        else:
            new_comp.add_edge(p1, p2, weight=1)

    for element in team:
        new_comp.node[element].setdefault('movies', [])
        new_comp.node[element]['movies'].append(team_id)
        new_comp.node[element]['last'] = team_date
        new_comp.node[element].setdefault('first', team_date)

    # Add the new component to the list of components.
    pos = sorted_append(components, new_comp)

    return pos == 0


def remove_nodes_from_component(component, nodes):
    """
    Removes nodes from a component, keeping internal movie indexes updated.
    """
    for removing in nodes:
        for mov in list(component.node[removing]['movies']):
            if mov in component.graph['movies']:
                component.graph['movies'][mov] -= 1
                if component.graph['movies'][mov] == 1:
                    del component.graph['movies'][mov]
                    for node in component.nodes():
                        if mov in component.node[node]['movies']:
                            component.node[node]['movies'].remove(mov)

    component.remove_nodes_from(nodes)


def split_non_connected_component(component):
    """Splits a non-connected component into connected sub-components."""

    new = list(nx.connected_component_subgraphs(component))
    old_movies = component.graph['movies']

    for new_c in new:
        new_c.graph['movies'] = {}
        for node in new_c:
            for movie in new_c.node[node]['movies']:
                if movie not in new_c.graph['movies']:
                    new_c.graph['movies'][movie] = old_movies[movie]

    return new


def prune_components(components, date):
    '''Remove inactive nodes considering the given date.'''

    dead = lambda c, x: (date - c.node[x]['last']) > timedelta(days=8*365)

    for component in list(components):
        to_remove = [n for n in component if dead(component, n)]
        if to_remove:
            remove_nodes_from_component(component, to_remove)

            if not len(component):
                components.remove(component)
                continue

            elif not nx.is_connected(component):
                components.remove(component)
                novos = list(split_non_connected_component(component))
                components += novos  # split_non_connected_component(component)

    return sorted(components, key=lambda x: -len(x))
