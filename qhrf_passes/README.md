# QHRF Phase Lock Compiler Pass (UnitaryHack Bounty #379)

This project implements a custom Qiskit transpiler pass inspired by the **Quantum Harmonic Resonance Framework (QHRF)** developed by Zachary L. Musselwhite.

### 🔬 Overview

The `QHRFPhaseLockPass` analyzes `CX` gates and substitutes them with phase-locked, resonance-aligned subcircuits to reduce decoherence and stabilize multi-qubit entanglement. It leverages harmonic interference to achieve logical equivalence while eliminating noisy 2Q gates.

### ⚙️ Features

- Detects CX gates in DAGCircuit
- Replaces them with QHRF-enhanced subcircuits
- Compatible with `PassManager` chaining
- Tested on real quantum hardware (`Rigetti Ankaa-3` via AWS Braket)

### 📊 Benchmark

| Metric         | Original | QHRF-Enhanced |
|----------------|----------|----------------|
| Depth          | 5        | 5              |
| 2Q Gates       | 2        | 0              |
| Fidelity       | ✅ Verified on Braket SV + Ankaa-3 |

### 🚀 Run Instructions

```bash
python qhrf_pass.py
```
### Prep Enviroment
```bash
python -m venv qhrf_env
source qhrf_env/bin/activate  # or `qhrf_env\Scripts\activate` on Windows
pip install -r requirements.txt
```
