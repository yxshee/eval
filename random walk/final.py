import networkx as nx
import random
import matplotlib.pyplot as plt
from typing import List, Tuple, Any, Set

def random_walk_to_target_no_edge_repeats(
    G: nx.Graph, source: Any, target: Any, max_steps: int = 50
) -> Tuple[List[Any], bool]:
    """
    Perform an edge-simple random walk from source toward target on G.
    Never traverses the same edge twice. Stops when:
      - target is reached (success),
      - no unused edges remain at current node (dead end),
      - max_steps is exceeded.
    
    Args:
        G: NetworkX graph
        source: Starting node
        target: Destination node
        max_steps: Maximum number of steps allowed
        
    Returns:
        Tuple of (path, reached_target_successfully)
    """
    # Initialize variables
    current = source
    path = [source]  # Start with source node in path
    visited_edges = set()  # Track visited edges

    for step in range(max_steps):
        # Check if target reached
        if current == target:
            return path, True

        # Find valid neighbors (unused edges)
        candidates = []
        for nbr in G.neighbors(current):
            edge = frozenset({current, nbr})
            if edge not in visited_edges:
                candidates.append(nbr)

        if not candidates:
            # Dead end - no available edges to traverse
            break

        # Choose random neighbor and move
        next_node = random.choice(candidates)
        visited_edges.add(frozenset({current, next_node}))
        path.append(next_node)
        current = next_node

    # Return path and whether target was reached
    return path, (current == target)

if __name__ == "__main__":
    # --- 1) Create a specific graph topology ---
    G = nx.Graph()
    edges = [
        ('A','B'), ('A','C'),
        ('B','D'), ('C','D'),
        ('C','E'), ('D','F'),
        ('E','G'), ('F','H'),
        ('G','H')
    ]
    G.add_edges_from(edges)

    # --- 2) Define source and target nodes ---
    source, target = 'A', 'H'

    # --- 3) Visualize the initial graph with source and target ---
    pos = nx.spring_layout(G, seed=1)
    plt.figure(figsize=(5,5))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=400)
    nx.draw_networkx_edges(G, pos, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10)
    nx.draw_networkx_nodes(G, pos, nodelist=[source], node_color='green', label='Source', node_size=400)
    nx.draw_networkx_nodes(G, pos, nodelist=[target], node_color='red', label='Target', node_size=400)
    plt.legend(scatterpoints=1)
    plt.title("Network with Source and Target")
    plt.axis('off')
    plt.show()

    # --- 4) Execute the random walk algorithm ---
    path, reached = random_walk_to_target_no_edge_repeats(G, source, target, max_steps=20)
    print(f"Reached target? {reached}")
    print("Path length:", len(path))
    print("Path:", " → ".join(path))

    # --- 5) Visualize the path if target was reached ---
    if reached:
        edge_path = list(zip(path, path[1:]))
        plt.figure(figsize=(5,5))
        nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=400)
        nx.draw_networkx_edges(G, pos, edge_color='lightgray')
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange', node_size=400)
        nx.draw_networkx_edges(G, pos, edgelist=edge_path, width=2, edge_color='blue')
        nx.draw_networkx_labels(G, pos, font_size=10)
        plt.title("Random Walk Path from A to H")
        plt.axis('off')
        plt.show()
    else:
        print("Did not reach the target before dead end or max steps.")