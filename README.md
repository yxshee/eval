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



import networkx as nx
import random
import matplotlib.pyplot as plt

# Create graph
G = nx.Graph()
edges = [('a', 'b'), ('a', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'f')]
G.add_edges_from(edges)

# Draw graph
nx.draw_networkx(G)
plt.axis('off')
plt.show()

def random_walk_no_edge_repeats(G, start_node, wlen):
    """
    Perform a random walk of up to length wlen on graph G,
    never traversing the same edge twice.
    """
    current = start_node
    walk = [start_node]
    # For undirected graphs, represent edges as frozensets
    visited_edges = set()

    for _ in range(wlen - 1):
        # Collect neighbors reachable by unused edges
        candidates = []
        for nbr in G.neighbors(current):
            edge = frozenset({current, nbr})
            if edge not in visited_edges:
                candidates.append(nbr)

        if not candidates:
            # Dead end: no unused edges left
            break

        # Choose next node at random
        next_node = random.choice(candidates)
        # Mark the undirected edge as used
        visited_edges.add(frozenset({current, next_node}))

        walk.append(next_node)
        current = next_node

    return walk

# Example usage
if __name__ == "__main__":
    path = random_walk_no_edge_repeats(G, start_node='a', wlen=10)
    print("Random walk (no edge repeats):", path)

