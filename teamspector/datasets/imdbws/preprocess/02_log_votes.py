# Movies with a null numVotes have received between 0 to 4 votes.
# To keep log_votes continuous, we consider these movies received 4 votes.
import math
import logging

from tqdm import tqdm
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__.split("/")[-1])
logger.info("Adding logarithm of number of votes for each movie…")

db = MongoClient().imdbws
q = {'log_votes': {'$exists': False}, 'is_subject': True}
docs = db.productions.find(q)
for m in tqdm(docs, total=docs.count_documents()):
    v = math.log(m['numVotes'] or 4)
    db.productions.update_one({'_id': m['_id']}, {'$set': {'log_votes': v}})
