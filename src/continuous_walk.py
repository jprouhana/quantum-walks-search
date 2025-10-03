"""
Continuous-time quantum walk via Hamiltonian evolution.
"""

import numpy as np
from scipy.linalg import expm
import networkx as nx


def adjacency_hamiltonian(graph):
    """
    Build the Hamiltonian from the graph adjacency matrix.
    H = -gamma * A where A is the adjacency matrix.
    """
    return np.array(nx.adjacency_matrix(graph).todense(), dtype=float)


def evolve_continuous_walk(graph, initial_node, time, gamma=1.0):
    """
    Evolve a continuous-time quantum walk on a graph.

    The state evolves as |psi(t)> = exp(-i * gamma * A * t) |initial>

    Args:
        graph: networkx Graph
        initial_node: starting node index
        time: evolution time
        gamma: coupling constant

    Returns:
        dict with 'probabilities' (array) and 'state' (array)
    """
    n = graph.number_of_nodes()
    A = adjacency_hamiltonian(graph)

    # initial state: localized at initial_node
    psi_0 = np.zeros(n, dtype=complex)
    psi_0[initial_node] = 1.0

    # time evolution
    U = expm(-1j * gamma * A * time)
    psi_t = U @ psi_0

    probabilities = np.abs(psi_t) ** 2

    return {
        'probabilities': probabilities,
        'state': psi_t,
    }


def sweep_evolution(graph, initial_node, time_range, gamma=1.0):
    """
    Sweep continuous-time evolution over a range of times.

    Returns:
        dict with 'times' and 'prob_matrix' (shape: n_times x n_nodes)
    """
    n = graph.number_of_nodes()
    prob_matrix = np.zeros((len(time_range), n))

    for i, t in enumerate(time_range):
        result = evolve_continuous_walk(graph, initial_node, t, gamma)
        prob_matrix[i] = result['probabilities']

    return {
        'times': np.array(time_range),
        'prob_matrix': prob_matrix,
    }
