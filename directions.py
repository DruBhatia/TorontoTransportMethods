import requests
import csv

# IMPORTANT:
# Declare API key, placeIDs of origin nodes, and base URL of HTTP requests to use with Google Maps API
# Make sure the values in this section are up-to-date and accurate to avoid wasted/redundant/unauthorized API calls
uoft_place_id = "ChIJm_0x87g0K4gR93ZadrabHY0"
union_station_place_id = "ChIJKQDzOA41K4gRajQDdyzD990"
pearson_airport_place_id = "ChIJkdQtwEo5K4gRxQ4DxOldHbQ"
api_key = "AIzaSyA06s0IARgjGwG2kv6KpRjlQGyrBOdUgCM"
base_url = "https://maps.googleapis.com/maps/api/directions/json?"


# Testing with sample coordinates and routes
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
    """ Get duration of this route. """
    return route["legs"][0]["duration"]["value"]


def get_shortest_duration(json_output) -> int:
    """ Get the duration of the shortest route from json_output. """
    duration = min(get_duration(route) for route in json_output["routes"] if get_duration(route) >= 0)
    return duration


def get_walking(origin: str, destination: str) -> int:
    """ Get duration of shortest walking route between origin and destination (if it exists). """
    mode = "walking"
    request = requests.get(
        base_url + "origin=place_id:" + origin + "&destination=" + destination + "&mode=" + mode + "&key=" + api_key)
    json_output = request.json()
    if json_output["status"] == "ZERO_RESULTS":
        return 200000
    else:
        return get_shortest_duration(json_output)


def get_biking(origin: str, destination: str) -> int:
    """ Get duration of shortest bicycling route between origin and destination (if it exists). """
    mode = "bicycling"
    request = requests.get(
        base_url + "origin=place_id:" + origin + "&destination=" + destination + "&mode=" + mode + "&key=" + api_key)
    json_output = request.json()
    if json_output["status"] == "ZERO_RESULTS":
        return 200000
    else:
        return get_shortest_duration(json_output) + 90


def get_transit(origin: str, destination: str) -> int:
    """ Get duration of shortest transit route between origin and destination (if it exists). """
    mode = "transit"
    request = requests.get(
        base_url + "origin=place_id:" + origin + "&destination=" + destination + "&mode=" + mode + "&key=" + api_key)
    json_output = request.json()
    if json_output["status"] == "ZERO_RESULTS":
        return 200000
    else:
        return get_shortest_duration(json_output)


def get_driving(origin: str, destination: str) -> int:
    """ Get duration of shortest driving route between origin and destination (if it exists). """
    mode = "driving"
    request = requests.get(
        base_url + "origin=place_id:" + origin + "&destination=" + destination + "&mode=" + mode + "&key=" + api_key)
    json_output = request.json()
    if json_output["status"] == "ZERO_RESULTS":
        return 200000
    else:
        return get_shortest_duration(json_output) + 720


def all_transport_modes(origin: str, destination: str) -> list:
    """ Get the duration of the shortest trip between origin and destination
    using each mode of transport: walking, biking, transit, driving. """
    durations = [
        get_walking(origin, destination),
        get_biking(origin, destination),
        get_transit(origin, destination),
        get_driving(origin, destination),
    ]
    return durations


def define_durations_header(input_file: str) -> None:
    """Define header for input_file, a .csv file designated for recording output from the record_durations method"""
    with open(input_file, 'w', newline='') as csv_out:
        csv_writer = csv.writer(csv_out)
        csv_writer.writerow(['TRACTID', 'LATITUDE', 'LONGITUDE', 'WALK', 'BIKE', 'TRANSIT', 'DRIVE', 'SHORTEST'])


def request_durations(origin: str, input_file: str, output_file: str) -> None:
    """ Request and record the durations of the shortest trips using each mode of transport from origin to the
    destinations stored in the rows of the input_file by writing the durations corresponding to each destination
    into the output file. BOTH input_file AND output_file MUST BE EXISTING .CSV FILES. Helper method to
     record_durations() below. """
    with open(input_file) as csv_in:
        csv_reader = csv.reader(csv_in)
        line_count = 0
        with open(output_file, 'a', newline='') as csv_out:
            csv_writer = csv.writer(csv_out)
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
                    full_row = tract_id, lat, long, walk, bike, transit, drive, shortest
                    csv_writer.writerow(full_row)


def record_durations(origin: str, input_files: list, output_file: str) -> None:
    """ Container method which uses helper function request_durations() above to record the durations of shortest trips
     using each mode of transport from origin to destinations stored in input_files and appends the calculated durations
     into the output_file. BOTH input_file AND output_file MUST BE EXISTING .CSV FILES. """
    define_durations_header(output_file)
    for input_file in input_files:
        print(f'Starting to process "{input_file}"')
        request_durations(origin, input_file, output_file)
        print(f'Data chunk processed... "{input_file}"')
    print("Durations formatted and recorded.")


# What recording of requests should look like: define the header for the formatted_durations_location.csv output file,
# then read the 3 equally sized centroid subfiles one by one, perform the requests, and append all the request results
# into the same output file which we just defined the header for.

# The 3 commands for record_durations() below are separated to represent the requests made for each origin node:
# (UofT, Pearson Airport, Union Station). Each record_durations() command is followed by a calculate_shares()
# command that calculates the share of census tracts which are fastest reached by each mode of transport from
# the origin node that was just previously used for duration requests.


record_durations(uoft_place_id, ["Formatted Data/formatted_centroids1.csv",
                                 "Formatted Data/formatted_centroids2.csv",
                                 "Formatted Data/formatted_centroids3.csv"],
                 "Formatted Data/formatted_durations_uoft.csv")
record_durations(pearson_airport_place_id, ["Formatted Data/formatted_centroids1.csv",
                                            "Formatted Data/formatted_centroids2.csv",
                                            "Formatted Data/formatted_centroids3.csv"],
                 "Formatted Data/formatted_durations_pearson.csv")
record_durations(union_station_place_id, ["Formatted Data/formatted_centroids1.csv",
                                          "Formatted Data/formatted_centroids2.csv",
                                          "Formatted Data/formatted_centroids3.csv"],
                 "Formatted Data/formatted_durations_unionst.csv")

# Once the above 3 commands are complete and all data chunks have been processed, move on to map visualization,
# which is managed in visualizer.py

# TODO: recompile master_merged_location.csv files to ensure changes made since last session are functional
# TODO: add README on GitHub and prepare instructions for reproducibility in case anyone wants to generate an updated,
#  contemporary map in future
