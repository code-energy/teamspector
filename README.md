# Teamspector
Teamspector is a complex networks framework for experimenting with
collaborative data. Currently it includes:

- IMDb data extraction (`extract-imdbws`)
- IMDb data pre-processing.
- IMDb EDA.

# Getting Started

Make sure you have all dependencies in `requirements.txt` installed. Installing
dependencies into a dedicated python virtual environment is advised.

First, download the IMDb data sources and extract it to a local MongoDB
collection:

    $ cd extract-imdbws
    $ mkdir datasets.imdbws.com
    $ wget -q -P datasets.imdbws.com -i files.txt
    $ gunzip datasets.imdbws.com/*.gz
    $ for f in *.py; do python "$f"; done

## New Data Sources
- [The MovieLens dataset](http://files.grouplens.org/datasets/movielens/ml-20m-README.html).
- Other collaborative networks:
    - Scientific Research ([google schoolar scrapper](http://www.icir.org/christian/scholar.html))
    - Github projects
    - Board of directors
    - High school students
    - Government cabinets
    - Small size military units
    - Book authors

## New Research Hypothesis
- Study the maturation time for nodes to become productive. Detect which nodes
  aren't maturating on time, predict whether they will maturate at all.
- Study whether teams with more influent nodes produce better results.

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
