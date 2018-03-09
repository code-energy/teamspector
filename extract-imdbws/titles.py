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
    t = {}
    for k, v in row.items():
        if v == "\\N":
            v = None
        if k == "tconst":
            k = "_id"
        if k in ["originalTitle", "endYear"]:
            continue
        t[k] = v
    if t['runtimeMinutes']:
        t['runtimeMinutes'] = int(t['runtimeMinutes'])

    if t['startYear']:
        t['startYear'] = int(t['startYear'])

    if t['genres']:
        t['genres'] = t['genres'].split(',')

    counter += 1
    if counter % 10000 == 0:
        print ("{} titles inserted.".format(counter))

    db.titles.save(t)
