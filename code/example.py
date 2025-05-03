import networkx as nx
import matplotlib.pyplot as plt
from random_walks import random_walk, random_walk_until_target, compute_hitting_time, compute_commute_time
from code.mcl import mcl, get_clusters
from code.pagerank import pagerank
from code.centrality import compute_centralities, print_centrality_measures

def example_random_walks():
    """Example of random walk algorithms"""
    print("\n=== Random Walks Example ===")
    G = nx.Graph()
    edges = [('a', 'b'), ('a', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'f')]
    G.add_edges_from(edges)
    
    # Draw the graph
    plt.figure(figsize=(8, 5))
    nx.draw_networkx(G)
    plt.title("Example Graph")
    plt.axis('off')
    plt.show()
    
    # Simple random walk
    walk = random_walk(G, 'a', 10)
    print(f"Random walk from 'a': {walk}")
    
    # Random walk to target
    steps = random_walk_until_target(G, 'a', 'f')
    print(f"Steps from 'a' to 'f': {steps}")
    
    # Hitting time
    hit_time = compute_hitting_time(G, 'a', 'f', simulations=100)
    print(f"Average hitting time from 'a' to 'f': {hit_time:.2f}")
    
    # Commute time
    commute_time = compute_commute_time(G, 'a', 'f', simulations=100)
    print(f"Average commute time between 'a' and 'f': {commute_time:.2f}")

def example_mcl():
    """Example of MCL clustering algorithm"""
    print("\n=== MCL Clustering Example ===")
    G = nx.Graph()
    edges = [
        ('a', 'b'), ('a', 'c'), ('b', 'c'), ('c', 'd'),
        ('d', 'e'), ('e', 'f'), ('f', 'g'), ('g', 'h'),
        ('h', 'i'), ('i', 'j'), ('j', 'h')
    ]
    G.add_edges_from(edges)
    
    # Run MCL
    M = mcl(G, expand_power=2, inflate_power=2, iterations=15)
    
    # Get clusters
    nodes = list(G.nodes())
    clusters = get_clusters(M, nodes)
    
    print("Clusters found:")
    for idx, cluster in enumerate(clusters):
        print(f"Cluster {idx+1}: {cluster}")

def example_pagerank():
    """Example of PageRank algorithm"""
    print("\n=== PageRank Example ===")
    G = nx.DiGraph()
    edges = [
        ('A', 'B'), ('A', 'C'), ('B', 'C'), ('C', 'A'),
        ('D', 'C'), ('E', 'C'), ('F', 'C'), ('C', 'F'),
        ('E', 'F'), ('F', 'E')
    ]
    G.add_edges_from(edges)
    
    # Compute PageRank
    page_ranks = pagerank(G)
    
    # Print results
    print("PageRank scores:")
    for page, rank in page_ranks.items():
        print(f"Page {page}: {rank:.4f}")

def example_centrality():
    """Example of centrality measures"""
    print("\n=== Centrality Measures Example ===")
    G = nx.Graph()
    edges = [
        ('Alice', 'Bob'), ('Alice', 'Charlie'),
        ('Bob', 'David'), ('Charlie', 'David'),
        ('Charlie', 'Eve'), ('David', 'Eve'),
        ('Eve', 'Frank'), ('Frank', 'Grace')
    ]
    G.add_edges_from(edges)
    
    # Compute centralities
    centralities = compute_centralities(G)
    
    # Print results
    print_centrality_measures(centralities)

if __name__ == "__main__":
    example_random_walks()
    example_mcl()
    example_pagerank()
    example_centrality()
