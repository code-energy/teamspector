# Adds TSV data of crew (writers and directors) from IMDB into a MongoDB
# collection.

import os
import csv

from pymongo import MongoClient

db = MongoClient().imdbws

root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + "/../raw/title.crew.tsv"

counter = 0

for row in csv.DictReader(open(path), delimiter='\t', quoting=csv.QUOTE_NONE):
    if db.titles.find_one({'_id': row['tconst']}):

        if row['directors'] == "\\N":
            row['directors'] = None
        else:
            row['directors'] = row['directors'].split(',')

        if row['writers'] == "\\N":
            row['writers'] = None
        else:
            row['writers'] = row['writers'].split(',')

        db.titles.update_one({'_id': row['tconst']}, {'$set':
                             {'directors': row['directors'],
                              'writers': row['writers']}})

        counter += 1
        if counter % 10000 == 0:
            print("{} titles updated.".format(counter))


x = db.titles.update_many({'directors': {'$exists': False}},
                          {'$set': {'directors': None}})
print("Updated {} titles without directors.".format(x.modified_count))

x = db.titles.update_many({'writers': {'$exists': False}},
                          {'$set': {'writers': None}})
print("Updated {} titles without writers.".format(x.modified_count))
