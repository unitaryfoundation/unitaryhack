---
title: The "Slop-Detection" Checklist for Maintainers
date: 2026-04-01
metaDescription: Maintainer's guide to reviewing AI-based submissions
permalink: /ai-checklist/index.html
---

If a PR hits **two or more** of these flags, it is likely "AI Slop." You have full permission to close it without further review.

## 1. The "Polite Robot" PR Description
- **The "Summarizer" Tone:** Does the description simply restate the issue in perfectly grammatical, slightly repetitive prose? (e.g., _"This Pull Request aims to resolve the reported issue by implementing the requested functionality in the designated module..."_)
- **Generic Bullet Points:** Are there bullet points that describe _what_ the code does but not _why_ the specific technical choices were made?
- **Missing Context:** No mention of local testing results, specific edge cases encountered, or "I tried X but Y happened."

## 2. Code Smells (The "Hallucination" Test)
- **Non-Existent APIs:** Does the code call functions or methods that don't exist in the library (e.g., calling `circuit.apply_quantum_magic()` in a Mitiq PR)?
- **The "Stub" Fix:** Does the PR "fix" the issue by adding a `TODO`, an empty `try/except` block, or by simply deleting the failing test case?
- **Redundant Comments:** Does the code have "Captain Obvious" comments?
   - _Example:_ `x = x + 1 # Increment x by one`
- **Inconsistent Logic:** Does the code define a variable and then never use it, or import a massive library for a one-line change?

## 3. The "Quantum Reality Check"
- **Physical Impossibility:** Does the code attempt to perform operations that violate quantum mechanics or the specific constraints of the backend (e.g., mid-circuit measurement on a device that doesn't support it without checking)?
- **Mathematical Nonsense:** AI often struggles with complex indexing in tensors or state vectors. Check for `shape` mismatches that a human would have caught by running the code once.

## 4. Behavioral Red Flags
- **The "Fastest Gun in the West":** Was the PR submitted within minutes of the bounty being posted? (Unless it's a typo fix, it’s likely automated).
- **Ghosting:** If you ask a clarifying technical question (_"Why did you choose this specific error mitigation technique over the default?"_) and they can't answer or provide another AI-generated paragraph, it's slop.

## 🛠 The "Fast-Close" Templates
_Copy and paste these to save your team from "rejection guilt."_

### Template A: The "Likely AI" Rejection
"Hi @[Username], thank you for your interest in unitaryHACK. This PR appears to be a low-effort, AI-generated submission that hasn't been properly verified or tested against our codebase. Per our Human-in-the-Loop AI Policy, we are closing this to prioritize maintainer time for substantive, human-led contributions. Please review the unitaryHACK Hacker Guide before submitting further PRs."

### Template B: The "Explain Your Work" Challenge
_(Use this if you aren't 100% sure but are suspicious)_
"Hi @[Username], thanks for the PR. To ensure this meets our quality standards, could you please explain the logic behind [Specific Line/Function] and confirm that you've run the test suite locally? We require all hackers to be able to defend their technical choices to be eligible for bounties."


## Pro-Tip for Maintainers:
If you see a user submitting "slop" across multiple projects in the Unitary Foundation ecosystem, **flag them in the #maintainers Discord channel.** We can then issue a global ban for the duration of unitaryHACK to stop the noise.
