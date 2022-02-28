import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import csv

# IMPORTANT:
# Declare working directory and files/lists to be used as frameworks for later visualization
# Make sure the directories in this section are updated and correspond to the file structure on your device
base_directory = "/"
census_2016 = "Geographical Data/lct_000b16a_e.shp"
census_tracts = gpd.read_file(census_2016)
census_tracts_toronto = census_tracts.loc[census_tracts['CMANAME'] == 'Toronto']
map_size = "core"  # change to "core" for map of city of Toronto proper, "greater" for map of Greater Toronto Area
origin = "uoft"  # change to "uoft" for UofT as origin, "unionst" for Union Station, or "pearson" for Pearson Airport


def calculate_shares(input_file: str, output_file: str) -> None:
    """ Calculates the share of the city's total census tracts that are best reached by each mode of transport, using
    data available in the input_file. Results are written in a basic table format to the output_file.
    BOTH input_file AND output_file MUST BE EXISTING .CSV FILES. """
    with open(input_file) as csv_in:
        csv_reader = csv.reader(csv_in)
        line_count = 0
        walking = 0
        biking = 0
        transit = 0
        driving = 0
        total = 0
        with open(output_file, 'w', newline='') as csv_out:
            csv_writer = csv.writer(csv_out)
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    if row[9] == "0":
                        walking += 1
                    elif row[9] == "1":
                        biking += 1
                    elif row[9] == "2":
                        transit += 1
                    elif row[9] == "3":
                        driving += 1
                    total += 1
            csv_writer.writerow(['MODE', 'TRACTS', 'SHARE'])
            csv_writer.writerow(['WALKING', walking, round((walking/total)*100, 2)])
            csv_writer.writerow(['BIKING', biking, round((biking/total)*100, 2)])
            csv_writer.writerow(['TRANSIT', transit, round((transit/total)*100, 2)])
            csv_writer.writerow(['DRIVING', driving, round((driving/total)*100, 2)])
            csv_writer.writerow(['TOTAL', walking+biking+transit+driving,
                                 round(((walking+biking+transit+driving)/total)*100, 2)])


# Parse a list of census tract (CT) data to strip redundant data
# Produces a formatted list of CT names that form the core City of Toronto and stores list
# in local scope for convenient manipulation and visualization later
core_tracts = base_directory + "Formatted Data/toronto_core_ctnames.csv"
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

# Visual checks to ensure parsing was successful. This section can be commented out safely if deemed unnecessary.
# print(len(core_tracts_list))
# print(core_tracts_list)
# print(census_tracts_toronto['CTNAME'])
# print(census_tracts['CTNAME'])

# Save an updated, non-redundant list of CTs that form the core City of Toronto
core_tracts_toronto = census_tracts_toronto[census_tracts_toronto['CTNAME'].isin(core_tracts_list)]
core_tracts_toronto.to_csv(base_directory + "Formatted Data/toronto_core_tracts.csv")

# Plot an uncoloured map template of the Greater Toronto Area as defined by the Census
map_toronto = census_tracts_toronto.plot()
converted_map_toronto = census_tracts_toronto.to_crs("EPSG:4326")
map_toronto_4326 = converted_map_toronto.plot()
plt.savefig('Maps/greater_toronto2.png', dpi=800)
plt.show()

# Plot an uncoloured map template of the core City of Toronto as defined by 2016 political boundaries
map_core_toronto = core_tracts_toronto.plot()
converted_map_core_toronto = core_tracts_toronto.to_crs("EPSG:4326")
map_core_toronto_4326 = converted_map_core_toronto.plot()
plt.savefig("Maps/core_toronto.png", dpi=800)
plt.show()

# Merge CT names with route data pulled from Google Maps API in directions.py
durations = pd.read_csv(base_directory + "Formatted Data/formatted_durations_" + origin + ".csv")
# print(durations.head())
# By default, route data is merged with the map of the core City of Toronto. To produce a map of the GTA, replace
# the value of map_size in line 13 with "greater" instead of "core"
if map_size == "greater":
    merged = converted_map_toronto.merge(durations, how="left", right_on="TRACTID", left_index=True)
else:
    merged = converted_map_core_toronto.merge(durations, how="left", right_on="TRACTID", left_index=True)
merged = merged[["TRACTID", "geometry", "LATITUDE",  "LONGITUDE", "WALK", "BIKE", "TRANSIT", "DRIVE", "SHORTEST"]]
# print(merged.head())
merged["SHORTEST"].fillna(value="4", inplace=True)
merged.to_csv(base_directory + "Formatted Data/master_merged_" + map_size + "_" + origin + ".csv")

# Assert and package hex colour values for each mode of transport
keys = ["0", "1", "2", "3", "4"]
colours = ["#65c81e", "#f5c73c", "#4384c4", "#d04f46", "xkcd:grey"]
colour_dict = dict(zip(keys, colours))

# Generate canvas framework for coloured map to be placed on in following section
row_count = 4
ax_list = []
for i in range(row_count+1):
    ax_list.append('ax' + str(i+1))
    ax_string = ', '.join(ax_list)
fig, (ax_string) = plt.subplots(row_count, 4)
ax1 = plt.subplot2grid((row_count, 4), (0, 0), rowspan=row_count, colspan=4)

# Iterate over map template(s) produced earlier and colour each CT as per quickest transport method,
# then plot map on subplot canvas produced in previous section and save plotted map as figure (.png)
for index, row in merged.iterrows():
    plot = merged[merged["TRACTID"] == row['TRACTID']].plot(color=colour_dict[str(int(row['SHORTEST']))], ax=ax1)
    ax1.axis("off")
fig.savefig(base_directory + "Maps/" + origin + "_" + map_size + "_coloured.png", dpi=1600)
print("Map plotted, saved in Maps/" + origin + "_" + map_size + "_coloured.png")

# Calculate percentage shares for each method of transport and save in .csv format
calculate_shares("Formatted Data/master_merged_" + map_size + "_" + origin + ".csv", "Formatted Data/transport_shares_"
                 + map_size + "_" + origin + ".csv")
print("Transport shares calculated, written to Formatted Data/transport_shares_" + map_size + "_" + origin + ".csv")
