# Social Networks Analysis

<img width="557" alt="Graph Visualization" src="https://github.com/user-attachments/assets/c9534239-2e22-467b-aadf-bad4e63329a0" />

## 📊 Overview

This repository contains implementations of various social network analysis algorithms, including random walks, centrality measures, community detection, and graph visualization techniques. These algorithms are useful for:

- Network exploration and navigation
- Identifying influential nodes
- Community structure detection
- Information flow analysis
- Network resilience assessment

## 🧮 Algorithms Implemented

| Category | Algorithms | Files |
|----------|------------|-------|
| **Random Walks** | Simple Random Walks, Biased Random Walks, Edge-Simple Walks, Hitting & Commute Time | [`random_walks.py`](code/random_walks.py), [`randomwalk.py`](code/randomwalk.py) |
| **Centrality Measures** | Degree, Closeness, Betweenness, Proximity Prestige | [`centrality.py`](code/centrality.py) |
| **Community Detection** | MCL, Louvain, Spectral Clustering, Label Propagation | [`mcl.py`](code/mcl.py), [`community_detection.py`](code/community_detection.py) |
| **Ranking** | PageRank | [`pagerank.py`](code/pagerank.py) |
| **Visualization** | Graph Layouts, Community Visualization, Path Visualization | [`visualization.py`](code/visualization.py) |
| **Utilities** | Graph Generation, Metrics, Network Properties | [`utils.py`](code/utils.py) |

## 🚀 Usage

### Random Walks

```python
import networkx as nx
from code.random_walks import random_walk, compute_hitting_time

# Create a simple graph
G = nx.Graph()
G.add_edges_from([('a','b'), ('a','c'), ('c','d'), ('d','e')])

# Perform a random walk
walk = random_walk(G, start_node='a', wlen=10)
print(f"Random walk from 'a': {walk}")

# Calculate hitting time between nodes
hit_time = compute_hitting_time(G, 'a', 'e', simulations=100)
print(f"Average hitting time from 'a' to 'e': {hit_time:.2f}")
```

### Community Detection

```python
import networkx as nx
from code.community_detection import louvain_method
from code.visualization import visualize_communities

# Create a graph with community structure
G = nx.karate_club_graph()

# Detect communities using Louvain method
communities = louvain_method(G)

# Visualize the communities
visualize_communities(G, communities, title="Zachary's Karate Club Communities")
```

### Centrality Measures

```python
import networkx as nx
from code.centrality import compute_centralities, print_centrality_measures

# Create a social network
G = nx.Graph()
G.add_edges_from([
    ('Alice', 'Bob'), ('Alice', 'Charlie'),
    ('Bob', 'David'), ('Charlie', 'David'),
    ('Charlie', 'Eve'), ('David', 'Eve'),
    ('Eve', 'Frank'), ('Frank', 'Grace')
])

# Compute centrality measures
centralities = compute_centralities(G)
print_centrality_measures(centralities)
```

## 🖼️ Visualization Features

The repository includes multiple visualization utilities:

1. **Basic Graph Visualization**:  
   Various layouts including spring, circular, kamada-kawai, and spectral.

2. **Community Visualization**:  
   Display detected communities with distinct colors.

3. **Centrality Visualization**:  
   Represent node importance through node size and color.

4. **Path Visualization**:  
   Highlight specific paths through networks.

## 📓 Jupyter Notebook

The repository includes a comprehensive Jupyter notebook (`Social Network.ipynb`) that demonstrates the algorithms in action with visualizations and explanations.

## ⚙️ Key Features

- Type annotations for better code readability and IDE support
- Comprehensive visualization options
- Well-documented implementations of fundamental SNA algorithms
- Support for various graph types (directed, undirected, weighted)

## 📚 Dependencies

- NetworkX
- NumPy
- Matplotlib
- Scikit-learn (for some clustering algorithms)
- Python 3.6+

