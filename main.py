# main.py

import csv
from algorithms.knapsack import solve as knapsack_solve
from algorithms.hamiltonian import find_cycle as hamiltonian_find_cycle
from algorithms.linear_search import search as linear_search

# --- Configuration ---
TRUCK_CAPACITY_KG = 100
PACKAGES_FILE = 'data/packages.csv'
LOCATIONS_FILE = 'data/locations.csv'

def load_data(packages_filepath, locations_filepath):
    """Loads packages and location data from CSV files."""
    packages = []
    with open(packages_filepath, mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            row['weight_kg'] = int(row['weight_kg'])
            row['priority'] = int(row['priority'])
            packages.append(row)
    
    locations = []
    distance_matrix = []
    with open(locations_filepath, mode='r') as infile:
        reader = csv.reader(infile)
        locations = next(reader)[1:] # Get header row for location names
        for row in reader:
            distance_matrix.append([int(d) for d in row[1:]])
            
    return packages, locations, distance_matrix

def main():
    """Main function to run the delivery planner workflow."""
    all_packages, all_locations, full_dist_matrix = load_data(PACKAGES_FILE, LOCATIONS_FILE)

    print("--- 1. Optimizing Truck Load using Knapsack Algorithm ---")
    
    # Prepare data for Knapsack
    weights = [p['weight_kg'] for p in all_packages]
    priorities = [p['priority'] for p in all_packages]

    max_priority, selected_indices = knapsack_solve(weights, priorities, TRUCK_CAPACITY_KG)
    
    truck_manifest = [all_packages[i] for i in selected_indices]
    total_weight = sum(p['weight_kg'] for p in truck_manifest)

    print(f"\nTruck Capacity: {TRUCK_CAPACITY_KG}kg")
    print(f"Optimized to carry {len(truck_manifest)} packages.")
    print(f"Total Weight: {total_weight}kg | Total Priority: {max_priority}")
    print("\n--- Loading Manifest ---")
    for pkg in truck_manifest:
        print(f"  - ID: {pkg['package_id']}, Dest: {pkg['destination']}, Weight: {pkg['weight_kg']}kg, Priority: {pkg['priority']}")

    print("\n\n--- 2. Planning Delivery Route using Hamiltonian Cycle Algorithm ---")
    
    # Get unique destinations from the manifest + Warehouse
    route_locations = ['Warehouse'] + sorted(list(set(p['destination'] for p in truck_manifest)))
    
    # Create a mapping from location name to index in the full matrix
    location_to_idx = {name: i for i, name in enumerate(all_locations)}
    
    # Build a smaller distance matrix for only the locations in our route
    num_route_locs = len(route_locations)
    route_dist_matrix = [[0] * num_route_locs for _ in range(num_route_locs)]
    
    for i in range(num_route_locs):
        for j in range(num_route_locs):
            loc1_name = route_locations[i]
            loc2_name = route_locations[j]
            
            idx1 = location_to_idx[loc1_name]
            idx2 = location_to_idx[loc2_name]
            
            route_dist_matrix[i][j] = full_dist_matrix[idx1][idx2]

    # Find the Hamiltonian cycle
    route_path_indices = hamiltonian_find_cycle(route_dist_matrix)

    if route_path_indices:
        route_path_names = [route_locations[i] for i in route_path_indices]
        print("\nOptimal Delivery Route Found:")
        print(" -> ".join(route_path_names))
    else:
        print("\nCould not find a valid round-trip route for the selected packages.")

    print("\n\n--- 3. On-the-Road Package Lookup using Linear Search ---")
    while True:
        search_id = input("\nEnter a Package ID to search on the truck (or 'exit' to quit): ").strip().upper()
        if search_id == 'EXIT':
            break
        
        found_package = linear_search(truck_manifest, search_id)
        
        if found_package:
            print(f"\nPackage Found:")
            print(f"  - ID: {found_package['package_id']}")
            print(f"  - Destination: {found_package['destination']}")
            print(f"  - Weight: {found_package['weight_kg']}kg")
        else:
            print(f"\nPackage '{search_id}' is NOT on the current truck manifest.")

    print("\n--- Simulation Ended ---")

if __name__ == "__main__":
    main()