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

fig = plt.gcf()

df['Decade'] = ((df['startYear'] // 10) * 10).astype('str') + 's'

ax = df.boxplot('numVotes', by='Decade', showfliers=False)
ax.set_ylim(5)  # Movies don't have negative votes.
ax.set_yscale('log')
ax.xaxis.grid(False)
ax.tick_params(which='both', bottom='off', top='off', left='off', right='off')

plt.title("Distribution of Votes by Decade", y=1.1, fontsize=10)
plt.suptitle("feature length movies from 1930 to 2016")
plt.ylabel('Votes')

plt.savefig('boxplot-decades-votes.pdf', bbox_inches='tight')
plt.close(fig)
