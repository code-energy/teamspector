# Adds TSV data of movie ratings from IMDB into a MongoDB collection. Movies
# for which no ratings are available receive a NULL value.

import os
import csv
import logging

from tqdm import tqdm
from pymongo import MongoClient
from bson.decimal128 import Decimal128

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__.split("/")[-1])
logger.info("Update movies' with their ratings…")

db = MongoClient().imdbws

root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + "/../raw/title.ratings.tsv"
total = sum(1 for i in open(path, 'rb'))
all_rows = csv.DictReader(open(path), delimiter='\t', quoting=csv.QUOTE_NONE)

for row in tqdm(all_rows, total=total):
    if db.productions.find_one({'_id': row['tconst']}):
        x = {'$set': {'averageRating': Decimal128(row['averageRating']),
                      'numVotes': int(row['numVotes'])}}
        db.productions.update_one({'_id': row['tconst']}, x)


x = db.productions.update_many({'numVotes': {'$exists': False}},
                               {'$set': {'numVotes': None,
                                         'averageRating': None}})
logger.info(f"Updated {x.modified_count} movies without ratings.")
