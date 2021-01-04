import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
# import pysal as psal


census_2016 = "C:/Users/dhruo/Documents/Projects/Toronto Transport Methods/Geographical Data/lct_000b16a_e.shp"
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
    "C:/Users/dhruo/Documents/Projects/Toronto Transport Methods/toronto_census_tracts_coordinates.csv")
# for rows in converted_map_toronto.iterrows():
print(gpd.GeoSeries(converted_map_toronto.centroid))
centroids = converted_map_toronto.centroid
centroids.to_csv("C:/Users/dhruo/Documents/Projects/Toronto Transport Methods/toronto_centroids.csv")
