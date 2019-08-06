# Adds TSV data of crew (writers and directors) from IMDB into a MongoDB
# collection.

import os
import csv

from tqdm import tqdm
from pymongo import MongoClient

db = MongoClient().imdbws

root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + "/../raw/title.crew.tsv"

total = sum(1 for i in open(path, 'rb'))
all_rows = csv.DictReader(open(path), delimiter='\t', quoting=csv.QUOTE_NONE)

for row in tqdm(all_rows, total=total):
    if db.titles.find_one({'_id': row['tconst']}):
        team = []
        if row['directors'] != "\\N":
            for d in row['directors'].split(','):
                team.append({'ordering': None, 'id': d, 'jobs': ['director']})

        if row['writers'] != "\\N":
            for w in row['writers'].split(','):
                team.append({'ordering': None, 'id': w, 'jobs': ['writer']})

        db.titles.update_one({'_id': row['tconst']}, {'$set': {'team': team}})
