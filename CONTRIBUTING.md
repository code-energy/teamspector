We're open to pull requests! If you want some inspiration of how to contribute
to the project, here's an interesting list of things we thought of exploring
next:

# New Data Sources
- [The MovieLens dataset](http://files.grouplens.org/datasets/movielens/ml-20m-README.html).
- Other collaborative networks:
    - Scientific Research ([google schoolar scrapper](http://www.icir.org/christian/scholar.html))
    - Github projects
    - Board of directors
    - High school students
    - Government cabinets
    - Small size military units
    - Book authors

# Improved Topological Information Extraction
- Add and evaluate Hyperbolic Centrality, from Paolo Boldi.
- Better use the weight information in the edges:
    - Clustering coefficient that considers the weight.
    - Implement/evaluate second type of weight: the strength of the edge
      increases in inverse proportion to total number of producers in the team.
- Nestedness: see if it can add novel information from teams or individuals.
- Incorporate homophily measures: https://goo.gl/WbyMQI.

# New Research Hypothesis
- Study the maturation time for nodes to become productive. Detect which nodes
  aren't maturating on time, predict whether they will maturate at all.
- Study whether teams with more influent nodes produce better results.
- Predict how likely a crew member is to take part in any of the future most
  important movies next year.

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
