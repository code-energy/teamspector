# Converts TSV data from IMDB into a MongoDB collection.

import os
import csv

from tqdm import tqdm
from pymongo import MongoClient, ASCENDING

db = MongoClient().imdbws
db.titles.create_index([('startYear', ASCENDING), ('_id', ASCENDING)])


root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + "/../raw/title.basics.tsv"
total = sum(1 for i in open(path, 'rb'))
all_rows = csv.DictReader(open(path), delimiter='\t', quoting=csv.QUOTE_NONE)


for row in tqdm(all_rows, total=total):
    t = {}
    for k, v in row.items():
        if v == '\\N':
            v = None
        if k == 'tconst':
            k = '_id'
        if k == 'isAdult':
            v = True if v == '1' else False
        if k in ["originalTitle", "endYear"]:
            continue
        t[k] = v

    if t['runtimeMinutes']:
        t['runtimeMinutes'] = int(t['runtimeMinutes'])

    if t['startYear']:
        t['startYear'] = int(t['startYear'])

    if t['genres']:
        t['genres'] = t['genres'].split(',')

    db.titles.save(t)
