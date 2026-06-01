---
title: "clifft"
id: "clifft"
emoji: "⛰"
project_url: "https://github.com/unitaryfoundation/clifft"
metaDescription: "Clifft is a fast, exact Simulator for near-Clifford quantum circuits."
date: 2026-03-23
summary: "Clifft is a fast, exact Simulator for near-Clifford quantum circuits."
tags:
  - "simulation"
  - "error correction"
  - "fault tolerance"
  - "C++"
  - "python"
bounties: []
---

Clifft is a python package with C++ core that leverages a factored quantum state representation to quickly simulate quantum circuits. Rather than scaling exponentially with the number of qubits N, Clifft's runtime scales exponentially based on the size of the non-magic subspace of the quantum state -- growing with non-Clifford operations and shrinking with Clifford ones. Clifft's efficiency comes from a compiler-like architecture that optimizes the workload once per circuit and generates a custom bytecode for fast per-shot sampling via an efficient virtual machine. Clifft has a stim-like API and has been used to explore fault-tolerant protocols like magic state distillation and cultivation.
