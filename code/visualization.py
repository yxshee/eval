import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
import matplotlib.cm as cm

def visualize_graph(G: nx.Graph, title: str = "Graph Visualization", 
                    layout: str = "spring", node_size: int = 300,
                    edge_width: float = 1.0, figsize: Tuple[int, int] = (10, 8)) -> None:
    """
    Visualize a graph with various layout options.
    
    Args:
        G: NetworkX graph
        title: Plot title
        layout: Layout algorithm ('spring', 'circular', 'kamada_kawai', 'spectral')
        node_size: Size of nodes
        edge_width: Width of edges
        figsize: Figure size as (width, height)
    """
    plt.figure(figsize=figsize)
    
    # Select layout algorithm
    if layout == "spring":
        pos = nx.spring_layout(G, seed=42)
    elif layout == "circular":
        pos = nx.circular_layout(G)
    elif layout == "kamada_kawai":
        pos = nx.kamada_kawai_layout(G)
    elif layout == "spectral":
        pos = nx.spectral_layout(G)
    else:
        pos = nx.spring_layout(G, seed=42)
    
    # Draw the network
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, width=edge_width, alpha=0.7)
    nx.draw_networkx_labels(G, pos, font_size=10)
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def visualize_communities(G: nx.Graph, communities: Dict[Any, int], 
                         title: str = "Community Detection", layout: str = "spring", 
                         figsize: Tuple[int, int] = (10, 8)) -> None:
    """
    Visualize communities in a graph with different colors.
    
    Args:
        G: NetworkX graph
        communities: Dictionary mapping nodes to community IDs
        title: Plot title
        layout: Layout algorithm
        figsize: Figure size
    """
    plt.figure(figsize=figsize)
    
    # Select layout
    if layout == "spring":
        pos = nx.spring_layout(G, seed=42)
    elif layout == "circular":
        pos = nx.circular_layout(G)
    else:
        pos = nx.spring_layout(G, seed=42)
    
    # Get unique communities
    unique_communities = set(communities.values())
    colors = cm.rainbow(np.linspace(0, 1, len(unique_communities)))
    
    # Draw nodes for each community with a different color
    for i, comm_id in enumerate(unique_communities):
        comm_nodes = [node for node, comm in communities.items() if comm == comm_id]
        nx.draw_networkx_nodes(G, pos, nodelist=comm_nodes, 
                               node_color=[colors[i]], label=f"Community {comm_id}")
    
    # Draw edges and labels
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=10)
    
    plt.title(title)
    plt.axis('off')
    plt.legend()
    plt.tight_layout()
    plt.show()

def visualize_centrality(G: nx.Graph, centrality_metric: Dict[Any, float], 
                        title: str = "Node Centrality", figsize: Tuple[int, int] = (10, 8)) -> None:
    """
    Visualize node centrality with node size proportional to centrality.
    
    Args:
        G: NetworkX graph
        centrality_metric: Dictionary mapping nodes to centrality values
        title: Plot title
        figsize: Figure size
    """
    plt.figure(figsize=figsize)
    
    pos = nx.spring_layout(G, seed=42)
    
    # Scale node sizes based on centrality (multiplied for visibility)
    node_sizes = [centrality_metric[node] * 5000 for node in G.nodes()]
    
    # Create a colormap
    node_colors = list(centrality_metric.values())
    
    # Draw the network
    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                                   node_color=node_colors, cmap=plt.cm.viridis)
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    nx.draw_networkx_labels(G, pos)
    
    # Add colorbar
    plt.colorbar(nodes)
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def visualize_path(G: nx.Graph, path: List[Any], title: str = "Path Visualization", 
                  figsize: Tuple[int, int] = (10, 8)) -> None:
    """
    Visualize a path in a graph.
    
    Args:
        G: NetworkX graph
        path: List of nodes representing the path
        title: Plot title
        figsize: Figure size
    """
    plt.figure(figsize=figsize)
    
    pos = nx.spring_layout(G, seed=42)
    
    # Create edge list from path
    path_edges = list(zip(path, path[1:]))
    
    # Draw all nodes and edges
    nx.draw_networkx_nodes(G, pos, node_color='lightgray', alpha=0.6)
    nx.draw_networkx_edges(G, pos, alpha=0.2)
    
    # Highlight the path
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red')
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    
    # Highlight start and end nodes
    nx.draw_networkx_nodes(G, pos, nodelist=[path[0]], node_color='green', node_size=500)
    nx.draw_networkx_nodes(G, pos, nodelist=[path[-1]], node_color='blue', node_size=500)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos)
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
