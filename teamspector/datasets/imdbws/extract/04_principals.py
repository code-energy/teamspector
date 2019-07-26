# Adds TSV data of principals (key people of movie's crew) from IMDB into a
# MongoDB collection.

import os
import csv

from pymongo import MongoClient

db = MongoClient().imdbws

root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + '/../raw/title.principals.tsv'

counter = 0


for row in csv.DictReader(open(path), delimiter='\t', quoting=csv.QUOTE_NONE):
    if db.titles.find_one({'_id': row['tconst']}):
        principal = {'ordering': int(row['ordering']),
                     'nconst': row['nconst'],
                     'category': row['category'],
                     'job': None if row['job'] == r'\N' else row['job']}
        db.titles.update_one({'_id': row['tconst']}, {'$push':
                             {'principals': principal}})

        counter += 1
        if counter % 10000 == 0:
            print("{} titles updated.".format(counter))


x = db.titles.update_many({'principals': {'$exists': False}},
                          {'$set': {'principals': []}})
print("Updated {} titles without principal cast.".format(x.modified_count))
