# Movies with a null numVotes have received between 0 to 4 votes.
# To keep log_votes continuous, we consider these movies received 4 votes.
import math

from tqdm import tqdm
from pymongo import MongoClient

db = MongoClient().imdbws

docs = db.titles.find({'log_votes': {'$exists': False}, 'is_subject': True})
total = docs.count()

for m in tqdm(docs, total=total):
    v = math.log(m['numVotes'] or 4)
    db.titles.update_one({'_id': m['_id']}, {'$set': {'log_votes': v}})
