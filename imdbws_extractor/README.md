- Download the CSV data from IMDB and extract the files:

    $ mkdir datasets.imdbws.com
    $ wget -q -P datasets.imdbws.com -i files.txt
    $ gunzip datasets.imdbws.com/*.gz
    $ python import_titles.py && python import_crew.py && \
      python import_ratings.py && python import_principals && \
      python import_names
    $ python add_log_votes.py && python add_normalized_ratings.py
