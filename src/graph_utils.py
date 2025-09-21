"""
Graph generators for quantum walk experiments.
"""

import networkx as nx
import numpy as np


def build_complete_graph(n):
    """Complete graph on n nodes."""
    return nx.complete_graph(n)


def build_hypercube(dimension):
    """Hypercube graph of given dimension (2^d nodes)."""
    return nx.hypercube_graph(dimension)


def build_grid_2d(rows, cols):
    """2D grid graph."""
    return nx.grid_2d_graph(rows, cols)


def build_cycle(n):
    """Cycle graph on n nodes."""
    return nx.cycle_graph(n)


def build_star(n):
    """Star graph with n-1 leaves."""
    return nx.star_graph(n - 1)


def classical_hitting_time(graph, start, target, n_trials=10000, seed=42):
    """
    Estimate classical random walk hitting time via Monte Carlo.

    Returns average number of steps to reach target from start.
    """
    rng = np.random.RandomState(seed)
    total_steps = 0
    nodes = list(graph.nodes())
    node_to_idx = {node: i for i, node in enumerate(nodes)}

    for _ in range(n_trials):
        current = start
        steps = 0
        while current != target:
            neighbors = list(graph.neighbors(current))
            current = neighbors[rng.randint(len(neighbors))]
            steps += 1
            if steps > 10 * len(nodes) ** 2:
                break
        total_steps += steps

    return total_steps / n_trials


def get_graph_builders():
    """Return dict of graph builder functions and their names."""
    return {
        'Complete': lambda n: build_complete_graph(n),
        'Cycle': lambda n: build_cycle(n),
        'Star': lambda n: build_star(n),
    }
