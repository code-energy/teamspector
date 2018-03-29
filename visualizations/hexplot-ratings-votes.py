import numpy as np
import pandas as pd
from pymongo import MongoClient

from plot_utils import plot_config
plot_config()
import matplotlib.pyplot as plt

db = MongoClient().imdbws
data = db.titles.find({'startYear': {'$gte': 1930, '$lte': 2013},
                       'titleType': 'movie'})
df = pd.DataFrame(list(data))

# Numpy doesn't support MongoDB's Decimal128, let's transform it to Float.
to_decimal = lambda x: float(x.to_decimal()) if 'to_decimal' in dir(x) else x
df['averageRating'] = df['averageRating'].apply(to_decimal)

ax = df.plot.hexbin('numVotes', 'averageRating', bins='log', xscale='log',
                    edgecolors='w', linewidths=(0.01,), cmap=plt.cm.Blues,
                    gridsize=40)

ax.set_ylim(1, 10)  # Ratings go from 1 to 10.
ax.set_xlim(5)  # Movies don't have negative votes.

ax.tick_params(which='both', bottom='off', top='off', left='off', right='off')

# Manually get the colorbar axis to set its label.
fig = plt.gcf()
cax = fig.get_axes()[1]
cax.set_ylabel(r'$\log_{10}(n)$')
cax.tick_params(which='both', right='off')

plt.title("Average Rating per Number of Votes", y=1.1, fontsize=10)
plt.suptitle("feature length movies from 1930 to 2016")

plt.xlabel('Votes')
plt.ylabel('Average Rating')

plt.savefig('hexplot-ratings-votes.pdf', bbox_inches='tight')
plt.close(fig)
