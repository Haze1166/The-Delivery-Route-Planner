# algorithms/linear_search.py

def search(data_list, target_id):
    """
    Performs a linear search on a list of dictionaries to find a package by its ID.
    """
    for item in data_list:
        if item['package_id'] == target_id:
            return item
    return None