# MongoDB
This software needs MongoDB 4.x running in your system. In Mac OS X, it can be
installed with Macports:

    $ sudo port install mongodb

# Python
It's best to install Teamspector in its own python virtual environment. You can
use `virtualenvwrapper` to create a virtual environment. If you don't already
have it,

    $ sudo pip install virtualenvwrapper
    $ mkdir ~/.virtualenvs

Then add these two lines to your `~/.profile` file:

    export WORKON_HOME=~/.virtualenvs
    source virtualenvwrapper.sh

After you restart your shell session, `virtualenvwrapper` and its commands
should be available. Create a new virtual environment with

    $ mkvirtualenv teamspector

After the environment has been created, activate it

    $ workon teamspector

After the virtual environment is active, install the package with its
dependencies by running

    (teamspector) $ pip install -e .

<!-- vim: set fdm=marker textwidth=79 colorcolumn=80: -->
