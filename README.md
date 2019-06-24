Teamspector is a complex networks framework for experimenting with
collaborative data. Currently it includes:

- An IMDb data extraction tool,
- IMDb data pre-processing scripts,
- An EDA notebook for IMDb data,
- Scripts to build a social network from IMDb data, and to extract each movie's
  social and success metrics.

# Getting Started

## MongoDB
Make sure MongoDB 4.x is installed and its daemon is running in your system. Do
to it with Mac OS X and Macports,

    $ sudo port install mongodb

## Python
Ensure you have all dependencies in `requirements.txt` installed in a dedicated
python virtual environment. You can use `virtualenvwrapper` to create your
virtual environment. To install it,

    $ sudo pip install virtualenvwrapper
    $ mkdir ~/.virtualenvs

Then add these two lines to your `~/.profile` file:

    export WORKON_HOME=~/.virtualenvs
    source virtualenvwrapper.sh

After you restart your shell session, `virtualenvwrapper` should be available.
You can create a new virtual environment with

    $ mkvirtualenv teamspector

After the environment has been created, activate it

    $ workon teamspector

After the virtual environment is active, install the dependencies by running

    (teamspector) $ pip install -r requirements.txt

## Downloading and Pre-Processing Data
First, download the IMDb data sources and extract it to a local MongoDB
collection:

    $ cd extract-imdbws
    $ mkdir datasets.imdbws.com
    $ wget -q -P datasets.imdbws.com -i files.txt
    $ gunzip datasets.imdbws.com/*.gz
    $ for f in *.py; do python "$f"; done
    $ cd ../pre-processing
    $ for f in *.py; do python "$f"; done

## Running the Experiment
Afterwards, you can run the experiment by running `build_network.py`:

    $ ./build_network.py

# Dataset Description

The IMDb dataset is provided by Amazon: <https://www.imdb.com/interfaces/>.
This website describes in detail the data that's made available. All movies are
considered, except for:

    - Movies without year of release,
    - Not feature-length, cinema productions (`titleType != movie`),
    - Adult movies (`isAdult = True`).

# Pre-Processing
During pre-processing, movies' number of votes (`numVotes`) is converted into a
logarithm `log_votes`, as it has an exponential distribution.

Movie's average ratings are normalized using a Bayesian estimate into
`nrating`, as there are wild differences in the sample sizes taken into account
to produce the average. We suppose the Bayesian estimate can be trusted only
for movies that have received five thousands of votes or more, hence `nrating`
is only defined for movies with `numVotes` ≥ 5000.

To calculate movie's success metrics, we compare how well a movie did in
metrics of `log_votes` and `nratings` compared to other movies produced in the
same year. The percentile of a movie's `log_votes` and `nratings` within movies
produced in the same year is computed as `ypct_votes` and `ypct_rating`.

To produce our final movie score metric, we movie's `ypct_votes` and
`ypct_rating`, and get the movie's percentile of this sum into `ypct`. Again
only considering movies produced in the same year. In other words, if a movie
has `ypct = 0.99`, this means the movie is considered better than 99% of the
movies produced in the year the movie came out.

Finally, a binary success metric, `top100`, is defined to capture if the movie
was one of the best 100 movies produced in the year as measured by `ypct`. It's
only after 1985 that we have more than 100 movies each year that have a valid
`nratings` value, hence the `top100` metric is only defined for movies produced
this year or afterwards.

# Future Improvements
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

## Improved Topological Information Extraction
- Add and evaluate Hyperbolic Centrality, from Paolo Boldi.
- Better use the weight information in the edges:
    - Clustering coefficient that considers the weight.
    - Implement/evaluate second type of weight: the strength of the edge
      increases in inverse proportion to total number of producers in the team.
- Nestedness: see if it can add novel information from teams or individuals.
- Incorporate homophily measures: https://goo.gl/WbyMQI.

## New Research Hypothesis
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

<!-- vim: set fdm=marker textwidth=79 colorcolumn=80: -->
