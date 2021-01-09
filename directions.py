import requests
import json
import csv

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
#     base_url + "origin=place_id:" + uoft_place_id + "&destination=" + test_latlong +
#     "&mode=" + mode + "&key=" + api_key)
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
        return get_shortest_duration(json_output)


def get_biking(origin: str, destination: str) -> int:
    """Get duration of shortest bicycling route between origin and destination (if it exists)."""
    mode = "bicycling"
    request = requests.get(
        base_url + "origin=place_id:" + origin + "&destination=" + destination + "&mode=" + mode + "&key=" + api_key)
    json_output = request.json()
    if json_output["status"] == "ZERO_RESULTS":
        return -1
    else:
        return get_shortest_duration(json_output)


def get_transit(origin: str, destination: str) -> int:
    """Get duration of shortest transit route between origin and destination (if it exists)."""
    mode = "transit"
    request = requests.get(
        base_url + "origin=place_id:" + origin + "&destination=" + destination + "&mode=" + mode + "&key=" + api_key)
    json_output = request.json()
    if json_output["status"] == "ZERO_RESULTS":
        return -1
    else:
        return get_shortest_duration(json_output)


def get_driving(origin: str, destination: str) -> int:
    """Get duration of shortest driving route between origin and destination (if it exists)."""
    mode = "driving"
    request = requests.get(
        base_url + "origin=place_id:" + origin + "&destination=" + destination + "&mode=" + mode + "&key=" + api_key)
    json_output = request.json()
    if json_output["status"] == "ZERO_RESULTS":
        return -1
    else:
        return get_shortest_duration(json_output)


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


def record_durations(origin: str, input_file: str, output_file: str) -> None:
    """Record the durations of the shortest trips using each mode of transport from origin to the destinations
    stored in the rows of the input_file by writing the durations corresponding to each destination into the
    output file. BOTH input_file AND output_file MUST BE EXISTING .CSV FILES."""
    with open(input_file) as csv_in:
        csv_reader = csv.reader(csv_in)
        line_count = 0
        with open(output_file, 'w', newline='') as csv_out:
            csv_writer = csv.writer(csv_out)
            csv_writer.writerow(['TRACTID', 'LONGITUDE', 'LATITUDE', 'WALK', 'BIKE', 'TRANSIT', 'DRIVE', 'SHORTEST'])
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    tract_id = row[0]
                    long = row[1]
                    lat = row[2]
                    destination = lat + "," + long
                    durations = all_transport_modes(origin, destination)
                    walk, bike, transit, drive = durations
                    for i in range(0, len(durations)):
                        if min(durations) == durations[i]:
                            shortest = i
                    full_row = tract_id, long, lat, walk, bike, transit, drive, shortest
                    csv_writer.writerow(full_row)


record_durations(uoft_place_id, "sample_centroids.csv", "sample_durations.csv")

# TODO: verify travel times of remaining entries in sample_durations.csv (4 complete)
# TODO: test dataframe merge and map visualizer with sample dataframe before applying to full dataset
# TODO: remember to record distinction between Toronto metropolitan area and core city when producing the map, either
#  by cropping the map image or feeding the code a modified input file containing the relevant subset of census tracts
# TODO: adjust order of longitude, latitude to latitude, longitude in centroid and duration .csv files
# TODO: add 12 mins of driving time to get_driving as adjustment for having to find parking and walking to destination
# TODO: add comments to directions.py inline with code to explain complex chunks
# TODO: extract code in data_formatter.py to form proper methods and functions with documentation and inline comments
