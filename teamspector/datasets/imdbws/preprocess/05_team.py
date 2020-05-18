# Creates a new "team_size" field with the length of "team".
# TODO: do we really need this? Check.
import logging

from tqdm import tqdm
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__.split("/")[-1])
logger.info("Calculating total team size for each movie…")

db = MongoClient().imdbws
q = {'team_size': {'$exists': False}, 'is_subject': True}
docs = db.productions.find(q)
for m in tqdm(docs, total=docs.count()):
    size = len(m['team'])
    db.productions.update_one({'_id': m['_id']}, {'$set': {'team_size': size}})
