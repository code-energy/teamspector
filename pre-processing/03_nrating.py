# Adds a weighted rating field based on the Bayesian estimate used by iMDB.
#
# weighted rating (WR) = (v ÷ (v+m)) × R + (m ÷ (v+m)) × C
# Where:
# R = average for the movie (mean) = (Rating)
# v = number of votes for the movie = (votes)
# m = min votes required for significance (IMDb uses 25,000)
# C = mean vote across the whole report (currently 7.0)

from pymongo import MongoClient

client = MongoClient()

db = client.imdbws

m = 25000
C = 7.0

i= 0
for mov in db.titles.find({'nrating': {'$exists': False}, 'is_subject': True}):
    i += 1
    v = mov['numVotes'] or 2
    if mov['averageRating']:
        R = float(mov['averageRating'].to_decimal())
    else:
        R = C

    wr = float((R * v) + (C * m))/(v + m)

    db.titles.update({'_id': mov['_id']}, {'$set': {'nrating': wr}})
    if i % 1000 == 0:
        print("{} titles updated.".format(i))
