import numpy as np
from pymongo import MongoClient

from plot_utils import plot_config
plot_config()
import matplotlib.pyplot as plt

db = MongoClient().imdbws
data = list(db.titles.find({'is_subject': True}))

all_data = []
all_years = sorted(list(set([m['startYear'] for m in data])))

for y in all_years:
    all_data.append(len([m for m in data if m['startYear'] == y]))

fig = plt.figure()
ax = fig.add_subplot(111)

locs = range(1, len(all_years)+1)
ax.bar(locs, all_data, color='0.0', width=1.0, linewidth=0, log=True)

ax.set_ylabel('Movies')
ax.set_yscale('log')

ax.set_xlabel('Years')
ax.set_xlim([1, len(all_years)])
fig.autofmt_xdate()

ax.tick_params(which='both', bottom='off', top='off', left='off', right='off')

plt.savefig('histogram.pdf', bbox_inches='tight')
plt.close(fig)
