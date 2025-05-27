---
title: LDPC
emoji:
project_url: https://github.com/quantumgizmos/ldpc
metaDescription: Software for Decoding Quantum LDPC Codes
date: 2025-04-28
summary: Software for Decoding Quantum LDPC Codes
tags:
  - C++
  - python
  - error correction
bounties:
  - issue_num: 70
    value: 40
  - issue_num: 71
    value: 60
  - issue_num: 72
    value: 180
  - issue_num: 73
    value: 220
---

Any quantum error correction code is only ever as effective as its decoder, the classical co-processor responsible for interpreting syndrome information in real-time. This package implements a variety of decoding algorithms, with a particular focus on general methods based on belief propagation, a technique widely used in classical communication technologies such as WiFi and 5G. Belief propagation-based decoders are especially well-suited for decoding quantum low-density parity-check (LDPC) codes, which offer the potential to significantly reduce qubit overheads compared to surface codes.
