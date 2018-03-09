To download files from IMDb and extract data to MongoDB:

    $ mkdir datasets.imdbws.com
    $ wget -q -P datasets.imdbws.com -i files.txt
    $ gunzip datasets.imdbws.com/*.gz
    $ python titles.py && python crew.py && python ratings.py && \
    $ python principals.py && python names.py
