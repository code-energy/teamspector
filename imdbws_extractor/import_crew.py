# Adds TSV data of crew (writers and directors) from IMDB into a MongoDB
# collection.

import os
import csv

from pymongo import MongoClient

db = MongoClient().imdbws

root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + "/datasets.imdbws.com/title.crew.tsv"

counter = 0

for row in csv.DictReader(open(path), delimiter='\t'):
    if db.movies.find_one({'_id': row['tconst']}):

        if row['directors'] == "\\N":
            row['directors'] = None
        else:
            row['directors'] = row['directors'].split(',')

        if row['writers'] == "\\N":
            row['writers'] = None
        else:
            row['writers'] = row['writers'].split(',')

        db.movies.update({'_id': row['tconst']}, {'$set':
                         {'directors': row['directors'],
                          'writers': row['writers']}})

        counter += 1
        if counter % 10000 == 0:
            print ("{} movies updated.".format(counter))
