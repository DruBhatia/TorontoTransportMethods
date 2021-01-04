import csv
import geopandas as gpd

# Ensure that geometry fields can be read since they are very large
csv.field_size_limit(400000)


def parse(input_file: str) -> None:
    """
    Parses input_file, performs necessary manipulation and writes the cleaned output to an output csv file.
    """
    with open(input_file, 'r', newline='') as data_in:
        # skip header
        next(data_in)
        reader = csv.reader(data_in)
        with open('census_cleaned.csv', 'w', newline='') as data_out:
            writer = csv.writer(data_out)
            writer.writerow(
                ['', 'CTUID', 'CTNAME', 'PRUID', 'PRNAME', 'CMAUID', 'CMAPUID', 'CMANAME', 'CMATYPE', 'geometry',
                 'centroid'])
            for row in reader:
                n, ctuid, ctname, pruid, prname, cmauid, cmapuid, cmaname, cmatype, geometry = row
                # manipulate your data here
                writer.writerow(row)


if __name__ == '__main__':
    parse('toronto_census_tracts_coordinates.csv')
