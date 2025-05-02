# eval

import random

def non_repeating_random_walk(adj_list, start):
    """
    Perform a random walk on the graph defined by adj_list,
    never revisiting a node.
    
    adj_list: dict mapping each node to an iterable of neighbors
    start: starting node
    Returns: list of nodes in the order visited
    """
    visited = {start}
    path = [start]
    current = start

    while True:
        # Filter neighbors to those not yet visited
        unvisited_neighbors = [n for n in adj_list.get(current, []) if n not in visited]
        if not unvisited_neighbors:
            break  # no more moves possible
        # Choose one at random
        next_node = random.choice(unvisited_neighbors)
        visited.add(next_node)
        path.append(next_node)
        current = next_node

    return path

# Example usage
if __name__ == "__main__":
    # Simple undirected graph
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'C', 'D'],
        'C': ['A', 'B', 'D', 'E'],
        'D': ['B', 'C', 'E'],
        'E': ['C', 'D']
    }

    walk = non_repeating_random_walk(graph, start='A')
    print("Random walk (no repeats):", walk)