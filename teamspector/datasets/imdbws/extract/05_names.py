# Converts TSV data from IMDB for crew into a MongoDB collection.

import os
import csv
import logging

from tqdm import tqdm
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__.split("/")[-1])
logger.info("Extracting movie participants' from CSV to a MongoDB collection…")

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

    db.participants.insert_one(c)
