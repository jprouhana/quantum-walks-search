"""
Discrete-time coined quantum walk on graphs.
"""

import numpy as np
from qiskit.circuit import QuantumCircuit
from qiskit_aer import AerSimulator


def grover_coin(n_coin_qubits):
    """
    Grover diffusion operator as a coin for the quantum walk.
    Acts on the coin register.
    """
    dim = 2 ** n_coin_qubits
    coin = (2.0 / dim) * np.ones((dim, dim)) - np.eye(dim)
    return coin


def hadamard_coin():
    """Standard Hadamard coin for a 1D walk."""
    return np.array([[1, 1], [1, -1]]) / np.sqrt(2)


def build_coined_walk_circuit(n_position_qubits, n_steps, coin_type='grover'):
    """
    Build a discrete-time coined quantum walk circuit.

    The walk uses a coin register to determine direction and
    a position register to track the walker's location.

    Args:
        n_position_qubits: number of qubits for position register
        n_steps: number of walk steps
        coin_type: 'grover' or 'hadamard'

    Returns:
        QuantumCircuit for the walk
    """
    n_coin = 1 if coin_type == 'hadamard' else n_position_qubits
    n_total = n_position_qubits + n_coin
    qc = QuantumCircuit(n_total, n_position_qubits)

    coin_qubits = list(range(n_coin))
    pos_qubits = list(range(n_coin, n_total))

    # initial superposition on coin
    for q in coin_qubits:
        qc.h(q)

    for step in range(n_steps):
        # coin operator
        if coin_type == 'hadamard' and n_coin == 1:
            qc.h(coin_qubits[0])
        else:
            coin_matrix = grover_coin(n_coin)
            qc.unitary(coin_matrix, coin_qubits, label=f'C{step}')

        # conditional shift: increment position if coin=|1>
        # simplified shift using controlled increment
        qc.cx(coin_qubits[0], pos_qubits[0])
        for i in range(1, len(pos_qubits)):
            qc.mcx(coin_qubits[:1] + pos_qubits[:i], pos_qubits[i])

    # measure position register
    for i, q in enumerate(pos_qubits):
        qc.measure(q, i)

    return qc


def run_coined_walk(n_position_qubits, n_steps, coin_type='grover',
                     shots=8192, seed=42):
    """
    Execute a coined quantum walk and return position distribution.

    Returns:
        dict with 'positions' (array) and 'probabilities' (array)
    """
    qc = build_coined_walk_circuit(n_position_qubits, n_steps, coin_type)

    backend = AerSimulator(seed_simulator=seed)
    job = backend.run(qc, shots=shots)
    counts = job.result().get_counts()

    n_positions = 2 ** n_position_qubits
    probabilities = np.zeros(n_positions)
    for bitstring, count in counts.items():
        idx = int(bitstring, 2)
        probabilities[idx] = count / shots

    return {
        'positions': np.arange(n_positions),
        'probabilities': probabilities,
        'circuit': qc,
    }
