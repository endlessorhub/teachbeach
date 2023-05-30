FROM python:3.7

ENV UPDATED_AT 2019-02-17

RUN apt-get update && apt-get install -y --no-install-recommends \
	gdal-bin && rm -rf /var/lib/apt/lists/*

# Install app requirements
COPY requirements.txt /home/docker/code/
RUN pip install -r /home/docker/code/requirements.txt --default-timeout=1000

# Install the app code
COPY . /home/docker/code/

# Make manage.py more convenient to run
RUN ln -s /home/docker/code/manage.py /manage.py

# Finish up
WORKDIR /home/docker/code
