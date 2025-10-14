"""
Visualization for quantum walk experiments.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def plot_walk_distribution(positions, probabilities, title='Quantum Walk Distribution',
                            save_dir='results'):
    """Plot position probability distribution of a quantum walk."""
    save_path = Path(save_dir)
    save_path.mkdir(exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(positions, probabilities, color='#4ECDC4', alpha=0.8, edgecolor='#2C3E50')
    ax.set_xlabel('Position', fontsize=12)
    ax.set_ylabel('Probability', fontsize=12)
    ax.set_title(title, fontsize=13)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(save_path / 'walk_distribution.png', dpi=150)
    plt.close()


def plot_search_probability(times, success_probs, optimal_time=None,
                             save_dir='results'):
    """Plot success probability over time for quantum walk search."""
    save_path = Path(save_dir)
    save_path.mkdir(exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(times, success_probs, '-', color='#FF6B6B', linewidth=2)

    if optimal_time is not None:
        idx = np.argmin(np.abs(times - optimal_time))
        ax.axvline(x=optimal_time, color='#2C3E50', linestyle='--', alpha=0.5)
        ax.plot(optimal_time, success_probs[idx], 'o', color='#2C3E50',
                markersize=10, label=f'Optimal t={optimal_time:.2f}')
        ax.legend(fontsize=11)

    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Success Probability', fontsize=12)
    ax.set_title('Quantum Walk Search: Success Probability vs Time')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path / 'search_probability.png', dpi=150)
    plt.close()


def plot_continuous_walk_evolution(times, prob_matrix, node_labels=None,
                                    save_dir='results'):
    """Plot probability evolution across nodes over time."""
    save_path = Path(save_dir)
    save_path.mkdir(exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    n_nodes = prob_matrix.shape[1]
    colors = plt.cm.viridis(np.linspace(0, 1, min(n_nodes, 8)))

    for i in range(min(n_nodes, 8)):
        label = node_labels[i] if node_labels else f'Node {i}'
        ax.plot(times, prob_matrix[:, i], '-', color=colors[i],
                linewidth=1.5, alpha=0.8, label=label)

    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Probability', fontsize=12)
    ax.set_title('Continuous-Time Quantum Walk Evolution')
    ax.legend(fontsize=9, ncol=2)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path / 'walk_evolution.png', dpi=150)
    plt.close()


def plot_scaling_comparison(n_nodes, quantum_times, classical_times,
                             save_dir='results'):
    """Compare quantum vs classical search scaling."""
    save_path = Path(save_dir)
    save_path.mkdir(exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(n_nodes, classical_times, 's-', color='#FF6B6B', linewidth=2,
            markersize=8, label='Classical Random Walk')
    ax.plot(n_nodes, quantum_times, 'o-', color='#4ECDC4', linewidth=2,
            markersize=8, label='Quantum Walk')

    ax.set_xlabel('Number of Nodes', fontsize=12)
    ax.set_ylabel('Steps / Time to Find Target', fontsize=12)
    ax.set_title('Search Scaling: Quantum vs Classical')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path / 'scaling_comparison.png', dpi=150)
    plt.close()
