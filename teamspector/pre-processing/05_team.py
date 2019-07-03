# Creates a new "team" field with ids from all movie's team members.

from pymongo import MongoClient

db = MongoClient().imdbws

db.titles.create_index('team')

i = 0
for m in db.titles.find({'team': {'$exists': False}, 'is_subject': True}):
        i += 1
        # FIXME: when missing data, these should already be empty lists.
        team = m['directors'] or []
        team += m['writers'] or []
        team += [x['nconst'] for x in m['principals']]
        team = list(set(team))
        db.titles.update_one({'_id': m['_id']}, {'$set': {'team':  team}})
        if i % 1000 == 0:
            print("{} titles updated.".format(i))
