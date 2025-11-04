def find_cycle(graph):
    num_vertices = len(graph)
    path = [-1] * num_vertices
    path[0] = 0
    visited = [False] * num_vertices
    visited[0] = True

    if not _find_cycle_util(graph, path, 1, visited):
        return None
    
    path.append(path[0])
    return path

def _find_cycle_util(graph, path, pos, visited):
    num_vertices = len(graph)
    if pos == num_vertices:
        return graph[path[pos - 1]][path[0]] != 0

    for v in range(num_vertices):
        last_vertex_in_path = path[pos-1]
        if graph[last_vertex_in_path][v] != 0 and not visited[v]:
            path[pos] = v
            visited[v] = True
            if _find_cycle_util(graph, path, pos + 1, visited):
                return True
            path[pos] = -1
            visited[v] = False
    return False