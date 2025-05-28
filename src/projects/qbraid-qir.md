---
title: qBraid-QIR
emoji: ⚙️🔌
project_url: https://github.com/qBraid/qbraid-qir
metaDescription: qBraid-SDK extension providing support for QIR conversions.
summary: qBraid-SDK extension providing support for QIR conversions.
date: 2025-05-08
tags:
  - python
  - qir
  - transpiler
  - openqasm
  - cirq
bounties:
  - issue_num: 196
    value: 75
  - issue_num: 93
    value: 125
  - issue_num: 199
    value: 150
  - issue_num: 224
    value: 150
---

qBraid-QIR is a Python package for generating [QIR](https://www.qir-alliance.org/) (Quantum Intermediate Representation) programs from high-level quantum programming languages. It currently supports conversions for [Cirq](https://quantumai.google/cirq) and [OpenQASM 3](https://openqasm.com/). This project aims to make QIR representations accessible via the [qBraid-SDK transpiler](https://docs.qbraid.com/sdk/user-guide/transpiler), and by doing so, open the door to language-specific conversions from any of the 10+ gate-based quantum program types [supported](https://github.com/qBraid/qBraid?tab=readme-ov-file#transpiler) by `qbraid`.

> “Interoperability opens doors to cross-fields problem-solving.” - QIR Alliance: [Why do we need it?](https://www.qir-alliance.org/qir-book/concepts/why-do-we-need.html)

This project was conceived in collaboration with the [Quantum Open Source Foundation](https://qosf.org/).

_Resources_:

- [Documentation](https://docs.qbraid.com/qir/user-guide/overview)
- [API Reference](https://sdk.qbraid.com/pyqasm/index.html)
- [Example Notebooks](https://github.com/qBraid/qbraid-lab-demo/tree/main/qbraid_qir)
