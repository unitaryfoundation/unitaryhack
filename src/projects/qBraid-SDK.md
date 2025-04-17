---
title: qBraid-SDK
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
---

The qBraid-SDK is a platform-agnostic quantum runtime framework designed for both quantum software and hardware providers.  This Python-based tool streamlines the full lifecycle management of quantum jobs—from defining program specifications to job submission and through to the post-processing and visualization of results. Unlike existing runtime frameworks that focus their automation and abstractions on quantum components, qBraid adds an extra layer of abstractions that considers the ultimate IR needed to encode the quantum program and securely submit it to a remote API. Notably, the qBraid-SDK does not adhere to a fixed circuit-building library, or quantum program representation. Instead, it empowers providers to dynamically register any desired input program type as the target based on their specific needs. This flexibility is extended by the framework’s modular pipeline, which facilitates any number of additional program validation, transpilation, and compilation steps.  By addressing the full scope of client-side software requirements necessary for secure submission and management of quantum jobs, the qBraid-SDK vastly reduces the overhead and redundancy typically associated with the development of internal pipelines and cross-platform integrations in quantum computing.
