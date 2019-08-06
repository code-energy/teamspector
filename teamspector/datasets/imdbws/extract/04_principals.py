# Adds TSV data of principals (key people of movie's crew) from IMDB into a
# MongoDB collection.

import os
import csv

from tqdm import tqdm
from pymongo import MongoClient

db = MongoClient().imdbws

root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + '/../raw/title.principals.tsv'
total = sum(1 for i in open(path, 'rb'))
all_rows = csv.DictReader(open(path), delimiter='\t', quoting=csv.QUOTE_NONE)

for row in tqdm(all_rows, total=total):
    t = db.titles.find_one({'_id': row['tconst']})
    if t:
        team = {p['id']: p for p in t['team']}
        _id = row['nconst']

        if _id not in team:
            team[_id] = {'id': _id, 'ordering': None, 'jobs': []}

        ordering = int(row['ordering'])
        if not (team[_id]['ordering']) or (ordering > team[_id]['ordering']):
            team[_id]['ordering'] = ordering

        if not row['category'] in team[_id]['jobs']:
            team[_id]['jobs'].append(row['category'])

        if row['job'] != r'\N' and row['job'] not in team[_id]['jobs']:
            team[_id]['jobs'].append(row['job'])

        team = list(team.values())
        db.titles.update_one({'_id': row['tconst']}, {'$set': {'team': team}})
