# A yearly and global success percentile is calculated, based on the
# percentiles for normalized ratings, and for the number of votes.
#
# Movies are also assigned into three groups:
#   A: top 100 movies for the year.
#   B: top 100-200 movies for the year.
#   C: the rest of the movies.

import pandas as pd

from pymongo import MongoClient

client = MongoClient()
db = client.imdbws
df = pd.DataFrame(list(db.titles.find({'is_subject': True})))

g = df.groupby('startYear')

r = g.log_votes.apply(lambda x: x.rank(pct=True))
df['ypct_votes'] = r

r = g.nrating.apply(lambda x: x.rank(pct=True, na_option='keep'))
df['ypct_rating'] = r

df['pct_votes'] = df.log_votes.rank(pct=True)
df['pct_rating'] = df.nrating.rank(pct=True, na_option='keep')

combined_rank = df.pct_rating.fillna(df.pct_votes) + df.pct_votes
df['pct'] = combined_rank.rank(pct=True)

def year_rank(x):
   return (x.ypct_rating.fillna(x.ypct_votes) + x.ypct_votes).rank(pct=True)
g = df.groupby('startYear', as_index=False)
df['ypct'] = g.apply(year_rank).reset_index(level=0, drop=True)

df['group'] = 'C'
yrank = df.groupby('startYear').ypct.rank(method='first', ascending=False)
df.loc[yrank <= 200, 'group'] = 'B'
df.loc[yrank <= 100, 'group'] = 'A'

i = 0
for _, r in df.iterrows():
    i += 1
    data = {'ypct': r['ypct'], 'ypct_votes': r['ypct_votes'],
            'ypct_rating': r['ypct_rating'], 'pct': r['pct'],
            'pct_votes': r['pct_votes'], 'pct_rating': r['pct_rating'],
            'group': r['group']}
    db.titles.update({'_id': r['_id']}, {'$set': data})
    if i % 1000 == 0:
        print("{} titles updated.".format(i))
