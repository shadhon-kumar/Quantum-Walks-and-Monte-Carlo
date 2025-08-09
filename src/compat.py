# src/compat.py
from qiskit import Aer, transpile
try:
    from qiskit.providers.aer import AerSimulator
    _HAS_AER_SIM = True
except Exception:
    AerSimulator = None
    _HAS_AER_SIM = False

def get_local_backend():
    if _HAS_AER_SIM:
        try:
            sim = AerSimulator()
            return sim, sim.name()
        except Exception:
            pass
    return Aer.get_backend('aer_simulator'), 'aer_simulator'

def run_on_local(qc, shots=2000, seed=42, optimization_level=1):
    backend, _ = get_local_backend()
    try:
        tqc = transpile(qc, backend=backend, optimization_level=optimization_level)
    except Exception:
        tqc = transpile(qc, optimization_level=optimization_level)
    job = backend.run(tqc, shots=shots)
    res = job.result()
    return res.get_counts()
