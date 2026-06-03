---
title: "Dynamiqs"
id: "dynamiqs"
emoji: "🔥"
project_url: "https://github.com/dynamiqs/dynamiqs"
metaDescription: "High-performance, GPU-accelerated and differentiable quantum systems simulation with JAX."
date: 2026-03-19
summary: "High-performance, GPU-accelerated and differentiable quantum systems simulation with JAX."
tags:
  - "scientific-computing"
  - "quantum-simulation"
  - "differentiable-programming"
  - "gpu-acceleration"
  - "python"
  - "jax"
bounties:
  - issue_num: 1079
    value: 140
  - issue_num: 1080
    value: 50
  - issue_num: 1081
    value: 75
  - issue_num: 1082
    value: 100
  - issue_num: 1083
    value: 135
office_hours:
  - date: "Monday, June 15, 2026"
    time: "11:00am ET"
    maintainer: "Nicolas Lepage"
---

**Dynamiqs** is a Python library for **GPU-accelerated** and **differentiable** quantum simulations. Solvers are available for the Schrödinger equation, the Lindblad master equation, the stochastic master equation, and others. The library is built with [JAX](https://jax.readthedocs.io/en/latest/index.html) and the main solvers are based on [Diffrax](https://github.com/patrick-kidger/diffrax).

The main features of **Dynamiqs** are:

* Running simulations on **CPUs** and **GPUs** with high-performance.  
* Executing many simulations **concurrently** by batching over Hamiltonians, initial states or jump operators.  
* Computing **gradients** of arbitrary functions with respect to arbitrary parameters of the system.  
* Full **compatibility** with the [JAX](https://jax.readthedocs.io/en/latest/index.html) ecosystem with a [QuTiP](https://qutip.org/)\-like API.
