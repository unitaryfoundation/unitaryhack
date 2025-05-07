---
title: PyZX
emoji: 🕷️
project_url: https://github.com/zxcalc/pyzx
metaDescription: Python library for quantum circuit rewriting and optimisation using the ZX-calculus
date: 2025-04-02
summary: Python library for quantum circuit rewriting and optimisation using the ZX-calculus
tags:
  - compiler
  - classical simulation
  - tensor networks
  - ZX-calculus
  - python
---

PyZX (pronounce as Pisics) is a Python tool implementing the theory of ZX-calculus for the creation, visualisation, and automated rewriting of large-scale quantum circuits.
ZX-diagrams are a type of tensor network built out of combinations of linear maps known as spiders. There are 2 types of spiders: the Z-spiders (represented as green dots in PyZX) and the X-spiders (represented as red dots). Every linear map between some set of qubits can be represented by a ZX-diagram. The ZX-calculus is a set of rewrite rules for ZX-diagrams. There are various extensive set of rewrite rules. PyZX however, uses only rewrite rules concerning the Clifford fragment of the ZX-calculus. Importantly, this set of rewrite rules is complete for Clifford diagrams, meaning that two representations of a Clifford map can be rewritten into one another if and only if the two linear maps they represent are equal.
