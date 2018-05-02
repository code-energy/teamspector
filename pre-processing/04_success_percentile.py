# Adds percentiles for the normalized ratings, and for the number of votes.
# Adds a success percentile based on the sum of the above percentiles.
# Bins movies into three groups:
#   A: 0.95–1 success percentile. (~15K movies)
#   B: 0.9–0.95 success percentile. (~15K movies)
#   C: 0—0.95 success percentile. (~284K movies)

import pandas as pd

from pymongo import MongoClient

client = MongoClient()
db = client.imdbws

data = db.titles.find({'is_subject': True})
df = pd.DataFrame(list(data))

df['percentile_log_votes'] = df['log_votes'].rank(pct=True)
df['percentile_nrating'] = df['nrating'].rank(pct=True)
df['sum_percentiles'] = (df['percentile_log_votes'] + df['percentile_nrating'])
df['percentile_sum_success'] = df['sum_percentiles'].rank(pct=True)

bins = [0, 0.9, 0.95, 1]
labels = ['C', 'B', 'A']
df['group'] = pd.cut(df.percentile_sum_success, bins=bins, labels=labels)

i = 0
for _, row in df.iterrows():
    i += 1
    new_data = {'percentile_log_votes': row['percentile_log_votes'],
                'percentile_nrating': row['percentile_nrating'],
                'percentile_sum_success': row['percentile_sum_success'],
                'group': row['group']}
    db.titles.update({'_id': row['_id']}, {'$set': new_data})
    if i % 1000 == 0:
        print("{} titles updated.".format(i))
