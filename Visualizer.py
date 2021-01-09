import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import csv

census_2016 = "C:/Users/dhruo/Documents/Projects/TorontoTransportMethods/Geographical Data/lct_000b16a_e.shp"
census_tracts = gpd.read_file(census_2016)
census_tracts_toronto = census_tracts.loc[census_tracts['CMANAME'] == 'Toronto']
map_toronto = census_tracts_toronto.plot()
converted_map_toronto = census_tracts_toronto.to_crs("EPSG:4326")
map_toronto_4326 = converted_map_toronto.plot()
plt.savefig('greater_toronto2.png', dpi=800)
plt.show()
print(converted_map_toronto.head())

durations = pd.read_csv("C:/Users/dhruo/Documents/Projects/TorontoTransportMethods/sample_durations.csv")
print(durations.head())
merged = converted_map_toronto.merge(durations, how="left", right_on="TRACTID", left_index=True)
merged = merged[["TRACTID", "geometry", "LONGITUDE", "LATITUDE", "WALK", "BIKE", "TRANSIT", "DRIVE", "SHORTEST"]]
print(merged.head())
merged["SHORTEST"].fillna(value="NA", inplace=True)
# merged.to_csv("C:/Users/dhruo/Documents/Projects/TorontoTransportMethods/sample_merged.csv")

keys = ["0", "1", "2", "3"]
colours = ["green", "teal", "gold", "crimson"]
colour_dict = dict(zip(keys, colours))
colour_dict["NA"] = "grey"

