# About Teamspector
Teamspector is a complex network framework for experimenting with collaborative
social data. It was used in the following research:

- A Network Analysis on Movie Producing Teams and Their Success, LA-WEB '14
  (<http://dl.acm.org/citation.cfm?id=2708863>)
- Pick the Right Team and Make a Blockbuster: a Social Analysis through
  Movie History, SAC '16


# Directions for Improvement

## Bugs to fix
- Financial values are sometimes extracted incorrectly. Currently the top value
  at the front of the list is extracted, and this might lead to
  inconsistencies. Financial data should be evaluated in order to determine the
  best way to use them experimentally. Values should match these:
  http://www.boxofficemojo.com/alltime/adjusted.htm

## Data visualization and graphs
- Perform network renderings with Gephi.

## Topological information extraction from movie teams
- Add and evaluate Hyperbolic Centrality, from Paolo Boldi.
- Better use the weight information in the edges:
    - Clustering coefficient that considers the weight.
    - Implement/evaluate second type of weight: the strength of the edge
      increases in inverse proportion to total number of producers in the team.
- Nestedness: see if it can add novel information from teams or individuals.
- Incorporate homophily measures: https://goo.gl/WbyMQI.

## Non-Topological information extraction from movie teams
- Use the locations from movies (i.e. location history diversity from team
  members as a new ego or team metric).

## Methodology
- Better method for historical inflation correction and currency exchange.
- Improve the IMDB data extracting script.
- Map everything that might change between experiments
    - Create a JSON structure with that, to describe a different experiment.
- Define a minimal key performance indicators number(s) for experiments.
- Record experiment results and unique JSON settings upon running experiments.

## Regression Accuracy
- Use Amazon Machine Learning: https://aws.amazon.com/machine-learning/.

## Dataset
- Incorporate data from the MovieLens dataset:
  http://files.grouplens.org/datasets/movielens/ml-20m-README.html
- Get all useful information from IMDB into the internal MongoDB collection.
  Example of information that could be useful: color info, languages, plot,
  votes distribution, etc. See
  http://imdbpy.sourceforge.net/docs/README.package.txt.
- Incorporate other types of social networks:
    - Scientific Research,
      http://www.icir.org/christian/scholar.html (google schoolar scrapper)
    - Github projects
    - Board of directors
    - High school students
    - Government cabinets
    - Small size military units
    - Book authors

## Research Hipothesys
- Study the maturation time for nodes to become productive. Detect with nodes
  aren't maturating on time, predict whether they will maturate at all.
- Study whether teams with more influent nodes produce better results.

## Code Quality
- Unit tests to ensure that the random clustering coefficient and path length
  are being computed correctly.

# Related Work

## Collaborative networks
- Amaral, Scala, Barthelemy & Stanley, 2000
- Herr, Ke, Hardy & Börner, 2007
- Watts & Strogatz, 1998
- Mei-Chen Yeh, Wen-Po Wu, 2007
  Clustering Faces in Movies Using an Automatically Constructed Social Network.

### Visualizing
- Dominique Haughton, Mark-David McLaughlin, Kevin Mentzer, Changan Zhang, 2014
  Movie analytics: Visualization of the co-starring network

### Success Prediction
- An Zeng, Stanislao Gualdi, Matus Medo, Yi-Cheng Zhang, 2013
  Trend Prediction in Temporal bipartite Networks: the Case of MovieLens,…
- Daehoon Kim, Daeyong Kim, Eenjun Hwang, Hong-Gu, 2013
  Choi: A user opinion and metadata mining scheme for predicting box office…
- Li Zhang, Jianhua Luo, Suying Yang, 2009
  Forecasting box office revenue of movies with BP neural network
- Predicting Golden Globe Awards & Christmas Day Gross (http://goo.gl/gCbEyQ)

<!-- vim: set fdm=marker textwidth=79 colorcolumn=80: -->
