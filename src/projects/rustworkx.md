---
title: rustworkx
emoji: 🦀🏋️
project_url: https://github.com/Qiskit/rustworkx
metaDescription: A high performance Python graph library implemented in Rust.
date: 2025-05-27
summary: A high performance Python graph library implemented in Rust.
tags:
  - python
  - rust
bounties:
  - issue_num: 840
    value: 200
  - issue_num: 1009
    value: 100
  - issue_num: 1184
    value: 125
  - issue_num: 1437
    value: 100
  - issue_num: 1438
    value: 125
---

**rustworkx** is a Python package for working with graphs and complex networks. It enables the creation, interaction with, and study of graphs and networks.

It provides:

- Data structures for creating graphs including directed graphs and multigraphs
- A library of standard graph algorithms
- Generators for various types of graphs including random graphs
- Visualization functions for graphs

rustworkx is written in the Rust programming language to leverage Rust’s inherent performance and safety. While this provides numerous advantages including significantly improved performance it does mean that the library needs to be compiled when being installed from source (as opposed to a pure Python library which can just be installed). rustworkx supports and publishes pre-compiled binaries for Linux on x86, x86_64, aarch64, s390x, and ppc64le, MacOS on x86_64, and arm64, and Windows 32bit and 64bit systems. However, if you are not running on one of these platforms, you will need a rust compiler to install rustworkx.
