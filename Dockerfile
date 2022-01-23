# syntax=docker/dockerfile:1
FROM python:3.8

COPY requirements.txt requirements.txt
RUN pip3 install geopandas googlemaps matplotlib

COPY /out /out
COPY /visualizer.py /visualizer.py
RUN python3 visualizer.py

CMD tail -f /dev/null
