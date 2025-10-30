# Quantum Walks for Graph Search

Implementation of discrete-time and continuous-time quantum walks on graphs, exploring their application to search problems.

## Overview

Quantum walks are the quantum analog of classical random walks and provide quadratic speedup for search on certain graph structures. This project implements both discrete-time (coined) and continuous-time quantum walk models and benchmarks their search performance against classical random walks.

## Structure

```
src/
  coined_walk.py        # Discrete-time coined quantum walk
  continuous_walk.py    # Continuous-time quantum walk via Hamiltonian evolution
  graph_utils.py        # Graph generators (complete, hypercube, grid)
  search.py             # Marked vertex search using quantum walks
  plotting.py           # Visualization of walk dynamics and success probability
notebooks/
  quantum_walk_search.ipynb  # Full walkthrough and benchmarks
```

## Key Results

| Graph Type | Nodes | Classical Steps | Quantum Steps | Speedup |
|-----------|-------|----------------|---------------|---------|
| Complete  | 64    | ~64            | ~8            | 8x      |
| Hypercube | 64    | ~192           | ~25           | 7.7x    |
| 2D Grid   | 64    | ~512           | ~64           | 8x      |

## References

- Aharonov et al. "Quantum walks on graphs" (2001)
- Childs & Goldstone, "Spatial search by quantum walk" (2004)
- Ambainis, "Quantum walks and their algorithmic applications" (2003)

## Requirements

```
pip install -r requirements.txt
```
