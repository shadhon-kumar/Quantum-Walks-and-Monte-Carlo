# src/postproc.py
import numpy as np
from collections import Counter
from scipy.stats import ks_2samp
from scipy.spatial.distance import jensenshannon
from scipy.special import rel_entr

def map_counts_to_probs_by_weight(counts, n_layers):
    """
    counts: dict from qiskit get_counts() where keys are bitstrings (MSB left).
    Interpret each bitstring as n_layers bits; count number of '1's in the string -> bin k.
    Returns prob_vector (length n_layers+1) and total shots.
    """
    total = sum(counts.values())
    hist = np.zeros(n_layers + 1, dtype=float)
    for bitstr, freq in counts.items():
        ones = bitstr.count('1')
        hist[ones] += freq
    if hist.sum() == 0:
        return hist, total
    return hist / hist.sum(), total

def block_rescale(probs, block_size=1):
    """
    For binomial distribution we typically map bins directly; block_size can aggregate contiguous counts.
    Returns xs (0..m-1) and normalized grouped probs.
    """
    if block_size <= 1:
        return np.arange(len(probs)), probs
    groups = []
    for start in range(0, len(probs), block_size):
        groups.append(probs[start:start+block_size].sum())
    arr = np.array(groups, dtype=float)
    s = arr.sum()
    if s == 0:
        return np.arange(len(arr)), arr
    return np.arange(len(arr)), arr / s

# Distances
def total_variation(p, q):
    p = np.asarray(p, dtype=float); q = np.asarray(q, dtype=float)
    if p.sum() == 0 or q.sum() == 0:
        return float('nan')
    p = p / p.sum(); q = q / q.sum()
    return 0.5 * np.sum(np.abs(p - q))

def js_divergence(p, q):
    p = np.asarray(p, dtype=float); q = np.asarray(q, dtype=float)
    if p.sum() == 0 or q.sum() == 0:
        return float('nan')
    return jensenshannon(p / p.sum(), q / q.sum(), base=2.0)

def kl_divergence(p, q):
    p = np.asarray(p, dtype=float) + 1e-12
    q = np.asarray(q, dtype=float) + 1e-12
    return float(np.sum(rel_entr(p, q)))
