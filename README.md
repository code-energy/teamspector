Teamspector is a complex networks framework for experimenting with
collaborative data. Currently it includes:

- An IMDb data extraction and pre-processing tools,
- An EDA notebook for exploring IMDb data,
- Scripts to build a social network from IMDb data, and to extract each movie's
  social and success metrics.

# Getting Started
Teamspector needs MongoDB, and should be installed in its own virtual
environment. For installation instructions, see `INSTALL.md`.  After installing
Teamspector, download the IMDb data sources, extract the data to a local
MongoDB collection, run the pre-processing rules:

    $ download imdbws
    $ extract imdbws
    $ preprocess imdbws

There is a smaller experiment that runs faster, just to test things. It has the
id `0`. The main experiment has id `1`. To run an experiment:

    $ experiment imdbws <experiment id>

# Dataset
The IMDb dataset is provided by Amazon: <https://www.imdb.com/interfaces/>.
This website describes in detail the data that's made available. All movies are
considered, except for:

    - Movies without year of release,
    - Not feature-length, cinema productions (`titleType != movie`),
    - Adult movies (`isAdult = True`).

# Pre-Processing
During pre-processing, movies' number of votes (`numVotes`) is converted into a
logarithm `log_votes`, as it has an exponential distribution.

The average ratings of movies are normalized into `nrating` using a Bayesian
estimate, as there are wild differences in the sample sizes taken into account
to produce the average. We suppose the Bayesian estimate can be trusted only
for movies that received five thousands of votes or more, hence `nrating` is
only defined for movies with `numVotes` ≥ 5000.

To calculate movie's success metrics, we check how well a movie did in terms of
`log_votes` and `nratings`, compared to other movies produced in the same year.
The percentile of a movie's `log_votes` and `nratings` within movies produced
in the same year is computed as `ypct_votes` and `ypct_rating`.

To produce our final movie score metric, `ypct_votes` and `ypct_rating` are
summed. The movie's percentile of this sum is computed into `ypct`. For this
percentile, we only consider movies produced in the same year. In other words,
if a movie has `ypct = 0.99`, this means the movie is considered better than
99% of the movies produced in the year the movie came out.

Finally, a binary success metric, `top100`, is defined to capture if the movie
was one of the best 100 movies produced in the year as measured by `ypct`. It's
only after 1985 that we have more than 100 movies each year that have a valid
`nratings` value, hence the `top100` metric is only defined for movies produced
this year or afterwards.

# Experiment
The goal of this experiment is to test the effect of social network structure
in human work. The experiment infers the social network graph from a group of
workers. Workers are nodes. Nodes who previously worked together are connected
via an edge. Edges are unordered, and their strength is proportional to the
number of previous works jointly conducted.

Edges and their nodes are removed from the graph after being inactive for eight
years. Only productions in which workers are part of the graph's giant
component are considered.

For each piece of work produced, we measure aspects of the social structure
from workers responsible for the piece of work, and success metrics related to
the piece of work. Afterwards, tests are conducted to measure the effect of
social structure on work success.

In the context of movie production, works are actors, producers, writers and
directors. Pieces of work are movies, their success metrics are `ypct` and
`top100`. The `build_network.py` uses the IMDb dataset to build the graph of
workers. For each movie produced, network metrics from workers and success
metrics from movies are stored in a separated table.
<!--'in a separated table' or 'in separate tables'?-->

## Methodology
The experiment runs in a loop, where each year is analyzed at a time. IMDb only
provides the year of release of movies, forcing us to consider movies produced
in a given year are all produced and released simultaneously.

We begin with an empty list of network graphs L.

Before each iteration of the loop, each graph in L is inspected and nodes that
haven't produced any work for over 8 years are removed along with their edges.
If this causes any of the graphs to become disconnected, the disconnected
graphs are added to L, while the original graph is removed from L

Then, we look into the productions released in the year. For each production,
we find the graphs in L which contain any of the production's workers. Workers
not present in the graph are added to the graph as new nodes. Edges between
workers are added, or strengthened in case they already exist. If we have
selected more than one graph from L, the now connected graphs are joined into a
single graph, which is added to L, and the original graphs which were joined
are removed from L.

### Time Frame
Experiment metrics are only collected starting from 1985, as success metrics
might not be reliable prior to this year. The experiment runs from 1985 to
2012. The reason 2012 was chosen instead of a more recent year is that we don't
know how long it takes after a movie is released for `ypct` and `top100` to
stabilize. We assume five years is a safe pick.

### Team Structure
For a large portion of movies, IMDb provides a list of producers, directors,
writers and actors. For some famous movies, more elements from the production
team may be available, such as editors, composers, and cinematographers.

Due to computational constraints, the experiment considers only producers,
directors and writers. Adding actors, the graphs become exceedingly big for
centrality network metrics to be feasibly computed.

### Network Metrics
For each production team, we collect social metrics related to each worker in
the team individually (Ego metrics), to the pairs of workers in the team (Pair
metrics) and to the team as a whole (Team metrics).

#### Ego Metrics
- [Closeness Centrality](https://en.wikipedia.org/wiki/Centrality#Closeness_centrality),
- [Betweenness Centrality](https://en.wikipedia.org/wiki/Centrality#Betweenness_centrality),
- [Clustering Coefficient](https://en.wikipedia.org/wiki/Clustering_coefficient),
- [Square Clustering](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.cluster.square_clustering.html),
- [Network Constraint](https://en.wikipedia.org/wiki/Structural_holes),
- Node's degreem
- Past Ratings: mean of `nrating` from node's prior works,
- Past Votes: mean of `log_votes` from node's prior works,
- Past Experience: the number of prior works the node was part of,

Each production will have as many ego metrics as the number of people in its
team. Hence, the maximum, minimum, median and standard deviation from the
metrics are calculated.

#### Team Metrics
Via [vertex contraction](http://mathworld.wolfram.com/VertexContraction.html),
all nodes that participated in the production being studied are temporarily
transformed in a single node. Then, all ego metrics are recalculated for the
contracted node representing the team. Besides that, another metric is taken:

- Team size: the number of nodes in the production team.

#### Pair Metrics

- Shared Collaborators: the number of nodes connected to both nodes of the
  pair,
- Neighbour Overlap: the shared collaborators number, divided by the number of
  nodes connected to either one of the nodes of the pair,
  the proportion of friends which are connected to both nodes,
- Past experience: the weight of the edge connecting the two nodes,

Production teams with more than two members will have many pairs. Hence, the
same aggregate statistics used for the Ego metrics are also used for the Pair
metrics.

# Contributing
If you like this project and want to participate, there's a lot of ways you can
help. Check out `CONTRIBUTING.md` for more info.

<!-- vim: set fdm=marker textwidth=79 colorcolumn=80: -->
