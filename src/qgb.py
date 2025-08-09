# src/qgb.py
"""
Quantum Galton Board — Step-qubit (Bernoulli-sum) implementation.

- n_layers qubits: each qubit represents one peg/decision.
- Unbiased: Hadamard on each decision qubit -> P(1)=0.5 -> binomial distribution.
- Biased (exponential-like): Ry(theta) on each decision qubit, P(1)=sin^2(theta/2).
- Hadamard-walk variant: different gate pattern to produce interference-like distribution.

build_qgb_circuit(n_layers, bias_thetas=None, mode='standard')
 returns (qc, measure_qubit_indices)
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import numpy as np

def build_qgb_circuit(n_layers: int, bias_thetas=None, mode='standard'):
    """
    n_layers: positive int — number of steps
    bias_thetas:
      - None => use H for unbiased
      - scalar => use Ry(theta) on every step qubit (bias)
      - list => per-step theta (len >= n_layers is ok)
    mode:
      - 'standard' -> unbiased or biased Bernoulli sum (Task 2 + exp)
      - 'hadamard_walk' -> variant: apply H then controlled-Z between neighbors to create interference
    Returns: (qc, measure_indices)
    """
    if n_layers < 1:
        raise ValueError("n_layers must be >= 1")

    q = QuantumRegister(n_layers, 'steps')
    c = ClassicalRegister(n_layers, 'csteps')
    qc = QuantumCircuit(q, c)

    # Prepare per-step angles
    if bias_thetas is None:
        thetas = [None] * n_layers
    elif np.isscalar(bias_thetas):
        thetas = [float(bias_thetas)] * n_layers
    else:
        thetas = list(bias_thetas)
        if len(thetas) < n_layers:
            thetas += [None] * (n_layers - len(thetas))

    # Apply coin/decision gates
    for i in range(n_layers):
        theta = thetas[i]
        if mode == 'hadamard_walk':
            qc.h(q[i])
        else:
            if theta is None:
                qc.h(q[i])
            else:
                qc.ry(theta, q[i])

    
    if mode == 'hadamard_walk':
        for i in range(n_layers - 1):
            qc.cz(q[i], q[i+1])

    qc.measure(q, c)
    measure_indices = list(range(n_layers))
    return qc, measure_indices
