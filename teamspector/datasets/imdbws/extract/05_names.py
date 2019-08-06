# Converts TSV data from IMDB for crew into a MongoDB collection.

import os
import csv

from tqdm import tqdm
from pymongo import MongoClient

db = MongoClient().imdbws

root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + "/../raw/name.basics.tsv"
total = sum(1 for i in open(path, 'rb'))
all_rows = csv.DictReader(open(path), delimiter='\t', quoting=csv.QUOTE_NONE)

for row in tqdm(all_rows, total=total):
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

    db.crew.save(c)
