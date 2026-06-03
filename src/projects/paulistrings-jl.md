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
bounties:
  - issue_num: 80
    value: 200
  - issue_num: 78
    value: 100
  - issue_num: 75
    value: 50
  - issue_num: 81
    value: 50
  - issue_num: 82
    value: 50
  - issue_num: 79
    value: 50
office_hours:
  - date: "Monday, June 8, 2026"
    time: "11:00am ET"
    maintainer: "Nicolas Loizeau"
---

[PauliStrings.jl](https://paulistrings.org/) is a Julia package for high performance simulation of quantum many-body systems in the Pauli string basis. It is particularly adapted for simulating systems with low-magic and non-trivial geometry.
The performance arises from two key features:
- a binary encoding of the Pauli algebra
- systematic truncation methods that discard low importance Pauli strings
