import networkx as nx
import numpy as np
from typing import Dict, List, Set, Any, Tuple
from collections import defaultdict

def louvain_method(G: nx.Graph, resolution: float = 1.0) -> Dict[Any, int]:
    """
    Simple implementation of Louvain method for community detection.
    This is a simplified version - for production use, consider networkx.community.louvain_communities
    
    Args:
        G: NetworkX graph
        resolution: Resolution parameter controlling community size
        
    Returns:
        Dictionary mapping nodes to community IDs
    """
    # Initialize each node to its own community
    communities = {node: i for i, node in enumerate(G.nodes())}
    
    # Helper function to calculate modularity gain
    def modularity_gain(node, community, communities, G, m):
        k_in = sum(G[node].get(neighbor, {}).get('weight', 1) for neighbor in G[node] 
                   if communities[neighbor] == community)
        k = sum(G[node].get(neighbor, {}).get('weight', 1) for neighbor in G[node])
        tot = sum(sum(G[n1].get(n2, {}).get('weight', 1) for n2 in G[n1]) 
                  for n1 in G if communities[n1] == community)
        
        return k_in - resolution * k * tot / (2 * m)
    
    # Phase 1: Optimize modularity locally
    improvement = True
    while improvement:
        improvement = False
        
        # Calculate total edge weight
        m = sum(G[u][v].get('weight', 1) for u, v in G.edges())
        
        # For each node, try moving it to neighboring communities
        for node in G.nodes():
            # Get neighboring communities
            neighbor_communities = {communities[neighbor] 
                                  for neighbor in G.neighbors(node) 
                                  if communities[neighbor] != communities[node]}
            best_community = communities[node]
            best_gain = 0
            
            # Check each neighboring community
            for community in neighbor_communities:
                gain = modularity_gain(node, community, communities, G, m)
                if gain > best_gain:
                    best_community = community
                    best_gain = gain
            
            # Move to best community if there's improvement
            if best_community != communities[node]:
                communities[node] = best_community
                improvement = True
    
    # Renumber communities to be consecutive
    unique_communities = set(communities.values())
    mapping = {old_id: new_id for new_id, old_id in enumerate(unique_communities)}
    communities = {node: mapping[community] for node, community in communities.items()}
    
    return communities

def girvan_newman_step(G: nx.Graph) -> Tuple[Set[Any], Set[Any]]:
    """
    Perform one step of Girvan-Newman community detection.
    Removes edge with highest betweenness centrality.
    
    Args:
        G: NetworkX graph
        
    Returns:
        Tuple of the two communities created by removing the edge
    """
    # Find edge with highest betweenness centrality
    edge_betweenness = nx.edge_betweenness_centrality(G)
    max_edge = max(edge_betweenness.items(), key=lambda x: x[1])[0]
    
    # Remove the edge
    G.remove_edge(*max_edge)
    
    # Get the two components
    components = list(nx.connected_components(G))
    if len(components) > 1:
        return components[0], components[1]
    else:
        return set(), set()

def spectral_clustering(G: nx.Graph, k: int = 2) -> Dict[Any, int]:
    """
    Perform spectral clustering to find communities.
    
    Args:
        G: NetworkX graph
        k: Number of communities
        
    Returns:
        Dictionary mapping nodes to community IDs
    """
    # Get the Laplacian matrix
    L = nx.normalized_laplacian_matrix(G)
    
    # Get eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(L.toarray())
    
    # Sort eigenvectors by eigenvalues
    idx = eigenvalues.argsort()[1:k+1]  # Skip the first eigenvalue (which is 0)
    
    # Get the k smallest non-zero eigenvectors
    X = eigenvectors[:, idx]
    
    # Use k-means to cluster the nodes
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X)
    
    # Map nodes to communities
    node_to_community = {node: int(kmeans.labels_[i]) 
                         for i, node in enumerate(G.nodes())}
    
    return node_to_community

def label_propagation(G: nx.Graph, max_iterations: int = 10) -> Dict[Any, int]:
    """
    Label Propagation Algorithm for community detection.
    
    Args:
        G: NetworkX graph
        max_iterations: Maximum number of iterations
        
    Returns:
        Dictionary mapping nodes to community IDs
    """
    # Initialize each node with a unique label
    labels = {node: i for i, node in enumerate(G.nodes())}
    
    for _ in range(max_iterations):
        # Shuffle node processing order
        nodes = list(G.nodes())
        random.shuffle(nodes)
        
        # Track if any label changed in this iteration
        changed = False
        
        for node in nodes:
            # Count labels of neighbors
            neighbor_labels = defaultdict(int)
            for neighbor in G.neighbors(node):
                neighbor_labels[labels[neighbor]] += 1
                
            if not neighbor_labels:
                continue
                
            # Find the most common label
            max_count = max(neighbor_labels.values())
            best_labels = [label for label, count in neighbor_labels.items() 
                          if count == max_count]
            
            # Choose one of the most common labels
            new_label = random.choice(best_labels)
            
            # Update label if different
            if new_label != labels[node]:
                labels[node] = new_label
                changed = True
        
        # If no labels changed, algorithm has converged
        if not changed:
            break
    
    # Renumber communities to be consecutive
    unique_labels = set(labels.values())
    mapping = {old_label: new_label for new_label, old_label in enumerate(unique_labels)}
    labels = {node: mapping[label] for node, label in labels.items()}
    
    return labels
