import networkx as nx
import random
from typing import List, Any, Dict, Tuple

def random_walk(G: nx.Graph, start_node: Any, wlen: int) -> List[Any]:
    """
    Perform a simple random walk on graph G.
    
    Args:
        G: NetworkX graph
        start_node: Starting node for the walk
        wlen: Length of the walk
        
    Returns:
        List of nodes in the walk
    """
    current = start_node
    walk = [start_node]
    
    for i in range(wlen-1):
        neighbours = list(G.neighbors(current))
        if neighbours:
            next_node = random.choice(neighbours)
            walk.append(next_node)
            current = next_node
        else:
            break
            
    return walk

def random_walk_until_target(G: nx.Graph, start: Any, target: Any) -> int:
    """
    Perform a random walk until target node is reached.
    
    Args:
        G: NetworkX graph
        start: Starting node
        target: Target node to reach
        
    Returns:
        Number of steps taken to reach target
    """
    steps = 0
    current = start
    
    while current != target:
        neighbours = list(G.neighbors(current))
        if not neighbours:
            return float('inf')  # Target unreachable
        current = random.choice(neighbours)
        steps += 1
    
    return steps

def compute_hitting_time(G: nx.Graph, start: Any, target: Any, simulations: int = 1000) -> float:
    """
    Compute average hitting time from start to target.
    
    Args:
        G: NetworkX graph
        start: Starting node
        target: Target node 
        simulations: Number of random walks to simulate
        
    Returns:
        Average hitting time
    """
    if start == target:
        return 0.0
        
    total_steps = 0
    for _ in range(simulations):
        total_steps += random_walk_until_target(G, start, target)
    return total_steps / simulations

def compute_commute_time(G: nx.Graph, start: Any, target: Any, simulations: int = 1000) -> float:
    """
    Compute commute time between start and target.
    
    Args:
        G: NetworkX graph
        start: First node
        target: Second node
        simulations: Number of random walks to simulate
        
    Returns:
        Average commute time
    """
    hit_start_to_target = compute_hitting_time(G, start, target, simulations)
    hit_target_to_start = compute_hitting_time(G, target, start, simulations)
    return hit_start_to_target + hit_target_to_start

def biased_random_walk(G: nx.Graph, start_node: Any, wlen: int, weight: str = 'weight') -> List[Any]:
    """
    Perform a biased random walk based on edge weights.
    
    Args:
        G: NetworkX graph
        start_node: Starting node for the walk
        wlen: Length of the walk
        weight: Edge attribute to use as weight
        
    Returns:
        List of nodes in the walk
    """
    current = start_node
    walk = [start_node]
    
    for i in range(wlen-1):
        neighbors = list(G.neighbors(current))
        if not neighbors:
            break
            
        weights = []
        for neighbor in neighbors:
            edge_data = G.get_edge_data(current, neighbor)
            w = edge_data.get(weight, 1.0)
            weights.append(w)
            
        # Normalize weights
        total = sum(weights)
        if total == 0:
            probabilities = [1/len(weights)] * len(weights)
        else:
            probabilities = [w/total for w in weights]
            
        next_node = random.choices(neighbors, weights=probabilities)[0]
        walk.append(next_node)
        current = next_node
            
    return walk
