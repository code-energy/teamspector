# Adds TSV data of movie ratings from IMDB into a MongoDB collection. Also
# removes movies that have zero ratings.

import os
import csv

from pymongo import MongoClient
from bson.decimal128 import Decimal128

db = MongoClient().imdbws

root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + "/datasets.imdbws.com/title.ratings.tsv"

counter = 0

for row in csv.DictReader(open(path), delimiter='\t'):
    if db.movies.find_one({'_id': row['tconst']}):
        db.movies.update({'_id': row['tconst']}, {'$set':
                         {'averageRating': Decimal128(row['averageRating']),
                          'numVotes': int(row['numVotes'])}})

        counter += 1
        if counter % 10000 == 0:
            print ("{} movies updated.".format(counter))


result = db.movies.delete_many({'numVotes': {'$exists': False}})
if result.deleted_count:
    print ("Removed {} movies without ratings.".format(result.deleted_count))
