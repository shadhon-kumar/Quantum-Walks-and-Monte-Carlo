# src/experiments.py
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

from src.compat import run_on_local
from src.qgb import build_qgb_circuit
from src.postproc import map_counts_to_probs_by_weight, block_rescale, total_variation, js_divergence, kl_divergence

RESULTS = Path("results")
(RESULTS / "figures").mkdir(parents=True, exist_ok=True)

def analyze_and_save(counts, shots, n_layers, name_tag, block_size=1):
    probs, total = map_counts_to_probs_by_weight(counts, n_layers)
    xs, grouped = block_rescale(probs, block_size=block_size)

    # compute mean/std from the full bin distribution
    k_vals = np.arange(len(xs))
    centers = (xs * block_size + (block_size-1)/2.0)
    mu = float((centers * grouped).sum()) if grouped.sum() > 0 else 0.0
    sigma = float(np.sqrt(((centers - mu)**2 * grouped).sum())) if grouped.sum() > 0 else 0.0

    # theoretical normal
    if sigma > 0:
        norm_pdf = norm.pdf(centers, loc=mu, scale=sigma)
        norm_p = norm_pdf / norm_pdf.sum()
    else:
        norm_p = np.zeros_like(grouped)

    tv = total_variation(grouped, norm_p) if norm_p.sum() > 0 else float('nan')
    js = js_divergence(grouped, norm_p) if norm_p.sum() > 0 else float('nan')
    kl = kl_divergence(grouped, norm_p) if norm_p.sum() > 0 else float('nan')

    # plot
    plt.figure(figsize=(6,4))
    plt.bar(centers, grouped, width=0.8, label="QGB (rescaled)")
    if norm_p.sum() > 0:
        plt.plot(centers, norm_p, label=f"Normal approx (mu={mu:.2f}, sd={sigma:.2f})", linewidth=2)
    plt.legend(loc='upper left')
    plt.xlabel("Bin (k successes / block)")
    plt.ylabel("Probability")
    plt.tight_layout()
    figpath = RESULTS / "figures" / f"{name_tag}.png"
    plt.savefig(figpath, dpi=150)
    plt.close()

    meta = {
        "name": name_tag,
        "shots": shots,
        "n_layers": n_layers,
        "block_size": block_size,
        "TV": None if np.isnan(tv) else float(tv) if not np.isnan(tv) else None,
        "JS": None if np.isnan(js) else float(js) if not np.isnan(js) else None,
        "KL": None if np.isnan(kl) else float(kl) if not np.isnan(kl) else None,
        "mu": mu,
        "sigma": sigma
    }
    with open(RESULTS / f"{name_tag}_metadata.json", "w") as f:
        json.dump(meta, f, indent=2)
    print(f"Saved {figpath} and metadata.")
    return meta

def task2_verify_gaussian(n_layers=20, shots=20000, block_size=1):
    qc, _ = build_qgb_circuit(n_layers=n_layers, bias_thetas=None, mode='standard')
    counts = run_on_local(qc, shots=shots)
    return analyze_and_save(counts, shots, n_layers, "task2_unbiased", block_size=block_size)

def task3_targets(n_layers=20, shots=20000, block_size=1):
    qc_exp, _ = build_qgb_circuit(n_layers=n_layers, bias_thetas=2.0, mode='standard')
    counts_exp = run_on_local(qc_exp, shots=shots)
    meta_exp = analyze_and_save(counts_exp, shots, n_layers, "task3_exponential", block_size=block_size)


    qc_h, _ = build_qgb_circuit(n_layers=n_layers, bias_thetas=None, mode='hadamard_walk')
    counts_h = run_on_local(qc_h, shots=shots)
    meta_h = analyze_and_save(counts_h, shots, n_layers, "task3_hadamard", block_size=block_size)

    return meta_exp, meta_h

if __name__ == "__main__":
    print("Running Task 2 (Gaussian verification)...")
    m2 = task2_verify_gaussian()
    print("Task2 metadata:", m2)
    print("Running Task 3 (two targets)...")
    m3 = task3_targets()
    print("Task3 metadata:", m3)
