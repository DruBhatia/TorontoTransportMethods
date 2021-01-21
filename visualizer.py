import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import csv

census_2016 = "C:/Users/dhruo/Documents/Projects/TorontoTransportMethods/Geographical Data/lct_000b16a_e.shp"
census_tracts = gpd.read_file(census_2016)
census_tracts_toronto = census_tracts.loc[census_tracts['CMANAME'] == 'Toronto']

core_tracts = "C:/Users/dhruo/Documents/Projects/TorontoTransportMethods/toronto_core_ctnames.csv"
with open(core_tracts) as csv_file:
    csv_reader = csv.reader(csv_file)
    line_counter = 0
    core_tracts_list = []
    for row in csv_reader:
        if line_counter == 0:
            line_counter += 1
        else:
            ctname = row[1]
            if len(row[1].split(".")[0]) == 1:
                ctname = "000" + ctname
            elif len(row[1].split(".")[0]) == 2:
                ctname = "00" + ctname
            else:
                ctname = "0" + ctname
            if len(row[1].split(".")) == 1:
                ctname = ctname + ".00"
            else:
                if len(row[1].split(".")[1]) == 1:
                    ctname = ctname + "0"
            core_tracts_list.append(ctname)
core_tracts_list = list(dict.fromkeys(core_tracts_list))
print(len(core_tracts_list))
print(core_tracts_list)
print(census_tracts_toronto['CTNAME'])
print(census_tracts['CTNAME'])

core_tracts_toronto = census_tracts_toronto[census_tracts_toronto['CTNAME'].isin(core_tracts_list)]

map_toronto = census_tracts_toronto.plot()
converted_map_toronto = census_tracts_toronto.to_crs("EPSG:4326")
map_toronto_4326 = converted_map_toronto.plot()
plt.savefig('greater_toronto2.png', dpi=800)
plt.show()

map_core_toronto = core_tracts_toronto.plot()
converted_map_core_toronto = core_tracts_toronto.to_crs("EPSG:4326")
map_core_toronto_4326 = converted_map_core_toronto.plot()
plt.savefig("core_toronto.png", dpi=800)
plt.show()

durations = pd.read_csv("C:/Users/dhruo/Documents/Projects/TorontoTransportMethods/formatted_durations_pearson.csv")
print(durations.head())
merged = converted_map_core_toronto.merge(durations, how="left", right_on="TRACTID", left_index=True)
merged = merged[["TRACTID", "geometry", "LATITUDE",  "LONGITUDE", "WALK", "BIKE", "TRANSIT", "DRIVE", "SHORTEST"]]
print(merged.head())
merged["SHORTEST"].fillna(value="4", inplace=True)
merged.to_csv("C:/Users/dhruo/Documents/Projects/TorontoTransportMethods/master_merged_unionst1.csv")

keys = ["0", "1", "2", "3", "4"]
colours = ["#65c81e", "#f5c73c", "#4384c4", "#d04f46", "xkcd:grey"]
colour_dict = dict(zip(keys, colours))

row_count = 4
ax_list = []
for i in range(row_count+1):
    ax_list.append('ax' + str(i+1))
    ax_string = ', '.join(ax_list)
fig, (ax_string) = plt.subplots(row_count, 4)
ax1 = plt.subplot2grid((row_count, 4), (0, 0), rowspan=row_count, colspan=4)

for index, row in merged.iterrows():
    plot = merged[merged["TRACTID"] == row['TRACTID']].plot(color=colour_dict[str(int(row['SHORTEST']))], ax=ax1)
    ax1.axis("off")
    ax1.set_title("Quickest method around City of Toronto from Pearson Airport")
fig.savefig("pearson_core_coloured.png", dpi=1600)
