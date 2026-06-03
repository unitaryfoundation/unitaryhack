---
title: "CUDA-Q"
id: "cuda-quantum"
emoji: 💚
project_url: "https://github.com/NVIDIA/cuda-quantum"
metaDescription: "The open-source software platform for quantum computing and quantum-GPU supercomputing"
date: 2026-05-29
summary: "The open-source software platform for quantum computing and quantum-GPU supercomputing"
tags: []
bounties:
  - issue_num: 4289
    value: 100
  - issue_num: 3437
    value: 100
  - issue_num: 2982
    value: 100
  - issue_num: 2942
    value: 100
  - issue_num: 2242
    value: 100
---

CUDA-Q is NVIDIA's open-source platform for quantum-GPU computing. Write a quantum program once in Python or C++ using @cudaq.kernel, and run it across NVIDIA's GPU-accelerated simulators or real QPUs without rewriting your code.
What you get at a hackathon:
Single-source hybrid programming. Express quantum and classical logic together in one language you already know, with tight integration to classical compute.
GPU-accelerated simulation through cuQuantum. State vector, tensor network, density matrix, and more, scaled across multiple GPUs and nodes so you can simulate larger systems and run faster than CPU-only tools.
Hardware portability. The same kernel targets simulators or physical QPUs from multiple hardware partners. Prototype on a GPU, point at a real device when you're ready.
Accelerated libraries. cuQuantum for simulation, CUDA-Q QEC for quantum error correction research including the first GPU-accelerated decoders, and CUDA-Q Solvers for application building blocks.
An MLIR-based compiler that handles optimization and lowering, so you focus on the algorithm.
Pitch line: write it once, simulate it fast on GPUs, and run it on real quantum hardware, all from Python or C++.
