---
title: "Piccolo"
id: "piccolo.jl"
emoji: "🎯🤖"
project_url: "https://github.com/harmoniqs/Piccolo.jl"
metaDescription: "A Julia package for solving quantum optimal control problems using direct trajectory optimization."
date: 2026-04-01
summary: "A Julia package for solving quantum optimal control problems using direct trajectory optimization."
tags:
  - "optimal-control"
  - "julia"
  - "optimization"
  - "pulse-design"
bounties: []
---

# Piccolo.jl

Piccolo.jl is a Julia package for quantum optimal control. It finds control pulses that implement quantum operations — gates, state transfers, and open-system dynamics — by solving a trajectory optimization problem over the joint space of quantum states and drive amplitudes.

## What you can do

- **Synthesize gates or state transfers** on qubits, qudits, cavities, and composite systems
- **Model common hardware** out of the box: transmons, transmon–cavity systems, trapped-ion chains, Rydberg arrays, and cat qubits
- **Choose a pulse parameterization**: piecewise constant, linear or cubic spline, Gaussian/erf envelopes, or custom functions
- **Optimize gate duration** (free-time), **global phases** (free-phase), and **system parameters** jointly with the pulse
- **Suppress leakage** via explicit costs and constraints on population outside the computational subspace
- **Design robust pulses** by optimizing fidelity over an ensemble of parameter variations
- **Handle open systems** with Lindbladian dynamics and density matrix objectives

Piccolo uses unitarity-preserving integrators and IPOPT as its NLP solver, and is part of the [Harmoniqs](https://github.com/harmoniqs) ecosystem.
