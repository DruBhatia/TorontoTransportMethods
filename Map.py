import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import csv
# import pysal as psal


census_2016 = "C:/Users/dhruo/Documents/Projects/TorontoTransportMethods/Geographical Data/lct_000b16a_e.shp"
census_tracts = gpd.read_file(census_2016)
full_map = census_tracts.plot()
census_tracts_toronto = census_tracts.loc[census_tracts['CMANAME'] == 'Toronto']
map_toronto = census_tracts_toronto.plot()
print(type(census_tracts))
print(census_tracts_toronto.head())
converted_map_toronto = census_tracts_toronto.to_crs("EPSG:4326")
map_toronto_4326 = converted_map_toronto.plot()
plt.show()
print(converted_map_toronto.head())
converted_map_toronto.to_csv(
    "C:/Users/dhruo/Documents/Projects/TorontoTransportMethods/toronto_census_tracts_coordinates.csv")
# for rows in converted_map_toronto.iterrows():
print(gpd.GeoSeries(converted_map_toronto.centroid))
centroids = converted_map_toronto.centroid
centroids.to_csv("C:/Users/dhruo/Documents/Projects/TorontoTransportMethods/toronto_centroids.csv")

# with open("toronto_centroids.csv") as csv_file:
#     csv_reader = csv.reader(csv_file)
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             print(f'Census tract {row[0]} has centroid of coordinates {row[1]}')

with open("toronto_centroids.csv") as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    with open('formatted_centroids.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['TRACTID', 'LONGITUDE', 'LATITUDE'])
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                tract_id = row[0]
                coordinate = row[1][6:].strip("()")
                latlong = coordinate.split(" ")
                longitude = latlong[0]
                latitude = latlong[1]
                manipulated_row = tract_id, longitude, latitude
                writer.writerow(manipulated_row)

