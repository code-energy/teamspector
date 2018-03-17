# Adds TSV data of principals (main actors and actresses) from IMDB into a
# MongoDB collection.

import os
import csv

from pymongo import MongoClient

db = MongoClient().imdbws

root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + '/datasets.imdbws.com/title.principals.tsv'

counter = 0

for row in csv.DictReader(open(path), delimiter='\t', quoting=csv.QUOTE_NONE):
    if db.titles.find_one({'_id': row['tconst']}):
        row['principalCast'] = row['principalCast'].split(',')
        db.titles.update_one({'_id': row['tconst']}, {'$set':
                             {'principalCast': row['principalCast']}})

        counter += 1
        if counter % 10000 == 0:
            print ("{} titles updated.".format(counter))


x = db.titles.update_many({'principalCast': {'$exists': False}},
                          {'$set': {'principalCast': None}})
print("Updated {} titles without principal cast.".format(x.modified_count))
