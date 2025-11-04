import math
from algorithms.knapsack import solve as knapsack_solve
from algorithms.hamiltonian import find_cycle as hamiltonian_find_cycle
from data_loader import load_packages, load_locations

MAX_LOCATIONS_FOR_HAMILTONIAN = 10 

def calculate_distance_matrix(location_names, locations_data):
    n = len(location_names)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j: continue
            loc1 = locations_data[location_names[i]]
            loc2 = locations_data[location_names[j]]
            dist = math.sqrt((loc1['lat'] - loc2['lat'])**2 + (loc1['lon'] - loc2['lon'])**2)
            matrix[i][j] = int(dist * 1000)
    return matrix

def plan_delivery(capacity):
    all_packages = load_packages()
    all_locations = load_locations()
    
    weights = [p['weight_kg'] for p in all_packages]
    priorities = [p['priority'] for p in all_packages]
    max_priority, selected_indices = knapsack_solve(weights, priorities, capacity)
    
    manifest = [all_packages[i] for i in selected_indices]
    total_weight = sum(p['weight_kg'] for p in manifest)
    
    route_location_names = ['Warehouse'] + sorted(list(set(p['destination'] for p in manifest)))
    
    route_names, route_coords = [], []
    if 1 < len(route_location_names) <= MAX_LOCATIONS_FOR_HAMILTONIAN:
        dist_matrix = calculate_distance_matrix(route_location_names, all_locations)
        route_indices = hamiltonian_find_cycle(dist_matrix)
        if route_indices:
            route_names = [route_location_names[i] for i in route_indices]
            route_coords = [[all_locations[name]['lat'], all_locations[name]['lon']] for name in route_names]

    return {
        'manifest': manifest,
        'total_weight': total_weight,
        'total_priority': max_priority,
        'route_names': route_names,
        'route_coords': route_coords
    }