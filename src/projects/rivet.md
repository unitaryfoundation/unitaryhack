---
title: rivet
emoji:
project_url: https://github.com/haiqu-ai/rivet
metaDescription: Rivet is a fast, flexible transpiler for quantum circuits, built for modularity and performance.
summary: Rivet is a fast, flexible transpiler for quantum circuits, built for modularity and performance.
tags:
  - python
  - transpiler
bounties:
  - issue_num: 4
    value: 250
  - issue_num: 5
    value: 250
---

Even at small scales, transpilation can become a key bottleneck in many complex quantum computing workflows, such as those in Error Mitigation or Quantum Machine Learning, where modular circuits are iteratively updated and transpiled or many instances of largely similar circuits are run.

[Rivet](https://github.com/haiqu-ai/rivet) is a modular, high-performance transpilation toolkit for quantum circuits, enabling flexible control over transpilation stacks (Qiskit, Pytket, BQSKit), subcircuit stitching, qubit constraint handling, and caching—dramatically reducing transpilation time. Built by [**Haiqu**](https://haiqu.ai/), a quantum software company focused on pushing the limits of today’s noisy quantum hardware, Rivet helps users get the best performance out of their applications.
