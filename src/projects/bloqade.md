---
title: "bloqade"
id: "bloqade"
emoji: "⚛️"
project_url: "https://github.com/QuEraComputing/bloqade"
metaDescription: "a neutral atom software development kit"
date: 2026-03-19
summary: "a neutral atom software development kit"
tags:
  - "coding langauge"
  - "neutral atom"
  - "programming language"
  - "compiler"
  - "emulator"
  - "SDK"
bounties: []
---

Bloqade is a Python SDK for neutral atom quantum computing. It provides a set of embedded domain-specific languages (eDSLs) for programming neutral atom quantum computers. Bloqade is designed to be a high-level, user-friendly SDK that abstracts away the complexities of neutral atom quantum computing, allowing users to focus on developing quantum algorithms and compilation strategies for neutral atom quantum computers.

The bloqade repository is a namespace package for several components of bloqade, the actual implementation belongs to the following packages:

- bloqade-circuit Bloqade-circuit provides the core components of representing quantum circuits for bloqade.
- bloqade-decoders The QEC user interface providing integration with popular open-source decoders for the Bloqade SDK.
- bloqade-lanes Bloqade-lanes provides the core components for compiling neutral atom quantum circuit programs down to moves. It focuses on the physical layout and movement of atoms along fixed lanes in a neutral atom quantum processor.
- tsim A GPU-accelerated circuit sampler via ZX-calculus stabilizer rank decomposition. Tsim feels just like Stim, but supports non-Clifford gates.
