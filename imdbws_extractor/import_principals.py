# Adds TSV data of principals (main actors and actresses) from IMDB into a
# MongoDB collection.

import os
import csv

from pymongo import MongoClient

db = MongoClient().imdbws

root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + '/datasets.imdbws.com/title.principals.tsv'

counter = 0

for row in csv.DictReader(open(path), delimiter='\t'):
    if db.movies.find_one({'_id': row['tconst']}):
        row['principalCast'] = row['principalCast'].split(',')
        db.movies.update({'_id': row['tconst']}, {'$set':
                         {'principalCast': row['principalCast']}})

        counter += 1
        if counter % 10000 == 0:
            print ("{} movies updated.".format(counter))
