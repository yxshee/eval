import networkx as nx
import numpy as np
import random
from typing import List, Dict, Any, Tuple, Optional, Union

def create_random_graph(n: int, p: float, directed: bool = False, seed: Optional[int] = None) -> nx.Graph:
    """
    Create a random Erdős-Rényi graph.
    
    Args:
        n: Number of nodes
        p: Probability of edge creation
        directed: Whether to create a directed graph
        seed: Random seed for reproducibility
        
    Returns:
        NetworkX graph
    """
    if directed:
        return nx.erdos_renyi_graph(n, p, directed=True, seed=seed)
    else:
        return nx.erdos_renyi_graph(n, p, seed=seed)

def create_scale_free_graph(n: int, seed: Optional[int] = None) -> nx.Graph:
    """
    Create a scale-free (preferential attachment) graph.
    
    Args:
        n: Number of nodes
        seed: Random seed for reproducibility
        
    Returns:
        NetworkX graph
    """
    return nx.barabasi_albert_graph(n, m=2, seed=seed)

def create_small_world_graph(n: int, k: int = 4, p: float = 0.1, seed: Optional[int] = None) -> nx.Graph:
    """
    Create a small-world graph using the Watts-Strogatz model.
    
    Args:
        n: Number of nodes
        k: Each node is connected to k nearest neighbors
        p: Probability of rewiring each edge
        seed: Random seed for reproducibility
        
    Returns:
        NetworkX graph
    """
    return nx.watts_strogatz_graph(n, k, p, seed=seed)

def load_karate_club() -> nx.Graph:
    """
    Load the classic Zachary's Karate Club network dataset.
    
    Returns:
        NetworkX graph of the karate club
    """
    return nx.karate_club_graph()

def generate_community_graph(communities: int = 3, nodes_per_community: int = 10, 
                            p_in: float = 0.7, p_out: float = 0.01, 
                            seed: Optional[int] = None) -> Tuple[nx.Graph, Dict[Any, int]]:
    """
    Generate a graph with community structure.
    
    Args:
        communities: Number of communities
        nodes_per_community: Nodes in each community
        p_in: Probability of intra-community edges
        p_out: Probability of inter-community edges
        seed: Random seed
        
    Returns:
        Tuple of (graph, node_to_community_dict)
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    total_nodes = communities * nodes_per_community
    G = nx.Graph()
    G.add_nodes_from(range(total_nodes))
    
    # Track community membership
    node_to_community = {}
    
    # Add edges based on community membership
    for i in range(total_nodes):
        community_i = i // nodes_per_community
        node_to_community[i] = community_i
        
        for j in range(i + 1, total_nodes):
            community_j = j // nodes_per_community
            
            # Determine edge probability based on community membership
            if community_i == community_j:
                prob = p_in
            else:
                prob = p_out
            
            # Add edge with given probability
            if random.random() < prob:
                G.add_edge(i, j)
    
    return G, node_to_community

def convert_to_weighted(G: nx.Graph, weight_range: Tuple[float, float] = (1.0, 10.0), 
                       seed: Optional[int] = None) -> nx.Graph:
    """
    Convert an unweighted graph to a weighted graph by assigning random weights.
    
    Args:
        G: NetworkX graph
        weight_range: Range for random weights (min, max)
        seed: Random seed
        
    Returns:
        NetworkX weighted graph
    """
    if seed is not None:
        random.seed(seed)
    
    # Create a copy of the graph
    G_weighted = G.copy()
    
    # Assign random weights to edges
    for u, v in G_weighted.edges():
        G_weighted[u][v]['weight'] = random.uniform(*weight_range)
    
    return G_weighted

def compute_graph_metrics(G: nx.Graph) -> Dict[str, Any]:
    """
    Compute various metrics for a graph.
    
    Args:
        G: NetworkX graph
        
    Returns:
        Dictionary of metric names to values
    """
    metrics = {}
    
    # Basic metrics
    metrics['nodes'] = G.number_of_nodes()
    metrics['edges'] = G.number_of_edges()
    metrics['density'] = nx.density(G)
    
    # Connected components
    if nx.is_directed(G):
        metrics['strongly_connected_components'] = nx.number_strongly_connected_components(G)
        metrics['weakly_connected_components'] = nx.number_weakly_connected_components(G)
    else:
        metrics['connected_components'] = nx.number_connected_components(G)
    
    # Try to compute metrics that might fail for disconnected graphs
    try:
        metrics['diameter'] = nx.diameter(G)
    except nx.NetworkXError:
        metrics['diameter'] = float('inf')
    
    try:
        metrics['average_shortest_path_length'] = nx.average_shortest_path_length(G)
    except nx.NetworkXError:
        metrics['average_shortest_path_length'] = float('nan')
    
    # Other metrics
    metrics['average_clustering'] = nx.average_clustering(G)
    metrics['transitivity'] = nx.transitivity(G)
    metrics['is_connected'] = nx.is_connected(G)
    
    return metrics
