FROM eeacms/python:2.7-slim

# Copy code into image

RUN mkdir live_catalogue
COPY requirements.txt requirements-dev.txt requirements-dep.txt /live_catalogue/
WORKDIR live_catalogue

# Install requirements

RUN pip install -U setuptools
RUN pip install -r requirements-dev.txt

COPY . /live_catalogue
COPY live_catalogue/local_settings.py.example live_catalogue/local_settings.py

# Expose needed port

EXPOSE 8002 

# Expose static volume

VOLUME live_catalogue/public/static/

#Default command

CMD gunicorn live_catalogue.wsgi:application --bind 0.0.0.0:8002