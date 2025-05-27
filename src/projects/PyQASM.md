---
title: PyQASM
emoji: 🐣🧩
project_url: https://github.com/qBraid/pyqasm
metaDescription: Python toolkit for OpenQASM program analysis, validation and compilation
date: 2025-04-17
summary: Python toolkit for OpenQASM program analysis, validation and compilation
tags:
  - python
  - openqasm
  - compiler
  - semantic analysis
bounties:
  - issue_num: 53
    value: 150
  - issue_num: 7
    value: 100
  - issue_num: 77
    value: 150
  - issue_num: 10
    value: 100
---

PyQASM is a Python toolkit providing an OpenQASM 3 semantic analyzer and utilities for program analysis and compilation.

[OpenQASM](https://openqasm.com/) is a powerful language for expressing hybrid quantum-classical programs, but it lacks a comprehensive tool supporting the full capabilities of the language. PyQASM addresses this by using the official [ANTLR grammar](https://openqasm.com/grammar/index.html) as a reference for OpenQASM 3’s language structure and by leveraging the [`openqasm3.parser`](https://github.com/openqasm/openqasm/blob/ast-py/v1.0.1/source/openqasm/openqasm3/parser.py) to interact with the official AST. On top of this foundation, it adds high-level utilities such as program _validation_ and _unrolling_.

In PyQASM, “unrolling” (also known as program flattening or inlining) refers to the process of simplifying a quantum program by expanding custom gate definitions, and flattening complex language constructs such as subroutines, loops, and conditional statements into a linear sequence of basic operations. By converting the program into this simplified format, it becomes easier to perform subsequent transpilation or compilation steps before executing the program on a quantum device.

_Resources_:

- [Documentation](https://docs.qbraid.com/pyqasm/user-guide/overview)
- [API Reference](https://sdk.qbraid.com/pyqasm/api/pyqasm.html)
- [Example Notebooks](https://github.com/qBraid/qbraid-lab-demo/tree/main/pyqasm)
