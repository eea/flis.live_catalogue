Quick installation
------------------

1. Clone the repository::

    git svn clone https://svn.eionet.europa.eu/repositories/Python/flis.live_catalogue/
    cd flis.live_catalogue


2. Create & activate a virtual environment::

    virtualenv sandbox
    echo '*' > sandbox/.gitignore
    source sandbox/bin/activate


3. Install prerequisites if missing::
    python2.7 or higher
    apt-get install python-setuptools python-dev
    For MySQL database:
    apt-get install mysql-client-5.5 mysql-common mysql-server-5.5
    For PostgreSQL database:
    apt-get install postgresql-9.1 postgresql-contrib-9.1 postgresql-server-dev-9.1


4. Install dependencies::

    pip install -r requirements-dev.txt


5. Create a instance folder::
     mkdir -p instance


6. Create local_settings.py ::
    touch live_catalogue/live_catalogue/local_settings.py
     # Check local.settings.example for configuration details


7. Set up the :
   a. MySQL database
    mysql > CREATE SCHEMA live_catalogue CHARACTER SET utf8 COLLATE utf8_general_ci;
   b. Postgresql database::
    root # su - postgres;
    postgres $ psql template1
    template1=# CREATE DATABASE live_catalogue WITH ENCODING 'UTF-8';
    template1=# CREATE USER edw WITH PASSWORD 'edw';
    template1=# GRANT ALL PRIVILEGES ON DATABASE live_catalogue TO edw;

8. Create tables ::
    ./manage.py syncdb
    ./manage.py createcachetable
    ./manage.py migrate


9. Run tests ::
    ./manage.py test

Create a migration after changes in models.py
---------------------------------------------
::
    ./manage.py schemamigration live_catalogue --auto
    ./manage.py migrate


Stuff to run when deploying ::
    ./manage.py syncdb
    ./manage.py migrate
    ./manage.py collectstatic --noinput
