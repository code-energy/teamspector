import logging

from tqdm import tqdm
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__.split("/")[-1])
logger.info("Selecting movies that are experiment subjects…")

db = MongoClient().imdbws

db.productions.create_index('is_subject')

all_docs = db.productions.find({'is_subject': {'$exists': False}})
for m in tqdm(all_docs, total=all_docs.count_documents():
    is_subject = True
    if not m['startYear']:
        is_subject = False
    if m['titleType'] != 'movie':
        is_subject = False
    if m['isAdult']:
        is_subject = False

    db.productions.update_one({'_id': m['_id']},
                              {'$set': {'is_subject':  is_subject}})
