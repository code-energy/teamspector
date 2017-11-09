# -*- coding: utf-8 -*-

# Add genre information as a dictionary.

from pymongo import MongoClient
db = MongoClient().imdb

genres = ['action', 'adventure', 'animation', 'biography', 'comedy', 'crime',
'documentary', 'drama', 'family', 'fantasy', 'history', 'horror',
'music', 'musical', 'mystery', 'romance', 'sci_fi', 'sport', 'thriller', 'war',
'western']


t = lambda x: x.lower().replace('-', '_')

for m in db.movies.find({'fgenre': {'$exists': False}}):

    fgenres = {}

    for g in genres:
        if g in map(t, m.get('genres') or []):
            fgenres[g] = 1
        else:
            fgenres[g] = 0

    db.movies.update({'_id': m['_id']},
                     {'$set': {'fgenre': fgenres}})
