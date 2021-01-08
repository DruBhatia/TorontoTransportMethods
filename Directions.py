import requests
import json

uoft_place_id = "ChIJm_0x87g0K4gR93ZadrabHY0"
union_station_place_id = "ChIJKQDzOA41K4gRajQDdyzD990"
pearson_airport_place_id = "ChIJkdQtwEo5K4gRxQ4DxOldHbQ"
api_key = "AIzaSyA06s0IARgjGwG2kv6KpRjlQGyrBOdUgCM"
base_url = "https://maps.googleapis.com/maps/api/directions/json?"

# test_longitude = "-79.4272866628539"
# test_latitude = "43.8781931250116"
# test_latlong = test_latitude + "," + test_longitude
# mode = "bicycling"

# request = requests.get(
#     base_url + "origin=place_id:" + uoft_place_id + "&destination=" + test_latlong + "&mode=" + mode + "&key=" + api_key)
# seconds = request.json()["routes"][0]["legs"][0]["duration"]["value"]
# minutes = seconds / 60
# print(f'This trip will take {minutes} minutes when {mode}.')
# # print(request.json())
# a = request.json()
# for k, v in a.items():
#     print(k, v)


def get_duration(route) -> int:
    """Get duration of this route."""
    return route["legs"][0]["duration"]["value"]


def get_shortest_duration(json_output) -> int:
    """Get the duration of the shortest route from json_output"""
    duration = min(get_duration(route) for route in json_output["routes"] if get_duration(route) >= 0)
    return duration


def get_walking(origin: str, destination: str) -> int:
    """Get duration of shortest walking route between origin and destination (if it exists)."""
    mode = "walking"
    request = requests.get(
        base_url + "origin=place_id:" + origin + "&destination=" + destination + "&mode=" + mode + "&key=" + api_key)
    json_output = request.json()
    if json_output["status"] == "ZERO_RESULTS":
        return -1
    else:
        get_shortest_duration(json_output)


def get_biking(origin: str, destination: str) -> int:
    """Get duration of shortest bicycling route between origin and destination (if it exists)."""
    mode = "bicycling"
    request = requests.get(
        base_url + "origin=place_id:" + origin + "&destination=" + destination + "&mode=" + mode + "&key=" + api_key)
    json_output = request.json()
    if json_output["status"] == "ZERO_RESULTS":
        return -1
    else:
        get_shortest_duration(json_output)


def get_transit(origin: str, destination: str) -> int:
    """Get duration of shortest transit route between origin and destination (if it exists)."""
    mode = "transit"
    request = requests.get(
        base_url + "origin=place_id:" + origin + "&destination=" + destination + "&mode=" + mode + "&key=" + api_key)
    json_output = request.json()
    if json_output["status"] == "ZERO_RESULTS":
        return -1
    else:
        get_shortest_duration(json_output)


def get_driving(origin: str, destination: str) -> int:
    """Get duration of shortest driving route between origin and destination (if it exists)."""
    mode = "driving"
    request = requests.get(
        base_url + "origin=place_id:" + origin + "&destination=" + destination + "&mode=" + mode + "&key=" + api_key)
    json_output = request.json()
    if json_output["status"] == "ZERO_RESULTS":
        return -1
    else:
        get_shortest_duration(json_output)


def all_transport_modes(origin: str, destination: str) -> list:
    """Get the duration of the shortest trip between origin and destination
    using each mode of transport: walking, biking, transit, driving."""
    durations = [
        get_walking(origin, destination),
        get_biking(origin, destination),
        get_transit(origin, destination),
        get_driving(origin, destination),
        ]
    return durations

