# syntax=docker/dockerfile:1
FROM python:3.8

RUN pip3 install geopandas googlemaps matplotlib

COPY / /

CMD tail -f /dev/null
