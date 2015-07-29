FROM eeacms/python:2.7-slim

# Copy code into image

RUN mkdir flis.live_catalogue
COPY . /flis.live_catalogue
WORKDIR flis.live_catalogue

# Install requirements

RUN pip install -U setuptools
RUN pip install -r requirements-dev.txt
COPY live_catalogue/local_settings.py.example live_catalogue/local_settings.py

# Expose needed port

EXPOSE 8002 

# Expose static volume

VOLUME live_catalogue/static/

#Default command

CMD python ./manage.py runserver 0.0.0.0:8002
