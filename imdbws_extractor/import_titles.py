# Converts TSV data from IMDB into a MongoDB collection.

#import operator
#from functools import reduce
#from datetime import datetime

#from dateutil import parser

import os
import csv

from pymongo import MongoClient

db = MongoClient().imdbws

root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + "/datasets.imdbws.com/title.basics.tsv"

counter = 0

for row in csv.DictReader(open(path), delimiter='\t'):
    if row['titleType'] == 'movie' and row['isAdult'] == '0':
        m = {}
        for k, v in row.items():
            if v == "\\N":
                v = None
            if k == "tconst":
                k = "_id"
            if k in ["originalTitle", "titleType", "isAdult", "endYear"]:
                continue
            m[k] = v
        if m['runtimeMinutes']:
            m['runtimeMinutes'] = int(m['runtimeMinutes'])

        if m['startYear']:
            m['startYear'] = int(m['startYear'])

        if m['genres']:
            m['genres'] = m['genres'].split(',')

        counter += 1
        if counter % 10000 == 0:
            print ("{} movies inserted.".format(counter))

        db.movies.save(m)
