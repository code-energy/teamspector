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

fig = plt.gcf()

df['Decade'] = ((df['startYear'] // 10) * 10).astype('str') + 's'

ax = df.boxplot('averageRating', by='Decade', showfliers=False)
ax.set_ylim(1, 10)  # Movies are can be rated from 1 to 10.
ax.xaxis.grid(False)
ax.tick_params(which='both', bottom='off', top='off', left='off', right='off')

plt.title("Distribution of Ratings by Decade", y=1.1, fontsize=10)
plt.suptitle("feature length movies from 1930 to 2016")
plt.ylabel('Votes')

plt.savefig('boxplot-decades-ratings.pdf', bbox_inches='tight')
plt.close(fig)
