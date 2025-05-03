# Social Networks Algorithms


<img width="557" alt="Graph Visualization" src="https://github.com/user-attachments/assets/c9534239-2e22-467b-aadf-bad4e63329a0" />


## 📊 Overview

This repository contains implementations of random walk algorithms on graphs, primarily focused on edge-simple random walks. These algorithms are useful for:

- Network exploration strategies
- Graph traversal with constraints
- Social network analysis
- Measuring node importance

## 🧮 Algorithms Implemented

| Algorithm | Description | File |
|-----------|-------------|------|
| Edge-Simple Random Walk | Random walk that never traverses the same edge twice | [`randomwalk.py`](random%20walk/randomwalk.py) |
| Target-Seeking Walk | Edge-simple random walk that attempts to reach a specified target | [`final.py`](random%20walk/final.py) |

## 🖼️ Visualizations

The code produces two main types of visualizations:

1. **Initial Network Configuration**:  
   Shows the complete graph with source (green) and target (red) nodes highlighted.

2. **Path Visualization**:  
   If the random walk successfully reaches the target, it displays the path taken.

## 🚀 Usage

### Random Graph Example

```python
# Generate a random Erdős–Rényi graph and perform a random walk
import networkx as nx
from random_walk.randomwalk import random_walk_to_target_no_edge_repeats

# Create random graph
G = nx.erdos_renyi_graph(12, 0.25)
source, target = "n0", "n5"

# Run algorithm
path, reached = random_walk_to_target_no_edge_repeats(G, source, target)
print(f"Reached target? {reached}")
print("Path:", " → ".join(path))
```


## ⚙️ How It Works

The edge-simple random walk algorithm:

1. Starts at a designated source node
2. At each step, randomly selects an unused edge
3. Never traverses the same edge twice
4. Terminates when:
   - The target node is reached (success)
   - There are no unused edges available (dead end)
   - Maximum steps are exceeded

## 🧪 Key Features

- Type annotations for better code readability
- Visualization of both graphs and paths
- Configurable maximum steps for walk length
- Support for any NetworkX graph type

## 📚 Dependencies

- NetworkX
- Matplotlib
- Python 3.6+

