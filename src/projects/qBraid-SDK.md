---
title: qBraid-SDK
id: qbraid
emoji: 🏃‍♂️⏱️
project_url: https://github.com/qBraid/qBraid
metaDescription: A platform-agnostic quantum runtime framework
date: 2025-04-17
summary: A platform-agnostic quantum runtime framework
tags:
  - python
  - runtime
  - transpiler
  - openqasm
  - qir
  - rustworkx
bounties:
  - issue_num: 953
    value: 50
  - issue_num: 851
    value: 50
  - issue_num: 789
    value: 100
  - issue_num: 785
    value: 100
  - issue_num: 981
    value: 200
---

The qBraid-SDK is a platform-agnostic quantum runtime framework designed for both quantum software and hardware providers. This Python-based tool streamlines the full lifecycle management of quantum jobs—from defining program specifications to job submission and through to the post-processing and visualization of results.

Unlike existing runtime frameworks that focus their automation and abstractions on quantum components, qBraid adds an extra layer of abstractions that considers the ultimate IR needed to encode the quantum program and securely submit it to a remote API. Notably, the qBraid-SDK _does not adhere to a fixed circuit-building library_, or quantum program representation. Instead, it empowers providers to dynamically [register](https://docs.qbraid.com/sdk/user-guide/programs#quantum-program-registry) any desired input program type as the target based on their specific needs. By doing so, the qBraid-SDK vastly reduces the overhead and redundancy typically associated with the development of [runtime pipelines](https://docs.qbraid.com/sdk/user-guide/runtime/components) and cross-platform integrations in quantum computing.

> Read more about our [graph-based transpiler](https://docs.qbraid.com/sdk/user-guide/transpiler)

_Resources_:

- [Documentation](https://docs.qbraid.com/sdk/user-guide/overview)
- [API Reference](https://sdk.qbraid.com/qBraid/index.html)
- [Example Notebooks](https://github.com/qBraid/qbraid-lab-demo/tree/main/qbraid_sdk)
