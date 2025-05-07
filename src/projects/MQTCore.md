---
title: MQT Core
emoji: ⚛️
project_url: https://github.com/munich-quantum-toolkit/core
metaDescription: The Backbone of the Munich Quantum Toolkit (MQT) -- A collection of design automation tools and software for quantum computing
date: 2025-04-10
summary: The Backbone of the Munich Quantum Toolkit (MQT) -- A collection of design automation tools and software for quantum computing
tags:
  - C++
  - python
  - simulation
  - compilation
  - MLIR
  - decision diagrams
  - ZX-calculus
  - neutral atoms
  - quantum software stack
---

Quantum computers are becoming a reality and numerous quantum computing applications with a near-term perspective (e.g., for finance, chemistry, machine learning, and optimization) and with a long-term perspective (e.g., for cryptography or unstructured search) are currently being investigated. However, designing and realizing potential applications for these devices in a scalable fashion requires automated, efficient, and user-friendly software tools that cater to the needs of end users, engineers, and physicists at every level of the entire quantum software stack. Many of the problems to be tackled in that regard are similar to design problems from the classical realm for which sophisticated design automation tools have been developed in the previous decades. The Munich Quantum Toolkit (MQT) is a collection of software tools for quantum computing that explicitly utilizes this design automation expertise. It is developed by the Chair for Design Automation at the Technical University of Munich as well as the Munich Quantum Software Company (MQSC). Among others, it is part of the Munich Quantum Software Stack (MQSS) ecosystem, which is being developed as part of the Munich Quantum Valley (MQV) initiative. Our overarching objective is to provide solutions for design tasks across the entire quantum software stack. This entails high-level support for end users in realizing their applications, efficient methods for the classical simulation, compilation, and verification of quantum circuits, tools for quantum error correction, support for physical design, and more. These methods are supported by corresponding data structures (such as decision diagrams or the ZX-calculus) and core methods (such as SAT encodings/solvers). All of the developed tools are available as open-source implementations and are hosted on github.com/munich-quantum-toolkit. MQT Core is an open-source C++17 and Python library for quantum computing that forms the backbone of the quantum software tools developed as part of the MQT. To this end, it consists of multiple components that are used throughout the MQT, including a fully fledged intermediate representation (IR) for quantum computations (including support for neutral atom quantum computing), a state-of-the-art decision diagram (DD) package for quantum computing, and a dedicated ZX-diagram package for working with the ZX-calculus. Additionally, it features a full OpenQASM 3 parser and exporter as well as direct translation to/from Qiskit.  
