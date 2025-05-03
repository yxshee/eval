import networkx as nx
from typing import Dict, Any

def pagerank(G: nx.DiGraph, damping: float = 0.85, max_iterations: int = 100, 
            tolerance: float = 1e-6) -> Dict[Any, float]:
    """
    Custom implementation of PageRank algorithm.
    
    Args:
        G: NetworkX directed graph
        damping: Damping factor (typically 0.85)
        max_iterations: Maximum number of iterations
        tolerance: Convergence tolerance
        
    Returns:
        Dictionary mapping nodes to their PageRank scores
    """
    # Initialize
    N = G.number_of_nodes()
    ranks = {node: 1 / N for node in G}  # initial rank for each node
    
    for i in range(max_iterations):
        new_ranks = {}
        # Calculate rank update for each node
        for node in G:
            rank_sum = 0
            # Sum contributions from incoming edges
            for neighbor in G.predecessors(node):
                out_degree = G.out_degree(neighbor)
                if out_degree > 0:
                    rank_sum += ranks[neighbor] / out_degree
            
            # Apply PageRank formula
            new_ranks[node] = (1 - damping) / N + damping * rank_sum
        
        # Check for convergence
        diff = sum(abs(new_ranks[node] - ranks[node]) for node in G)
        ranks = new_ranks
        
        if diff < tolerance:
            break
            
    return ranks

def nx_pagerank(G: nx.Graph, damping: float = 0.85, max_iterations: int = 100) -> Dict[Any, float]:
    """
    Wrapper for NetworkX's built-in PageRank implementation.
    
    Args:
        G: NetworkX graph
        damping: Damping factor
        max_iterations: Maximum number of iterations
        
    Returns:
        Dictionary mapping nodes to their PageRank scores
    """
    return nx.pagerank(G, alpha=damping, max_iter=max_iterations)
