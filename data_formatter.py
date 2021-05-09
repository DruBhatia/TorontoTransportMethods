import geopandas as gpd
import matplotlib.pyplot as plt
import csv


def filter_df(df, attribute: str, value: str):
    """ Filters a pandas.DataFrame-like object, df, to produce a filtered dataframe, only returning the rows of df
    that match the value that was queried for in the specified attribute of df. """
    filtered_df = df.loc[df[attribute] == value]
    return filtered_df


def convert_coordinates(df, convention: int):
    """ Converts the coordinates of the polygons in a geopandas.GeoDataFrame-like object, df, to their equivalents in
    the specified convention. """
    return df.to_crs("EPSG:"+str(convention))


def format_centroids(input_csv: str, output_csv:str):
    """ Reads input_csv and produces a formatted output_csv file with each row of the file representing a geometric
    polygon from some masterfile and the longitude and latitude coordinates of said polygon's centroid. """
    with open(input_csv) as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        with open(output_csv, 'w', newline='') as output_file:
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
                    stripped_row = tract_id, longitude, latitude
                    writer.writerow(stripped_row)


def formatted_centroid_display(input_csv: str):
    """ Reads input_csv, which contains rows representing geometric polygons and their respective centroids in
    geopandas.Geometry format, and displays a formatted text in the output console describing the polygon's attributes,
    including the coordinates of its centroid as strings. """
    with open(input_csv) as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'Census tract {row[0]} has centroid of coordinates {row[1]}')


base_directory = "C:/Users/dhruo/Documents/Projects/TorontoTransportMethods/"
census_2016 = base_directory + "Geographical Data/lct_000b16a_e.shp"
census_tracts = gpd.read_file(census_2016)
full_map = census_tracts.plot()
census_tracts_toronto = filter_df(census_tracts, "CMANAME", "Toronto")
map_toronto = census_tracts_toronto.plot()
converted_map_toronto = convert_coordinates(census_tracts_toronto, 4326)
map_toronto_4326 = converted_map_toronto.plot()
plt.savefig('Maps/greater_toronto1.png', dpi=800)
converted_map_toronto.to_csv(
    base_directory + "Formatted Data/toronto_census_tracts_coordinates.csv")
centroids = converted_map_toronto.centroid
centroids.to_csv(base_directory + "Formatted Data/toronto_centroids.csv")
format_centroids("Formatted Data/toronto_centroids.csv", "Formatted Data/formatted_centroids.csv")

