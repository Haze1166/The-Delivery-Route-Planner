# planner_logic.py
import math
from algorithms.knapsack import solve as knapsack_solve
from algorithms.hamiltonian import find_cycle as hamiltonian_find_cycle

MAX_LOCATIONS_FOR_HAMILTONIAN = 10 # Performance guardrail

def calculate_distance_matrix(location_names, locations_data):
    """Creates a distance matrix for the given locations."""
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
    """
    Main logic function to run the full planning process.
    Returns a dictionary with all results or an error.
    """
    from data_loader import load_packages, load_locations
    
    all_packages = load_packages()
    all_locations = load_locations()
    
    # 1. Knapsack: Select packages for the manifest
    weights = [p['weight_kg'] for p in all_packages]
    priorities = [p['priority'] for p in all_packages]
    max_priority, selected_indices = knapsack_solve(weights, priorities, capacity)
    
    manifest = [all_packages[i] for i in selected_indices]
    if not manifest:
        return {'error': 'No packages could be selected for the given capacity.'}
        
    total_weight = sum(p['weight_kg'] for p in manifest)

    # 2. Hamiltonian: Plan the route
    route_location_names = ['Warehouse'] + sorted(list(set(p['destination'] for p in manifest)))
    
    # Performance Guardrail
    if len(route_location_names) > MAX_LOCATIONS_FOR_HAMILTONIAN:
        return {
            'error': f'Route planning failed: Too many unique destinations ({len(route_location_names)}). Maximum allowed is {MAX_LOCATIONS_FOR_HAMILTONIAN} for performance reasons.'
        }
        
    dist_matrix = calculate_distance_matrix(route_location_names, all_locations)
    route_indices = hamiltonian_find_cycle(dist_matrix)
    
    route_names = []
    route_coords = []
    if route_indices:
        route_names = [route_location_names[i] for i in route_indices]
        route_coords = [[all_locations[name]['lat'], all_locations[name]['lon']] for name in route_names]

    # 3. Assemble results
    return {
        'manifest': manifest,
        'total_weight': total_weight,
        'max_priority': max_priority,
        'route_names': route_names,
        'route_coords': route_coords,
        'location_data': {name: all_locations[name] for name in route_location_names}
    }