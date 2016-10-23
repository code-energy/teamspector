This directory contains all the .gz files from IMDB, the Sqlite database
generated with imdbpy2sql.py, and the scripts to generate the MongoDB database
with all data required for the experiments. Below are instructions to get the
IMDb database from its source and convert it to the MongoDB collection:


0. The IMDBpy python package only works on Python2. We should create a python2
   virtualenv and install py2 dependencies there:

    $ virtualenv --python=/usr/bin/python2.7 virtualenv
    $ source virtualenv/bin/activate
    $ pip install -r imdb-extraction-reqs.txt

1. Download the .gz files from IMDb. It should be ~1.5 GB of data.

    $ mkdir temp.gz && cd temp.gz
    $ wget -r --accept="*.gz" --no-directories --no-host-directories \
      --level 1 ftp://ftp.fu-berlin.de/pub/misc/movies/database/

2. Use the .gz files to generate an Sqlite database. It should take about 45
   minutes using an SSD hard disk.

    $ cd ..
    $ python imdbpy2sql.py -u \
      sqlite:<path to root project>/imdb_raw_data/imdb.sqlite \
      -d temp.gz --sqlite-transactions

3. Create indexes in the most important columns of the Sqlite database.

    $ sqlite3 imdb.sqlite
    > CREATE INDEX title_idx on title (kind_id);
    > CREATE INDEX movie_info_idx on movie_info_idx (movie_id,info_type_id);

4. Generate the MongoDB database. Let it run overnight:

    $ python parse_movie_data.py

5. Generate indexes for the "release" key, as we'll sort movies by it:

    $ mongo imdb --eval "db.movies.ensureIndex({release:1, _id:1})"
    $ mongo imdb --eval "db.movies.ensureIndex({'team.full':1})"

6. Normalize IMDBs ratings:

    $ python normalize_ratings.py

Now we still need to normalize gross.

    #TODO

<!-- vim: set fdm=marker textwidth=79 colorcolumn=80: -->
