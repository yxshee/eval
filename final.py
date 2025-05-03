import networkx as nx
import random
import matplotlib.pyplot as plt

def random_walk_to_target_no_edge_repeats(G, source, target, max_steps=50):
    current = source
    path = [source]
    visited_edges = set()

    for _ in range(max_steps):
        if current == target:
            return path, True

        candidates = []
        for nbr in G.neighbors(current):
            edge = frozenset({current, nbr})
            if edge not in visited_edges:
                candidates.append(nbr)

        if not candidates:
            break

        next_node = random.choice(candidates)
        visited_edges.add(frozenset({current, next_node}))
        path.append(next_node)
        current = next_node

    return path, (current == target)

if __name__ == "__main__":
    G = nx.Graph()
    edges = [
        ('A','B'), ('A','C'),
        ('B','D'), ('C','D'),
        ('C','E'), ('D','F'),
        ('E','G'), ('F','H'),
        ('G','H')
    ]
    G.add_edges_from(edges)

    source, target = 'A', 'H'

    pos = nx.spring_layout(G, seed=1)
    plt.figure(figsize=(5,5))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=400)
    nx.draw_networkx_edges(G, pos, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10)
    nx.draw_networkx_nodes(G, pos, nodelist=[source], node_color='green', node_size=400)
    nx.draw_networkx_nodes(G, pos, nodelist=[target], node_color='red', node_size=400)
    plt.legend(['Source','Target'])
    plt.axis('off')
    plt.show()

    path, reached = random_walk_to_target_no_edge_repeats(G, source, target, max_steps=20)
    print(f"Reached target? {reached}")
    print("Path length:", len(path))
    print("Path:", " → ".join(path))

    if reached:
        edge_path = list(zip(path, path[1:]))
        plt.figure(figsize=(5,5))
        nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=400)
        nx.draw_networkx_edges(G, pos, edge_color='lightgray')
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange', node_size=400)
        nx.draw_networkx_edges(G, pos, edgelist=edge_path, width=2, edge_color='blue')
        nx.draw_networkx_labels(G, pos, font_size=10)
        plt.axis('off')
        plt.show()
    else:
        print("Did not reach the target before dead end or max steps.")