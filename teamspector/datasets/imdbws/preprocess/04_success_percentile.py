# A yearly and global success percentile is calculated, based on the
# percentiles for normalized ratings, and for the number of votes.
#
# Movies are assigned into two groups: the top 100 movies for the year, and
# non-top-100 ones.
#
# Prior to 1985, less than 100 movies per year received over 5k votes. To keep
# consistency, only movies from 1985 onwards are considered for the success
# metrics.

import pandas as pd
from tqdm import tqdm
from pymongo import MongoClient

client = MongoClient()
db = client.imdbws
qry = {'is_subject': True, 'startYear': {'$gte': 1985}}
df = pd.DataFrame(list(db.titles.find(qry)))

g = df.groupby('startYear')

r = g.log_votes.apply(lambda x: x.rank(pct=True))
df['ypct_votes'] = r

r = g.nrating.apply(lambda x: x.rank(pct=True, na_option='top'))
df['ypct_rating'] = r

df['pct_votes'] = df.log_votes.rank(pct=True)
df['pct_rating'] = df.nrating.rank(pct=True, na_option='top')

combined_rank = df.pct_rating + df.pct_votes
df['pct'] = combined_rank.rank(pct=True)


def year_rank(x):
    return (x.ypct_rating + x.ypct_votes).rank(pct=True)


g = df.groupby('startYear', as_index=False)
df['ypct'] = g.apply(year_rank).reset_index(level=0, drop=True)

df['top100'] = False
yrank = df.groupby('startYear').ypct.rank(method='first', ascending=False)
df.loc[yrank <= 100, 'top100'] = True

for _, r in tqdm(df.iterrows(), total=df.shape[0]):
    data = {'ypct': r['ypct'], 'ypct_votes': r['ypct_votes'],
            'ypct_rating': r['ypct_rating'], 'pct': r['pct'],
            'pct_votes': r['pct_votes'], 'pct_rating': r['pct_rating'],
            'top100': r['top100']}
    db.titles.update({'_id': r['_id']}, {'$set': data})
