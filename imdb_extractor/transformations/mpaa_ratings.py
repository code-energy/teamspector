# -*- coding: utf-8 -*-

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


counter = 0
total_counter = 0
cur.execute("SELECT id FROM title WHERE kind_id = 1")

while True:
    row = cur.fetchone()
    if not row:
        break

    total_counter += 1
    if total_counter % 1000 == 0:
        print total_counter

    if db.movies.find_one({'_id': row[0], '$or': [
        {'mpaa': {'$exists': False}}, {'certificates': {'$exists': False}}
            ]}):

        m = ia.get_movie(row[0])
        ia.update(m)
        mpaa = m['mpaa'] if 'mpaa' in m.keys() else None
        certificates = m['certificates'] if 'certificates' in m.keys() else []

        db.movies.update({'_id': m.getID()},
                {'$set': {'mpaa': mpaa, 'certificates': certificates}})

conn.close()
