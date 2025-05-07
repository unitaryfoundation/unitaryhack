---
title: Pauli Propagation
emoji: 🇵 🇵
project_url: https://github.com/MSRudolph/PauliPropagation.jl
metaDescription: A framework for simulating quantum circuits and quantum systems in the Pauli basis
date: 2025-04-02
summary: A framework for simulating quantum circuits and quantum systems in the Pauli basis
tags:
  - julia
  - circuits
  - simulation
  - pauli strings
---

`PauliPropagation.jl` is a Julia package for Pauli propagation simulation of quantum circuits.

Pauli propagation methods are a new kid on the block of classical simulation algorithms, and can in some cases already outperform state-of-the-art tensor networks. Our mission is to develop this flexible and high-performance code base for everyone to use in their research.

The package simulates the evolution of objects expressed in the Pauli basis under noiseless and noisy quantum circuits. Commonly, this is used for the Heisenberg picture evolution of an observable. Some opt-in truncations or approximations are particularly suited for estimating expectation values of evolved observables with quantum states.
