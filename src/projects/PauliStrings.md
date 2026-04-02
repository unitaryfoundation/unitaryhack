---
title: "PauliStrings.jl"
id: "paulistrings.jl"
emoji: "🧶"
project_url: "https://github.com/nicolasloizeau/PauliStrings.jl"
metaDescription: "Quantum many body simulations in the Pauli strings basis"
date: 2026-03-20
summary: "Quantum many body simulations in the Pauli strings basis"
tags:
  - "julia"
  - "pauli propagation"
  - "circuits"
  - "simulation"
bounties: []
---

[PauliStrings.jl ](https://paulistrings.org/) is a Julia package for high performance simulation of quantum many-body systems in the Pauli string basis. It is particularly adapted for simulating systems with low-magic and non-trivial geometry.
The performance arises from two key features:
- a binary encoding of the Pauli algebra
- systematic truncation methods that discard low importance Pauli strings
