#!/home/halljona/anaconda3/bin/python3

# get_routes.py
# Created by Jonathan D. Hall (jonathan.hall@utoronto.ca)
# This gets routes from Google Maps

import googlemaps
from datetime import datetime
from datetime import timedelta
import time
import numpy as np
import os
import sqlite3
import math
import csv
import hashlib
import json
import random
import requests

database_name = "../output/routes.db"
hours_to_run = [2,3,9,18]
time_zone_adj = '+8 hours'
time_zone_adj2 = +8
max_jobs_month = 20000
max_jobs_day = 6000
max_jobs_hour = math.floor(max_jobs_day / len(hours_to_run))
api_key_list = ["AAA", "BBB"] 
salt = bytes(6955854)

# Select which API key to use
api_key = random.choice(api_key_list)
api_hash = hashlib.pbkdf2_hmac('sha256', api_key.encode('utf-8'), salt, 100000).hex()


def find_n_jobs_to_run():
    """
    Find the number of jobs to run. This is the smaller of (1) remaining jobs that can be run today, (2) remaining jobs that can be run this hour, (3) remaining minutes in hour * 60.
    """
    n_jobs_this_month = conn.execute('''SELECT COUNT(tripid) FROM routes WHERE strftime('%Y-%m','now',?) == strftime('%Y-%m',time_run) AND api_key_used == ?''',(time_zone_adj,api_hash)).fetchone()[0] 
    n_jobs_today = conn.execute('''SELECT COUNT(tripid) FROM routes WHERE strftime('%Y-%m-%d','now',?) == strftime('%Y-%m-%d',time_run)''',(time_zone_adj,)).fetchone()[0] 
    n_jobs_this_hour = conn.execute('''SELECT COUNT(tripid) FROM routes WHERE strftime('%Y-%m-%dT%H','now',?) == strftime('%Y-%m-%dT%H',time_run)''',(time_zone_adj,)).fetchone()[0] 
    n_minutes_left_in_hour = (55 - datetime.now().minute)
    n_jobs_to_run = min( max_jobs_month - n_jobs_this_month, max_jobs_day - n_jobs_today, max_jobs_hour - n_jobs_this_hour, n_minutes_left_in_hour * 60)
    return n_jobs_to_run
    

def get_and_save_directions(row):
    """
    For in input list, get and save the Google Maps routes (polyline and text) for the recommended route and up to two alternate routes.
    """
    (origin, destination, target_hour) = row
    
    # Get routes from Google Maps
    dr = gmaps.directions(origin,
                      destination,
                      mode="driving",
                      departure_time="now", alternatives=True)
    
    # Process results from Google Maps -- Saving polyline and text directions
    polyline = []
    text_directions = []
   
    # Save results back to database
    conn.execute('''UPDATE routes SET results = ?, time_run = datetime('now',?), api_key_used = ?
                                WHERE 
                                   target_hour == ? AND
                                   origin == ? AND
                                   destination == ?''',
              (json.dumps(dr), time_zone_adj, api_hash,
               target_hour, origin, destination))
    
def create_database():
    """
    Creates the database we will store our jobs and results in
    """
    with sqlite3.connect(database_name) as conn:
        # Create the database
        conn.execute('''CREATE TABLE routes (
            target_hour INTEGER NOT NULL,
            time_run DATETIME,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            tripid INTEGER NOT NULL,
            timezone TEXT NOT NULL,
            city TEXT NOT NULL,
            priority INTEGER NOT NULL,
            api_key_used TEXT,
            results JSON
            ) ''')
        
        # Import list of O-D pairs
        with open("../temp/alltrips-manila.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
            next(csv_reader)  # skip the headers
            # Create an entry for each O-D pair and each hour_to_run
            for line in csv_reader:
                orig = str(line[1]) + "," + str(line[2])
                dest = str(line[3]) + "," + str(line[4])
                odpairid = line[0] # ID of OD pair
                timezone = line[6]
                priority = line[8]
                city = line[5]
                for hour in hours_to_run:
                    conn.execute('''INSERT INTO routes (target_hour, origin, destination, tripid, timezone, city, priority) VALUES (?,?,?,?,?,?,?)''', (hour, orig, dest, odpairid, timezone, city, priority) )
        
        # Create index
        conn.execute('''CREATE INDEX idx ON routes (origin, destination)''')
        # Commit changes
        conn.commit()


# If the database doesn't exist, create it
if not os.path.isfile(database_name):
    create_database()

# Connect to database
conn = sqlite3.connect(database_name)

# Initialize Google Maps API
gmaps = googlemaps.Client(key=api_key)


while True:
    
#     # If it is 1am, check if done
#     if (datetime.utcnow() + timedelta(hours = time_zone_adj2)).hour == 1:
#         n_jobs_remaining = conn.execute('''SELECT COUNT(tripid) FROM routes WHERE route1polyline IS NULL''').fetchone()[0]
#         print('There are ' + str(n_jobs_remaining) + ' jobs remaining.') 
#         if n_jobs_remaining == 0:
#             break
    
    # If it is the weekend, don't run
    if (datetime.utcnow() + timedelta(hours = time_zone_adj2)).weekday() >= 5:
        break
    
    
    # Decide how many jobs to run
    n_jobs_to_run = find_n_jobs_to_run()
    if n_jobs_to_run <= 0:
        break
    
    # Find the lowest priority level with remaining jobs
    n_jobs_by_priority = conn.execute('''SELECT priority, COUNT(tripid) FROM routes GROUP BY priority''').fetchall()
    nnn = 0
    priority_level = -1
    while nnn == 0:
        priority_level += 1
        nnn = n_jobs_by_priority[priority_level][1]
    
    print(priority_level)
    print(n_jobs_to_run)

    # Are there any jobs to run
    n_jobs_available = conn.execute('''SELECT COUNT(tripid) FROM routes 
        WHERE target_hour == strftime('%H','now',?) AND results IS NULL AND priority == ?
        ORDER BY RANDOM()
        LIMIT ?''',
        (time_zone_adj, priority_level, n_jobs_to_run)).fetchall()[0][0]
    print(n_jobs_available)
    if n_jobs_available < 1:
        break

    jobs_to_run = conn.execute('''SELECT origin, destination, target_hour FROM routes 
        WHERE target_hour == strftime('%H','now',?) AND results IS NULL AND priority == ?
        ORDER BY RANDOM()
        LIMIT ?''',
        (time_zone_adj, priority_level, n_jobs_to_run))

    # Actually run
    for row in jobs_to_run:
        get_and_save_directions(row)

    # Commit changes to database
    conn.commit()
    
# Check with healthchecks.io
requests.get("https://hc-ping.com/b8b0d2a9-79bc-44ba-9f53-50a111984212", timeout=10)

# Are all available jobs done?    
n_jobs_left = conn.execute('''SELECT COUNT(tripid) FROM routes''').fetchall()[0][0]
print(n_jobs_left)
if n_jobs_left < 1:
    requests.get("https://hc-ping.com/b8b0d2a9-79bc-44ba-9f53-50a111984212/fail", timeout=10) ## Send a failure signal to healthchecks.io
