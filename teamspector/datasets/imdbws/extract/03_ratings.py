# Adds TSV data of movie ratings from IMDB into a MongoDB collection. Movies
# for which no ratings are available receive a NULL value.

import os
import csv

from tqdm import tqdm
from pymongo import MongoClient
from bson.decimal128 import Decimal128

db = MongoClient().imdbws

root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + "/../raw/title.ratings.tsv"
total = sum(1 for i in open(path, 'rb'))
all_rows = csv.DictReader(open(path), delimiter='\t', quoting=csv.QUOTE_NONE)

for row in tqdm(all_rows, total=total):
    if db.titles.find_one({'_id': row['tconst']}):
        x = {'$set': {'averageRating': Decimal128(row['averageRating']),
                      'numVotes': int(row['numVotes'])}}
        db.titles.update_one({'_id': row['tconst']}, x)


x = db.titles.update_many({'numVotes': {'$exists': False}},
                          {'$set': {'numVotes': None, 'averageRating': None}})
print("Updated {} titles without ratings.".format(x.modified_count))
