---
title: "Stretto"
id: "stretto.jl"
emoji:
project_url: "https://github.com/harmoniqs/Stretto.jl"
metaDescription: "Stretto.jl is the circuit-to-pulse compilation layer of the Piccolo.jl ecosystem."
date: 2026-05-12
summary: "Stretto.jl is the circuit-to-pulse compilation layer of the Piccolo.jl ecosystem."
tags:
  - "Julia"
bounties: []
office_hours:
  - date: "Friday, June 12, 2026"
    time: "1:00pm ET"
    maintainer: "Jack Champagne"
---

**Stretto.jl** is the circuit-to-pulse compilation layer of the [Piccolo.jl](https://github.com/harmoniqs/Piccolo.jl) ecosystem. Given a gate-level circuit and a hardware device profile, Stretto synthesizes a single optimized control pulse that implements the whole circuit as one block unitary U — skipping gate decomposition, scheduling, and gate-boundary error accumulation.
