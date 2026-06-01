---
title: "QuEST"
id: "quest"
emoji: "🏆"
project_url: "https://github.com/QuEST-Kit/QuEST"
metaDescription: "A multithreaded, distributed, GPU-accelerated simulator of quantum statevectors and density matrices"
date: 2026-03-26
summary: "A multithreaded, distributed, GPU-accelerated simulator of quantum statevectors and density matrices"
tags:
  - "simulation"
  - "C"
  - "C++"
  - "CUDA"
  - "MPI"
  - "OpenMP"
  - "cuQuantum"
  - "HIP"
bounties: []
---

The **Quantum Exact Simulation Toolkit** (QuEST) is a high-performance simulator of quantum statevectors and density matrices. It hybridises **multithreading**, **GPU acceleration** and **distribution** to run lightning fast on laptops, desktops and supercomputers, parallelising over multiple cores, CPUs and GPUs. Behind the scenes, QuEST leverages [OpenMP](https://www.openmp.org/), [MPI](https://www.mpi-forum.org/), [CUDA](https://developer.nvidia.com/cuda-zone), [HIP](https://rocm.docs.amd.com/projects/HIP/en/docs-develop/what_is_hip.html), [Thrust](https://developer.nvidia.com/thrust), [cuQuantum](https://developer.nvidia.com/cuquantum-sdk) and [GPUDirect](https://developer.nvidia.com/gpudirect) for cutting-edge performance on modern multi-GPU clusters, and compatibility with older NVIDIA and AMD GPUs. These deployments can be combined in any combination, or automatically decided at runtime, yet are abstracted behind a single, seamless interface, accessible by both C and C++ and all the major compilers
