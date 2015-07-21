# Pyhton image

FROM python:2.7-slim

# System requirements

RUN apt-get -y update && apt-get -y install \
    gcc \
    python-setuptools \
    python-dev \
    python-mysqldb \
    libxml2-dev \
    libxslt1-dev \
    lib32z1-dev \
    libpq-dev \
    libldap2-dev \
    libsasl2-dev \
    libmysqlclient-dev

# Copy code into image

RUN mkdir flis.live_catalogue
COPY . /flis.live_catalogue
WORKDIR flis.live_catalogue

# Install requirements

RUN pip install -U setuptools
RUN pip install -r requirements-dev.txt
COPY live_catalogue/local_settings.py.example live_catalogue/local_settings.py

# Expose needed port

EXPOSE 8000

#Default command

CMD python ./manage.py runserver 0.0.0.0:8000
