---
title: "Marqov SDK"
id: "marqov-sdk"
emoji: "⚛️🦘"
project_url: "https://github.com/marqov-dev/marqov-sdk"
metaDescription: "A Python SDK for orchestrating reproducible quantum-classical hybrid workflows across simulators and QPUs."
date: 2026-06-02
summary: "A Python SDK for orchestrating reproducible quantum-classical hybrid workflows across simulators and QPUs."
tags:
  - "python"
  - "quantum-computing"
  - "quantum-classical-hybrid"
  - "orchestration"
  - "workflow"
  - "reproducibility"
  - "braket"
  - "azure-quantum"
  - "qiskit"
  - "pyquil"
  - "temporal"
  - "sdk"
bounties:
  - issue_num: 1
    value: 150
  - issue_num: 2
    value: 125
  - issue_num: 3
    value: 65
  - issue_num: 4
    value: 75
  - issue_num: 5
    value: 50
  - issue_num: 6
    value: 35
---

**Marqov SDK** is the open-source Python interface to the Marqov platform, a quantum-classical hybrid orchestration layer for building, running, and reproducing hybrid workflows across multiple quantum backends.

Write your hybrid programs once using `@task` and `@workflow` decorators, then dispatch them to simulators or QPUs through a unified executor abstraction. The SDK speaks to the major hardware and simulation providers out of the box (Amazon Braket, Azure Quantum, etc) so you can swap backends without rewriting your circuit or orchestration logic.

A core design goal is **reproducibility**: workflows are structured so that an experiment can be re-run and verified rather than re-derived, addressing the reproducibility gap that affects much of today's quantum-classical research.

**What you'll find in the repo**
- A circuit abstraction layer that's vendor-agnostic across supported backends
- `@task` / `@workflow` decorators for composing hybrid pipelines
- Pluggable executors for simulators and QPUs
- A CLI for submitting and managing jobs
- Durable workflow orchestration built on Temporal (`temporalio`)

**Who should contribute**
Whether your background is in quantum algorithm and SDK development or in HPC, infrastructure, and orchestration engineering, there's surface area here for you. Algorithm-focused contributors can work on circuit abstractions, backend adapters, and provider integrations; infrastructure-focused contributors can work on executors, the CLI, job lifecycle management, and orchestration durability. The entire public SDK is Python, so no other language required to contribute.
