import requests
import json

uoft_place_id = "ChIJm_0x87g0K4gR93ZadrabHY0"
union_station_place_id = "ChIJKQDzOA41K4gRajQDdyzD990"
pearson_airport_place_id = "ChIJkdQtwEo5K4gRxQ4DxOldHbQ"
api_key = "AIzaSyA06s0IARgjGwG2kv6KpRjlQGyrBOdUgCM"
request_base = "https://maps.googleapis.com/maps/api/directions/json?"

test_longitude = "-79.4272866628539"
test_latitude = "43.8781931250116"
test_latlong = test_latitude + "," + test_longitude
mode = "bicycling"

request = requests.get(
   request_base + "origin=place_id:" + uoft_place_id + "&destination=" + test_latlong + "&mode=" + mode + "&key=" + api_key)
seconds = request.json()["routes"][0]["legs"][0]["duration"]["value"]
minutes = seconds/60
print(f'This trip will take {minutes} minutes when {mode}.')
