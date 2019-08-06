# Creates a new "team_size" field with the length of "team".
# TODO: do we really need this? Check.

from tqdm import tqdm
from pymongo import MongoClient

db = MongoClient().imdbws
docs = db.titles.find({'team_size': {'$exists': False}, 'is_subject': True})
for m in tqdm(docs, total=docs.count()):
    team_size = len(m['team'])
    db.titles.update_one({'_id': m['_id']}, {'$set': {'team_size': team_size}})
