from tqdm import tqdm
from pymongo import MongoClient

db = MongoClient().imdbws

db.titles.create_index('is_subject')

all_docs = db.titles.find({'is_subject': {'$exists': False}})
total = all_docs.count()

for m in tqdm(all_docs, total=total):
        is_subject = True
        if not m['startYear']:
            is_subject = False
        if m['titleType'] != 'movie':
            is_subject = False
        if m['isAdult']:
            is_subject = False

        db.titles.update_one({'_id': m['_id']},
                             {'$set': {'is_subject':  is_subject}})
