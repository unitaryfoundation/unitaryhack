---
title: "Dynamiqs"
id: "dynamiqs"
emoji: 🔥
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
bounties: []
---

Dynamiqs is a Python library for GPU-accelerated and differentiable quantum simulations. Solvers are available for the Schrödinger equation, the Lindblad master equation, the stochastic master equation, and others. The library is built with JAX and the main solvers are based on Diffrax.

The main features of Dynamiqs are:
- Running simulations on CPUs and GPUs with high-performance.
- Executing many simulations concurrently by batching over Hamiltonians, initial states or jump operators.
- Computing gradients of arbitrary functions with respect to arbitrary parameters of the system.
- Full compatibility with the JAX ecosystem with a QuTiP-like API.
