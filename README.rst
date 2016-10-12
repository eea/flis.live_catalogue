Quick installation
------------------

#. Clone the repository::

    git clone git@github.com:eea/flis.live_catalogue.git
    cd flis.live_catalogue


#. Create & activate a virtual environment::

    virtualenv sandbox
    echo '*' > sandbox/.gitignore
    source sandbox/bin/activate


#. Install prerequisites if missing::

    python2.7 or higher
    apt-get install python-setuptools python-dev
    
    For PostgreSQL database:
    apt-get install postgresql-9.1 postgresql-contrib-9.1 postgresql-server-dev-9.1


#. Install dependencies::

    pip install -r requirements-dev.txt


#. Create local_settings.py ::

    touch live_catalogue/local_settings.py
    # Check local.settings.example for configuration details


#. Set up the Postgresql database::
   
        root # su - postgres;
        postgres $ psql template1
        template1=# CREATE DATABASE live_catalogue WITH ENCODING 'UTF-8';
        template1=# CREATE USER edw WITH PASSWORD 'edw';
        template1=# GRANT ALL PRIVILEGES ON DATABASE live_catalogue TO edw;


#. Create tables::

    ./manage.py createcachetable
    ./manage.py migrate
    
    
#. Install fixtures::

    ./manage.py loaddata live_catalogue/fixtures/*
    ./manage.py load_metadata_fixtures
    ./manage.py sync_remote_models


#. Run tests::

    ./manage.py test

Create a migration after changes in models.py
---------------------------------------------
::

    ./manage.py makemigrations live_catalogue
    ./manage.py migrate


Stuff to run when deploying ::

    ./manage.py migrate
    ./manage.py collectstatic --noinput
