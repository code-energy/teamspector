# Adds TSV data of crew (writers and directors) from IMDB into a MongoDB
# collection.

import os
import csv
import logging

from tqdm import tqdm
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__.split("/")[-1])
logger.info("Adding directors and writers to movies' production teams…")

db = MongoClient().imdbws

root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + "/../raw/title.crew.tsv"

total = sum(1 for i in open(path, 'rb'))
all_rows = csv.DictReader(open(path), delimiter='\t', quoting=csv.QUOTE_NONE)

for row in tqdm(all_rows, total=total):
    if db.productions.find_one({'_id': row['tconst']}):
        team = []
        if row['directors'] != "\\N":
            for d in row['directors'].split(','):
                team.append({'ordering': None, 'id': d, 'jobs': ['director']})

        if row['writers'] != "\\N":
            for w in row['writers'].split(','):
                team.append({'ordering': None, 'id': w, 'jobs': ['writer']})

        db.productions.update_one({'_id': row['tconst']},
                                  {'$set': {'team': team}})

db.productions.create_index([('team.id', 1)])
