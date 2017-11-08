# -*- coding: utf-8 -*-

# This will create a new field indicating the countries in which the movie
# production took place, and the continents in which those countries are.

from pymongo import MongoClient
db = MongoClient().imdb

import json

codes = json.load(open('country_codes.json'))

countries = {x['name'].split(',')[0]: x['alpha-3'] for x in codes}
countries['USA'] = 'USA'
countries['UK'] = 'GBR'
countries['Russia'] = 'RUS'
countries['West Germany'] = 'DEU'
countries['East Germany'] = 'DEU'
countries['South Korea'] = 'KOR'
countries['Soviet Union'] = 'RUS'
countries['Republic of Macedonia'] = countries['Macedonia']
countries['Yugoslavia'] = countries['Macedonia']
countries['Federal Republic of Yugoslavia'] = countries['Macedonia']
countries['Vietnam'] = countries['Viet Nam']
countries['Czechoslovakia'] = countries['Czech Republic']
countries['Palestinian Territory'] = countries['Palestine']
countries['Occupied Palestinian Territory'] = countries['Palestinian Territory']
countries['Serbia and Montenegro'] = countries['Serbia']
countries['Kosovo'] = countries['Serbia']
countries['Syria'] = countries['Syrian Arab Republic']
countries['Democratic Republic of the Congo'] = countries['Congo']
countries['Ivory Coast'] = 'CIV'
countries['North Korea'] = 'PRK'
countries['U.S. Virgin Islands'] = 'VIR'
countries['Laos'] = 'LAO'
countries['Reunion'] = 'FRA'
countries['Burma'] = countries['Myanmar']
countries['Netherlands Antilles'] = 'CUW'
countries['Zaire'] = countries['Congo']
countries['North Vietnam'] = countries['Vietnam']
countries['Federated States of Micronesia'] = countries['Micronesia']

for m in db.movies.find({'country_codes': {'$exists': False}}):
    x = []

    for c in m['country'] or []:
        x.append(countries[c])

    db.movies.update({'_id': m['_id']},
                     {'$set': {'country_code': x}})

def get_cont(c):
    if c['name'] in ['Antarctica', 'Bouvet Island',
                     'French Southern Territories',
                     'Heard Island and McDonald Islands',
                     'South Georgia and the South Sandwich Islands']:
        return None

    if c['name'] in ['British Indian Ocean Territory']:
        return 'Asia'

    if c['name'] in ['United States Minor Outlying Islands']:
        return 'North America'

    if c['name'] in ['Christmas Island', 'Cocos (Keeling) Islands']:
        return 'Oceania'

    if c['region-code'] == '142':
        return "Asia"
    if c['region-code'] == '002':
        return "Africa"
    if c['region-code'] == '019':
        if c['sub-region-code'] == '021':
            return "North America"
        else:
            return "Latin America"
    if c['region-code'] == '150':
        return "Europe"
    if c['region-code'] == '009':
        return "Oceania"

cont = {x['alpha-3']: get_cont(x) for x in codes}
code = {x['alpha-3']: x for x in codes}


for m in db.movies.find({'continent': {'$exists': False}}):
    x = []

    for c in m['country_code']:
        x.append(get_cont(code[c]))

    continents = { 'Africa' : 'Africa' in x,
                   'Asia': 'Asia' in x,
                   'Europe': 'Europe' in x,
                   'Oceania': 'Oceania' in x,
                   'North America': 'North America' in x,
                   'Latin America': 'Latin America' in x}

    db.movies.update({'_id': m['_id']},
                     {'$set': {'continent': continents}})
