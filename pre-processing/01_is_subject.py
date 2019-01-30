from pymongo import MongoClient

db = MongoClient().imdbws

i = 0
for m in db.titles.find({'is_subject': {'$exists': False}}):
        i += 1
        is_subject = True
        if not m['startYear']:
            is_subject = False
        if m['titleType'] != 'movie':
            is_subject = False
        if m['isAdult']:
            is_subject = False

        db.titles.update_one({'_id': m['_id']},
                             {'$set': {'is_subject':  is_subject}})

        if i % 1000 == 0:
            print("{} titles updated.".format(i))

db.titles.create_index('is_subject')
