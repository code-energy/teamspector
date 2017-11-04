# -*- coding: utf-8 -*-

# This will get movie information form the Sqlite database generated by
# imdb2sql.py and record the relevant information into a MongoDB collection.

import os
from datetime import datetime

import sqlite3
from dateutil import parser

from imdb import IMDb
from pymongo import MongoClient

root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + "/../imdb.sqlite"
conn = sqlite3.connect(path)
cur = conn.cursor()

ia = IMDb('sql', uri='sqlite://'+path)

db = MongoClient().imdb


def movie_is_valid(movie):
    if not all(x in m.keys() for x in ['rating', 'votes']):
        return False

    if len(movie_full_team(get_movie_team(movie))) < 2:
        return False

    return True


def get_movie_runtime(m):
    if 'runtimes' in m.keys():
        runtime = m['runtime'][0]
        print runtime

        if '::' in runtime:
            runtime = runtime.split('::')[0]

        if ':' in runtime:
            runtime = runtime.split(':')[1]

        if '.' in runtime:
            runtime = runtime.split('.')[0]

        if '-' in runtime:
            runtime = runtime.split('-')[0]

        if ',' in runtime:
            runtime = runtime.split(',')[0]

        if ' ' in runtime:
            runtime = runtime.split(' ')[0]

        if '\'' in runtime:
            runtime = runtime.split('\'')[0]

        if '\"' in runtime:
            runtime = runtime.split('\"')[0]

        if 'm' in runtime:
            runtime = runtime.split('m')[0]

        if '\\' in runtime:
            runtime = runtime.split('\\')[0]

        if '/' in runtime:
            runtime = runtime.split('/')[0]

        if runtime == '':
            return 0

        print runtime
        print int(runtime)
        print '---------------------'
        return int(runtime)

    return None

counter = 0
total_counter = 0
cur.execute("SELECT id FROM title WHERE kind_id = 1")

while True:
    row = cur.fetchone()
    if not row:
        break

    total_counter += 1
    if total_counter % 100 == 0:
        print total_counter

    if db.movies.find_one({'_id': row[0], 'runtime': {'$exists': False}}):
        m = ia.get_movie(row[0])

        db.movies.update({'_id': m.getID()},
                         {'$set': {'runtime':  get_movie_runtime(m)}})
conn.close()
