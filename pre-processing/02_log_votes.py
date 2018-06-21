# Movies with a null numVotes have received less than 5 votes. We consider they
# have received 2 votes.

from pymongo import MongoClient

import math

db = MongoClient().imdbws

i = 0
for m in db.titles.find({'log_votes': {'$exists': False}, 'is_subject': True}):
        i += 1
        db.titles.update_one({'_id': m['_id']},
            {'$set': {'log_votes':  math.log(m['numVotes'] or 2)}})
        if i % 1000 == 0:
            print("{} titles updated.".format(i))
