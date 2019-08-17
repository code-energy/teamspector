_dataset = 'imdbws'
experiments = [
    {'id': 0,
     'dataset': _dataset,
     'team': ['producer', 'director'],
     'year_start': 1985,
     'year_end': 1986,
     'filter': {'is_subject': True}},
    {'id': 1,
     'dataset': _dataset,
     'team': ['producer', 'director', 'writer'],
     'year_start': 1985,
     'year_end': 2012,
     'filter': {'is_subject': True}},
]
experiments = dict([(x['id'], x) for x in experiments])
