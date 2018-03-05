# Plots the distribution of ratings as ViolinPlots, binned by # of votes.

import numpy as np
import pandas as pd
from pymongo import MongoClient

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import seaborn as sns


db = MongoClient().imdbws

data = db.movies.find({}, {'_id': 0, 'numVotes':1, 'averageRating': 1})
df = pd.DataFrame(list(data))

# Numpy doesn't support MongoDB's Decimal128, so let's transform it to Float.
to_decimal = lambda x: float(x.to_decimal()) if 'to_decimal' in dir(x) else x
df['averageRating'] = df['averageRating'].apply(to_decimal)

def name_bins(g):
    g['numVotes'] = g.name
    return g

fig, ax = plt.subplots()
fig.set_size_inches(8, 4)

break_points = [0, 5000, 10000, 25000, 100000, 300000, np.inf]
labels = ["0-5k", "5-10k", "10-25k", "25-100k", "100-300k", "300k+"]
dfx = df.groupby(pd.cut(df.numVotes, break_points, labels=labels))

dfx = dfx.apply(name_bins)

# TODO: Investigate about this line not producing any effect:
# sns.set_style("darkgrid", {"axes.facecolor": ".5",  'axes.grid': True,})

ax = sns.violinplot(data=dfx, x="numVotes", y="averageRating", showmeans=False,
        showmedians=True, showfliers=False, order=labels, color="seagreen")
ax.yaxis.grid(True)
ax.set_ylim(1,10)
ax.figure.savefig("votes-ratings.pdf")
plt.close()
