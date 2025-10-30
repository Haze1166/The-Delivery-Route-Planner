# algorithms/hamiltonian.py

def find_cycle(graph):
    """
    Finds a Hamiltonian Cycle in a graph using backtracking.
    Returns the path (list of vertex indices) if found, otherwise None.
    """
    num_vertices = len(graph)
    path = [-1] * num_vertices
    path[0] = 0  # Start at vertex 0 (Warehouse)
    visited = [False] * num_vertices
    visited[0] = True

    if not _find_cycle_util(graph, path, 1, visited):
        return None
    
    path.append(path[0]) # Add the starting point to the end to complete the cycle
    return path

def _find_cycle_util(graph, path, pos, visited):
    num_vertices = len(graph)
    
    # Base case: If all vertices are included in the path
    if pos == num_vertices:
        # Check if there is an edge from the last included vertex to the first vertex
        last_vertex = path[pos - 1]
        if graph[last_vertex][path[0]] != 0:
            return True
        else:
            return False

    for v in range(num_vertices):
        last_vertex_in_path = path[pos-1]
        # Check if vertex v can be added to the Hamiltonian Cycle
        if graph[last_vertex_in_path][v] != 0 and not visited[v]:
            path[pos] = v
            visited[v] = True

            # Recur to construct the rest of the path
            if _find_cycle_util(graph, path, pos + 1, visited):
                return True

            # If adding vertex v doesn't lead to a solution, backtrack
            path[pos] = -1
            visited[v] = False
    
    return False