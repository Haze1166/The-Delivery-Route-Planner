import copy

def solve_greedy(packages, capacity, strategy):
    packages_copy = copy.deepcopy(packages)
    sorted_packages = []
    
    if strategy == 'min_weight':
        sorted_packages = sorted(packages_copy, key=lambda p: p['weight_kg'])
    elif strategy == 'max_profit':
        sorted_packages = sorted(packages_copy, key=lambda p: p['profit'], reverse=True)
    elif strategy == 'max_ratio':
        for p in packages_copy:
            p['ratio'] = p['profit'] / p['weight_kg'] if p['weight_kg'] > 0 else 0
        sorted_packages = sorted(packages_copy, key=lambda p: p['ratio'], reverse=True)
    else:
        return [], 0, 0

    manifest, total_weight, total_profit = [], 0, 0
    for package in sorted_packages:
        if total_weight + package['weight_kg'] <= capacity:
            manifest.append(package)
            total_weight += package['weight_kg']
            total_profit += package['profit']
            
    return manifest, total_weight, total_profit