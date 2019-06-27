This software isn't installed, it's run as a script on the fly. But to run it,
you'll need to have MongoDB and Python dependencies installed.

# MongoDB
Make sure MongoDB 4.x is installed and its daemon is running in your system. Do
to it with Mac OS X and Macports,

    $ sudo port install mongodb

# Python
Ensure you have all dependencies in `requirements.txt` installed in a dedicated
python virtual environment. You can use `virtualenvwrapper` to create your
virtual environment. To install it,

    $ sudo pip install virtualenvwrapper
    $ mkdir ~/.virtualenvs

Then add these two lines to your `~/.profile` file:

    export WORKON_HOME=~/.virtualenvs
    source virtualenvwrapper.sh

After you restart your shell session, `virtualenvwrapper` should be available.
You can create a new virtual environment with

    $ mkvirtualenv teamspector

After the environment has been created, activate it

    $ workon teamspector

After the virtual environment is active, install the dependencies by running

    (teamspector) $ pip install -r requirements.txt

<!-- vim: set fdm=marker textwidth=79 colorcolumn=80: -->
