from pymongo import MongoClient

import math

db = MongoClient().imdbws

i = 0
for m in db.titles.find({'log_votes': {'$exists': False},
                         'numVotes': {'$ne': None}}):
        i += 1
        db.titles.update_one({'_id': m['_id']},
            {'$set': {'log_votes':  math.log(m['numVotes'])}})
        if i % 1000 == 0:
            print("{} titles updated.".format(i))

x = db.titles.update_many({'numVotes': None}, {'$set': {'log_votes': None}})
print("Updated {} titles without ratings.".format(x.modified_count()))
