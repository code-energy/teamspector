# Converts TSV data from IMDB for crew into a MongoDB collection.

import os
import csv

from pymongo import MongoClient

db = MongoClient().imdbws

root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + "/../raw/name.basics.tsv"

counter = 0

for row in csv.DictReader(open(path), delimiter='\t', quoting=csv.QUOTE_NONE):
    c = {}
    for k, v in row.items():
        if v == "\\N":
            v = None
        if k == "nconst":
            k = "_id"
        c[k] = v
    if c['birthYear']:
        c['birthYear'] = int(c['birthYear'])

    if c['deathYear']:
        c['deathYear'] = int(c['deathYear'])

    if c['primaryProfession']:
        c['primaryProfession'] = c['primaryProfession'].split(',')

    if c['knownForTitles']:
        c['knownForTitles'] = c['knownForTitles'].split(',')

    counter += 1
    if counter % 10000 == 0:
        print("{} crew inserted.".format(counter))

    db.crew.save(c)
