# -*- coding: utf-8 -*-

# Adds a weighted rating field based on the Bayesian estimate used by iMDB.
#
# weighted rating (WR) = (v ÷ (v+m)) × R + (m ÷ (v+m)) × C
# Where:
# R = average for the movie (mean) = (Rating)
# v = number of votes for the movie = (votes)
# m = min votes required for significance
# C = mean vote across the whole report (currently 7.0)

from pymongo import MongoClient
client = MongoClient()
db = client.imdb


m = 2500
C = 7.0


for mov in db.movies.find({'nrating': {'$exists': False}}):
    v = mov['votes']
    R = mov['rating']

    wr = float((R * v) + (C * m))/(v + m)

    db.movies.update({'_id': mov['_id']}, {'$set': {'nrating': wr}})
