import networkx as nx
import matplotlib.pyplot as plt
import argparse
import sys
import os
import random
import numpy as np
from typing import Dict, List, Any, Optional

# Ensure code directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import local modules
from code.randomwalk import random_walk, compute_hitting_time, compute_commute_time, biased_random_walk
from code.community_detection import louvain_method, spectral_clustering, label_propagation
from code.centrality import compute_centralities, print_centrality_measures
from code.mcl import mcl, get_clusters
from code.pagerank import pagerank
from code.visualization import (
    visualize_graph, visualize_communities, visualize_centrality, visualize_path
)
from code.utils import (
    create_random_graph, create_scale_free_graph, create_small_world_graph,
    load_karate_club, generate_community_graph, compute_graph_metrics
)
from code.randomwalk import random_walk_to_target_no_edge_repeats

def parse_arguments():
    """Parse command line arguments for the application."""
    parser = argparse.ArgumentParser(
        description="Social Network Analysis Tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --action visualize --graph-type random --nodes 20
  python main.py --action centrality --graph-type karate 
  python main.py --action community --graph-type scale-free --nodes 30
  python main.py --action random-walk --graph-type small-world
  python main.py --action metrics --graph-file network.gexf
"""
    )
    
    # Graph source options
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--graph-type', choices=['random', 'scale-free', 'small-world', 'karate'],
                      help='Type of graph to generate')
    group.add_argument('--graph-file', type=str, help='Load graph from file (GEXF, GraphML, GML, etc.)')
    
    # Actions
    parser.add_argument('--action', required=True, 
                        choices=['visualize', 'random-walk', 'centrality', 
                                 'community', 'mcl', 'pagerank', 'metrics'],
                        help='Analysis action to perform')
    
    # Graph generation parameters
    parser.add_argument('--nodes', type=int, default=20, 
                        help='Number of nodes for generated graphs')
    parser.add_argument('--p', type=float, default=0.2, 
                        help='Edge probability for random graphs / rewiring probability for small-world')
    parser.add_argument('--m', type=int, default=2, 
                        help='Number of edges to attach from new node to existing nodes in scale-free graph')
    parser.add_argument('--k', type=int, default=4, 
                        help='Each node connected to k nearest neighbors in small-world graph')
    
    # Algorithm parameters
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    parser.add_argument('--viz-layout', default='spring', 
                        choices=['spring', 'circular', 'kamada_kawai', 'spectral'],
                        help='Layout algorithm for visualization')
    
    # Output options
    parser.add_argument('--output', type=str, help='Save output to file')
    parser.add_argument('--no-display', action='store_true', help='Do not display figures')
    
    return parser.parse_args()

def load_graph(args):
    """Load or generate a graph based on command line arguments."""
    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)
    
    if args.graph_file:
        try:
            # Determine file format from extension
            file_ext = os.path.splitext(args.graph_file)[1].lower()
            if file_ext == '.gexf':
                G = nx.read_gexf(args.graph_file)
            elif file_ext == '.graphml':
                G = nx.read_graphml(args.graph_file)
            elif file_ext == '.gml':
                G = nx.read_gml(args.graph_file)
            elif file_ext == '.edgelist':
                G = nx.read_edgelist(args.graph_file)
            else:
                print(f"Unsupported file format: {file_ext}")
                sys.exit(1)
            print(f"Loaded graph from {args.graph_file} with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        except Exception as e:
            print(f"Error loading graph: {e}")
            sys.exit(1)
    elif args.graph_type == 'random':
        G = create_random_graph(args.nodes, args.p, seed=args.seed)
        print(f"Generated random graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    elif args.graph_type == 'scale-free':
        G = nx.barabasi_albert_graph(args.nodes, args.m, seed=args.seed)
        print(f"Generated scale-free graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    elif args.graph_type == 'small-world':
        G = create_small_world_graph(args.nodes, args.k, args.p, seed=args.seed)
        print(f"Generated small-world graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    elif args.graph_type == 'karate':
        G = load_karate_club()
        print(f"Loaded Zachary's karate club graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    else:
        print("No graph source specified")
        sys.exit(1)
    
    return G

def action_visualize(G, args):
    """Visualize a graph."""
    visualize_graph(G, title=f"Graph Visualization", layout=args.viz_layout)

def action_random_walk(G, args):
    """Perform and visualize random walks on a graph."""
    # Choose source and target nodes
    nodes = list(G.nodes())
    source = random.choice(nodes)
    target = random.choice([n for n in nodes if n != source])
    
    # Standard random walk
    walk = random_walk(G, source, 10)
    print(f"Random walk from {source} (10 steps): {' → '.join(map(str, walk))}")
    
    # Biased random walk (if graph has degree variance)
    if len(set(dict(G.degree()).values())) > 1:
        biased_walk = biased_random_walk(G, source, 10, 'weight')
        print(f"Biased random walk from {source} (10 steps): {' → '.join(map(str, biased_walk))}")
    
    # Edge-simple random walk to target
    path, reached = random_walk_to_target_no_edge_repeats(G, source, target)
    print(f"Edge-simple random walk from {source} to {target}:")
    print(f"  Reached: {reached}")
    print(f"  Path length: {len(path)}")
    print(f"  Path: {' → '.join(map(str, path))}")
    
    # Hitting and commute time
    try:
        hit_time = compute_hitting_time(G, source, target, simulations=50)
        commute_time = compute_commute_time(G, source, target, simulations=50)
        print(f"Average hitting time {source} → {target}: {hit_time:.2f}")
        print(f"Average commute time {source} ⟷ {target}: {commute_time:.2f}")
    except Exception as e:
        print(f"Error computing hitting/commute time: {e}")
    
    # Visualize the path if target was reached
    if reached:
        visualize_path(G, path, title=f"Random Walk from {source} to {target}")

def action_centrality(G, args):
    """Compute and visualize centrality measures."""
    centralities = compute_centralities(G)
    print_centrality_measures(centralities)
    
    # Visualize degree centrality
    visualize_centrality(G, centralities["degree"], title="Degree Centrality")
    
    # Visualize betweenness centrality
    visualize_centrality(G, centralities["betweenness"], title="Betweenness Centrality")

def action_community(G, args):
    """Detect and visualize communities in a graph."""
    print("Detecting communities using Louvain method...")
    try:
        communities = louvain_method(G)
        
        # Count communities and their sizes
        comm_sizes = {}
        for node, comm in communities.items():
            comm_sizes[comm] = comm_sizes.get(comm, 0) + 1
        
        print(f"Found {len(comm_sizes)} communities:")
        for comm, size in comm_sizes.items():
            print(f"  Community {comm}: {size} nodes")
        
        # Visualize communities
        visualize_communities(G, communities, title="Communities (Louvain Method)")
    except Exception as e:
        print(f"Error in community detection: {e}")

def action_mcl(G, args):
    """Perform MCL clustering and visualize results."""
    print("Performing MCL clustering...")
    try:
        # Convert to undirected if directed
        if nx.is_directed(G):
            G = G.to_undirected()
            
        M = mcl(G, expand_power=2, inflate_power=2, iterations=20)
        nodes = list(G.nodes())
        clusters = get_clusters(M, nodes)
        
        print(f"Found {len(clusters)} clusters:")
        for i, cluster in enumerate(clusters):
            print(f"  Cluster {i+1}: {len(cluster)} nodes - {', '.join(map(str, list(cluster)[:5]))}" + 
                  ("..." if len(cluster) > 5 else ""))
        
        # Convert clusters to communities format for visualization
        comm_id_map = {}
        for i, cluster in enumerate(clusters):
            for node in cluster:
                comm_id_map[node] = i
                
        visualize_communities(G, comm_id_map, title="MCL Clustering")
    except Exception as e:
        print(f"Error in MCL clustering: {e}")

def action_pagerank(G, args):
    """Compute and visualize PageRank scores."""
    # Ensure graph is directed
    if not nx.is_directed(G):
        G = G.to_directed()
    
    print("Computing PageRank...")
    try:
        ranks = pagerank(G)
        
        # Get top nodes by PageRank
        sorted_ranks = sorted(ranks.items(), key=lambda x: x[1], reverse=True)
        
        print("Top nodes by PageRank:")
        for node, rank in sorted_ranks[:min(10, len(sorted_ranks))]:
            print(f"  {node}: {rank:.6f}")
        
        # Visualize PageRank
        visualize_centrality(G, ranks, title="PageRank Scores")
    except Exception as e:
        print(f"Error computing PageRank: {e}")

def action_metrics(G, args):
    """Compute and display various graph metrics."""
    print("Computing graph metrics...")
    metrics = compute_graph_metrics(G)
    
    print("\nGraph Metrics:")
    print("=" * 40)
    for key, value in metrics.items():
        print(f"{key}: {value}")

def main():
    """Main entry point for the application."""
    args = parse_arguments()
    
    # Load or generate graph
    G = load_graph(args)
    
    # Perform the requested action
    if args.action == 'visualize':
        action_visualize(G, args)
    elif args.action == 'random-walk':
        action_random_walk(G, args)
    elif args.action == 'centrality':
        action_centrality(G, args)
    elif args.action == 'community':
        action_community(G, args)
    elif args.action == 'mcl':
        action_mcl(G, args)
    elif args.action == 'pagerank':
        action_pagerank(G, args)
    elif args.action == 'metrics':
        action_metrics(G, args)
    
    # Save output if requested
    if args.output and plt.get_fignums():
        plt.savefig(args.output)
        print(f"Output saved to {args.output}")
    
    # Show plots if not disabled
    if not args.no_display and plt.get_fignums():
        plt.show()

if __name__ == "__main__":
    main()
