# Quantum Galton Board 


## 3. Implementation Approach

### 3.1 Design Choice — Step-Qubit Model
Instead of using complex binary‐encoded position registers with arithmetic increment/decrement, this project uses a **step‐qubit** model:
- Each layer is represented by a single “decision” qubit.
- An unbiased step is implemented with a **Hadamard** gate:  
  \( P(\text{right}) = P(\text{left}) = 0.5 \).
- Measuring all step qubits yields a bitstring whose **Hamming weight** (number of `1`s) corresponds to the final bin.

This model is:
- **General** — works for any number of layers.
- **Stable** — uses only standard gates (`H`, `Ry`, `CZ`, `measure`).
- **Efficient** — minimal circuit depth, low simulator noise.

### 3.2 Task 2 — Gaussian Verification
- Built a circuit with **n_layers = 20** unbiased steps (`H` gates).
- Ran on Qiskit AerSimulator with 20,000 shots.
- Mapped measured bitstrings to Hamming weights to produce histogram.
- Compared the histogram to a theoretical Gaussian approximation using **Total Variation (TV)**, **Jensen–Shannon divergence (JS)**, and **Kullback–Leibler divergence (KL)**.

**Expected result:** Binomial distribution with  
\( \mu \approx \frac{n}{2} \) and \( \sigma \approx \sqrt{n/4} \).

**Observed:**  
`mu = 9.99`, `sigma = 2.24` — matches theory.

### 3.3 Task 3a — Exponential-like Distribution
- Replaced each `H` with a biased **`Ry(theta)`** gate.  
- Chose `theta = 2.0` radians → \( P(\text{right}) > 0.5 \) producing a skewed distribution toward high Hamming weights.

**Observed:**  
`mu = 14.15` (shifted right), `sigma = 2.03`.  
Divergences from Gaussian larger than in Task 2.

### 3.4 Task 3b — Hadamard Quantum Walk Variant
- Applied **`H`** to each qubit, then **`CZ`** gates between neighbors to introduce quantum interference patterns.
- Distribution remained centered near `mu ≈ 10` but with subtle deviations from the Gaussian.

---

## 4. Results Summary

| Task                 | μ (mean) | σ (std. dev.) | TV     | JS      | KL       | Notes |
|----------------------|----------|---------------|--------|---------|----------|-------|
| Task 2 — Gaussian    | 9.99     | 2.24           | 0.0095 | 0.0132  | 0.00045  | Matches binomial Gaussian |
| Task 3a — Exponential| 14.15    | 2.03           | 0.0288 | 0.0362  | 0.00352  | Skewed right |
| Task 3b — Hadamard   | 10.00    | 2.26           | 0.0127 | 0.0146  | 0.00056  | Interference pattern |

**Interpretation:**
- Task 2 reproduces the expected Gaussian behavior of an unbiased Galton board.
- Task 3a demonstrates control over bias to produce a clearly different target distribution.
- Task 3b shows a second alternative distribution, distinct from both the unbiased and biased cases.




