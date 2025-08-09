
This project implements a ** ## Project 1 Quantum Walks and Monte Carlo ** using Qiskit

A classical Galton board produces a binomial (Gaussian) distribution of balls across bins.  
In the **quantum** version, each “peg” is replaced by a quantum coin toss, allowing superposition and interference to produce different target distributions.

All results are saved as **plots** and **metadata JSON** for easy verification.

## Project Structure
.
├── src/ # Source code
│ ├── qgb.py                        # QGB circuit construction
│ ├── experiments.py                 # test 3 execution
│ ├── postproc.py                   # Histogram mapping & metrics
│ ├── compat.py                     # Qiskit Aer 
├── results/
│ ├── figures/                      # Output plots
│ ├── *_metadata.json               # Statistical metrics
├── requirements.txt                # Python dependencies
├── README.md
├── summary.pdf                     #two‐page summary


## Installation

### 1️⃣ Create and activate environment

conda create --name qiskit_env python==3.10
conda activate qiskit_env

## Install dependencies

pip install -r requirements.txt

## Running the Project 
## Run The (Gaussian verification) and (two target distributions)

python -m src.experiments







