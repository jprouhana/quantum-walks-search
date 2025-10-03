"""
Quantum walk-based search for marked vertices.
"""

import numpy as np
from scipy.linalg import expm
import networkx as nx
from .graph_utils import adjacency_hamiltonian


def build_search_hamiltonian(graph, marked_vertex, gamma=1.0):
    """
    Build the search Hamiltonian: H = -gamma * A + |w><w|
    where |w> is the marked vertex.

    The oracle term |w><w| adds energy to the marked state,
    creating a spectral gap that drives the walk toward it.
    """
    n = graph.number_of_nodes()
    A = np.array(nx.adjacency_matrix(graph).todense(), dtype=float)

    # oracle projector
    oracle = np.zeros((n, n))
    oracle[marked_vertex, marked_vertex] = 1.0

    H = -gamma * A + oracle
    return H


def search_continuous_walk(graph, marked_vertex, gamma=None, time=None,
                            n_time_steps=200):
    """
    Search for a marked vertex using continuous-time quantum walk.

    Starts from uniform superposition and evolves under the search
    Hamiltonian. Returns the optimal time and success probability.

    Args:
        graph: networkx Graph
        marked_vertex: index of the marked vertex
        gamma: coupling constant (auto-computed if None)
        time: total evolution time (auto-computed if None)
        n_time_steps: resolution of time sweep

    Returns:
        dict with 'optimal_time', 'max_probability', 'prob_over_time'
    """
    n = graph.number_of_nodes()

    if gamma is None:
        gamma = 1.0 / n

    if time is None:
        time = np.pi / 2 * np.sqrt(n)

    times = np.linspace(0, time, n_time_steps)

    # initial state: uniform superposition
    psi_0 = np.ones(n, dtype=complex) / np.sqrt(n)

    H = build_search_hamiltonian(graph, marked_vertex, gamma)

    success_probs = np.zeros(len(times))
    for i, t in enumerate(times):
        U = expm(-1j * H * t)
        psi_t = U @ psi_0
        success_probs[i] = np.abs(psi_t[marked_vertex]) ** 2

    optimal_idx = np.argmax(success_probs)

    return {
        'optimal_time': times[optimal_idx],
        'max_probability': success_probs[optimal_idx],
        'times': times,
        'success_probs': success_probs,
    }


def benchmark_search(graph_builder, node_counts, marked_vertex=0,
                      n_time_steps=200):
    """
    Benchmark quantum walk search across different graph sizes.

    Returns:
        dict with 'n_nodes', 'optimal_times', 'max_probs'
    """
    optimal_times = []
    max_probs = []

    for n in node_counts:
        print(f"  Searching on {n} nodes...", end=" ")
        graph = graph_builder(n)
        result = search_continuous_walk(graph, marked_vertex,
                                         n_time_steps=n_time_steps)
        optimal_times.append(result['optimal_time'])
        max_probs.append(result['max_probability'])
        print(f"P={result['max_probability']:.4f} at t={result['optimal_time']:.2f}")

    return {
        'n_nodes': list(node_counts),
        'optimal_times': optimal_times,
        'max_probs': max_probs,
    }
