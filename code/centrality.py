import networkx as nx
from typing import Dict, Any

def compute_centralities(G: nx.Graph) -> Dict[str, Dict[Any, float]]:
    """
    Compute multiple centrality measures for a graph.
    
    Args:
        G: NetworkX graph
        
    Returns:
        Dictionary with different centrality measures
    """
    # Calculate various centrality measures
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    
    # Proximity prestige (interpretable like closeness centrality)
    proximity_prestige = closeness_centrality
    
    return {
        "degree": degree_centrality,
        "closeness": closeness_centrality,
        "betweenness": betweenness_centrality,
        "proximity_prestige": proximity_prestige
    }

def print_centrality_measures(centralities: Dict[str, Dict[Any, float]]) -> None:
    """
    Print centrality measures in a readable format.
    
    Args:
        centralities: Dictionary with centrality measures
    """
    print("Degree Centrality:")
    for node, centrality in centralities["degree"].items():
        print(f"{node}: {centrality:.2f}")

    print("\nCloseness Centrality:")
    for node, centrality in centralities["closeness"].items():
        print(f"{node}: {centrality:.2f}")

    print("\nBetweenness Centrality:")
    for node, centrality in centralities["betweenness"].items():
        print(f"{node}: {centrality:.2f}")

    print("\nProximity Prestige (same as normalized Closeness Centrality):")
    for node, prestige in centralities["proximity_prestige"].items():
        print(f"{node}: {prestige:.2f}")
