import networkx as nx
import random
import matplotlib.pyplot as plt

def random_walk_to_target_no_edge_repeats(G, source, target, max_steps=100):
    """
    Perform an edge-simple random walk from source toward target on G.
    Never traverses the same edge twice. Stops when:
      - target is reached (success),
      - no unused edges remain at current node (dead end),
      - max_steps is exceeded.
    Returns (path, reached_target: bool).
    """
    current = source
    path = [source]
    visited_edges = set()  # store frozenset({u, v}) for each undirected edge used

    for _ in range(max_steps):
        if current == target:
            return path, True

        # gather next‐step candidates via unused edges
        candidates = []
        for nbr in G.neighbors(current):
            edge = frozenset({current, nbr})
            if edge not in visited_edges:
                candidates.append(nbr)

        if not candidates:
            # dead end reached
            break

        next_node = random.choice(candidates)
        visited_edges.add(frozenset({current, next_node}))
        path.append(next_node)
        current = next_node

    return path, (current == target)

if __name__ == "__main__":
    # 1) Build a graph of up to 12 nodes (Erdős–Rényi random graph)
    n = 12
    p = 0.25  # probability of edge creation
    G = nx.erdos_renyi_graph(n, p)
    # relabel to strings "n0", "n1", ...
    G = nx.relabel_nodes(G, lambda x: f"n{x}")

    # ensure we have at least one path between source and target
    while not nx.is_connected(G):
        G = nx.erdos_renyi_graph(n, p)
        G = nx.relabel_nodes(G, lambda x: f"n{x}")

    # 2) Pick distinct source and target
    nodes = list(G.nodes())
    source, target = random.sample(nodes, 2)

    # 3) Draw the graph, highlighting source (green) and target (red)
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(6,6))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8)
    nx.draw_networkx_nodes(G, pos, nodelist=[source], node_color='green', label='Source', node_size=300)
    nx.draw_networkx_nodes(G, pos, nodelist=[target], node_color='red', label='Target', node_size=300)
    plt.legend(scatterpoints=1)
    plt.axis('off')
    plt.title("Random Graph with 12 Nodes")
    plt.show()

    # 4) Run the edge‐simple random walk towards target
    path, reached = random_walk_to_target_no_edge_repeats(G, source, target, max_steps=50)
    print(f"Source: {source}, Target: {target}")
    print("Reached target?", reached)
    print("Path length:", len(path))
    print("Path:", " → ".join(path))

    # 5) If reached, overlay the path
    if reached:
        edge_path = list(zip(path, path[1:]))
        plt.figure(figsize=(6,6))
        nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=300)
        nx.draw_networkx_edges(G, pos, alpha=0.3)
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange', node_size=300)
        nx.draw_networkx_edges(G, pos, edgelist=edge_path, width=2, edge_color='blue')
        nx.draw_networkx_labels(G, pos, font_size=8)
        plt.title("Walked Path (No Edge Repeats)")
        plt.axis('off')
        plt.show()
    else:
        print("Did not reach the target before dead end or max steps.")