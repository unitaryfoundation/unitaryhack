---
title: "IonQ Core"
id: "ionq-core-python"
emoji: "⚛️🐍"
project_url: "https://github.com/ionq/ionq-core-python"
metaDescription: "The fully-typed, sync + async Python REST client for the IonQ Quantum Cloud — the wire-level building block the IonQ SDKs sit on."
date: 2026-06-04
summary: "The fully-typed, sync + async Python REST client for the IonQ Quantum Cloud — the wire-level building block the IonQ SDKs sit on."
tags:
  - "Python"
  - "quantum-computing"
  - "trapped-ion"
  - "REST API"
  - "API client"
  - "SDK"
  - "httpx"
  - "async/await"
  - "OpenAPI"
bounties:
  - issue_num: 56
    value: 125
  - issue_num: 57
    value: 150
  - issue_num: 58
    value: 150
---

**`ionq-core`** is a typed, sync **and** async Python client for the [IonQ Quantum Cloud Platform](https://cloud.ionq.com/dashboard) REST API. The HTTP layer is generated from [IonQ's OpenAPI spec](https://api.ionq.co/v0.4/api-docs), then wrapped in a small hand-written layer that adds retries, polling, cursor pagination, sessions, structured exceptions, and native-gate unitaries (GPi, GPi2, MS, ZZ).

It's the same wire-level client the higher-level IonQ integrations will build on, so it's a great place to hack if you want to work close to the API or extend the ecosystem.

**Why contribute?**

\- **Modern Python** \- `httpx`, `attrs`, full type hints, `ty`\-checked, 100% branch coverage on hand-written code.

\- **Real quantum hardware** \- submit circuits to IonQ's trapped-ion QPUs (Aria, Forte) and the cloud simulator.

\- **Foundational** \- will power Qiskit, Cirq, PennyLane, CUDA-Q, and more IonQ integrations.

\- **Approachable** \- Apache-2.0, on PyPI (`pip install ionq-core`), with a clear generated-vs-hand-written boundary and good first issues.

Docs: [https://ionq.github.io/ionq-core-python/](https://ionq.github.io/ionq-core-python/)
