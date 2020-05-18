# Adds a weighted rating field based on the Bayesian estimate that IMDb claimed
# to have used priorly.
#
# weighted rating (WR) = (v ÷ (v+m)) × R + (m ÷ (v+m)) × C
# Where:
# R = average for the movie (mean) = (Rating)
# v = number of votes for the movie = (votes)
# m = min votes required for significance (IMDb uses 25,000)
# C = mean vote across the whole report (currently 7.0)
#
# The minimum number of votes for having an informative normalized rating was
# arbitrarily set at 5,000.
import logging

from tqdm import tqdm
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__.split("/")[-1])
logger.info("Calculating normalized ratings for each movie…")

client = MongoClient()

db = client.imdbws

m = 25000
M = 5000
C = 7.0

docs = db.productions.find({'nrating': {'$exists': False}, 'is_subject': True})
for mov in tqdm(docs, total=docs.count_documents()):
    v = mov['numVotes']
    if v and v >= M:
        R = float(mov['averageRating'].to_decimal())
        wr = float((R * v) + (C * m))/(v + m)
    else:
        wr = None

    db.productions.update_one({'_id': mov['_id']}, {'$set': {'nrating': wr}})
