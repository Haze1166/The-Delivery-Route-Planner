import csv

def load_packages(filepath='data/packages.csv'):
    packages = []
    with open(filepath, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            row['weight_kg'] = int(row['weight_kg'])
            row['priority'] = int(row['priority'])
            packages.append(row)
    return packages

def load_locations(filepath='data/locations_with_coords.csv'):
    locations = {}
    with open(filepath, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            locations[row['location']] = {
                'lat': float(row['lat']),
                'lon': float(row['lon'])
            }
    return locations