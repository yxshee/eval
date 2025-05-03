import numpy as np
import networkx as nx
from typing import List, Set, Dict, Any, Tuple

def create_adjacency_matrix(G: nx.Graph) -> np.ndarray:
    """
    Create adjacency matrix with self-loops from NetworkX graph.
    
    Args:
        G: NetworkX graph
        
    Returns:
        NumPy array representing adjacency matrix with self-loops
    """
    A = nx.to_numpy_array(G)
    np.fill_diagonal(A, 1)  # Add self-loops
    return A

def normalize(M: np.ndarray) -> np.ndarray:
    """
    Normalize matrix so columns sum to 1.
    
    Args:
        M: Matrix to normalize
        
    Returns:
        Column-normalized matrix
    """
    column_sums = M.sum(axis=0)
    return M / column_sums

def expand(M: np.ndarray, power: int) -> np.ndarray:
    """
    Expansion step of MCL algorithm.
    
    Args:
        M: Matrix to expand
        power: Power to raise the matrix to
        
    Returns:
        Expanded matrix
    """
    return np.linalg.matrix_power(M, power)

def inflate(M: np.ndarray, inflation_factor: float) -> np.ndarray:
    """
    Inflation step of MCL algorithm.
    
    Args:
        M: Matrix to inflate
        inflation_factor: Inflation parameter
        
    Returns:
        Inflated matrix
    """
    M = np.power(M, inflation_factor)
    return normalize(M)

def mcl(G: nx.Graph, expand_power: int = 2, inflate_power: float = 2.0, 
        iterations: int = 10, convergence_threshold: float = 1e-15) -> np.ndarray:
    """
    Markov Cluster Algorithm for graph clustering.
    
    Args:
        G: NetworkX graph
        expand_power: Power parameter for expansion step
        inflate_power: Power parameter for inflation step
        iterations: Maximum number of iterations
        convergence_threshold: Convergence threshold for early stopping
        
    Returns:
        Final matrix after MCL convergence
    """
    # Initialize with normalized adjacency matrix
    M = create_adjacency_matrix(G)
    M = normalize(M)
    
    prev_M = None
    for i in range(iterations):
        # Store previous matrix for convergence check
        prev_M = M.copy() if i > 0 else None
        
        # Expansion and inflation steps
        M = expand(M, expand_power)
        M = inflate(M, inflate_power)
        
        # Check for convergence
        if prev_M is not None and np.allclose(M, prev_M, atol=convergence_threshold):
            break
            
    return M

def get_clusters(M: np.ndarray, nodes: List[Any], threshold: float = 0.01) -> List[Set[Any]]:
    """
    Extract clusters from MCL result matrix.
    
    Args:
        M: Result matrix from MCL algorithm
        nodes: List of node labels
        threshold: Threshold for considering a connection
        
    Returns:
        List of clusters, where each cluster is a set of nodes
    """
    clusters = []
    seen = set()
    
    for i, row in enumerate(M):
        if nodes[i] not in seen:
            # Collect nodes connected to current node
            cluster = set([nodes[j] for j, val in enumerate(row) if val > threshold])
            
            if cluster:
                clusters.append(cluster)
                seen.update(cluster)
                
    return clusters
