---
title: unitaryHACK Hacker’s Guide to Ethical AI Contributions
metaDescription: unitaryHACK AI Policy
date: 2026-04-01
permalink: /ai-guide/index.html
eleventyNavigation:
  key: AI Guide
  order: 5
---

At unitaryHACK, we believe AI is a powerful co-pilot, not an autopilot. Quantum computing is hard, and while Large Language Models (LLMs) like ChatGPT, Claude, or Copilot can help you understand a new library, they can also confidently generate code that violates the laws of physics.

To keep the ecosystem healthy and respect our maintainers’ time, we follow a **Human-in-the-Loop** policy.

## 🟢 The Green Light: High-Value AI Collaboration
These are tasks where AI adds value without burdening maintainers. **Note: All AI-assisted work must still be disclosed and verified.**
- **Documenting the Complex:** Ask an LLM to help you draft a docstring for a complex function, then edit it to ensure the quantum terminology (e.g., "non-Clifford gate count" or "basis state") is precise.
- **Boilerplate Unit Tests:** Use AI to generate the structural code for a test suite. Crucial: You must then run those tests locally and verify they actually pass and cover the edge cases.
- **Explaining Errors:** Paste a cryptic stack trace into an LLM to help you brainstorm why a circuit might be failing. Use that insight to write your own fix.
- **Code Refactoring:** Use AI to suggest more "Pythonic" ways to write a loop or handle data, provided the underlying quantum logic remains untouched.

## 🔴 The Red Light: "AI Slop" & Cheating
Submitting these will likely result in an immediate rejection and potential disqualification.
- **The "Blind" PR:** Copy-pasting an issue description into an LLM and submitting the output without ever running the code or understanding how it works.
- **Mass-Submissions:** Using automation to "spray and pray" AI-generated fixes across dozens of repositories.
- **Hallucinated Logic:** Submitting PRs that use functions or libraries that don't exist, or that "fix" a bug by simply deleting the failing test.
- **Undisclosed AI Use:** Passing off AI-generated code or documentation as your own original work. **Honesty is a requirement for bounty eligibility.**

## 🛠 The Ethical Workflow: 4 Steps to a Winning PR
If you use AI to help with your contribution, follow this "Human-in-the-Loop" checklist before you hit _Submit_:
1. **Understand:** Could I explain this code to a maintainer in a live interview? If no, don't submit it.
2. **Verify:** Did I run `pytest` (or the project's equivalent) locally? Do the tests pass?
3. **Refine:** Did I remove the "AI fluff"? LLMs often add unnecessary comments or verbose explanations. Strip it down to the essentials.
4. **Disclose:** Add a note in your PR: _"I used [Tool Name] to help brainstorm the logic for [Section X], which I then manually verified and tested."_
   
**A Note on Burnout:** Maintainers are the backbone of the quantum world. When you submit unverified AI code, you are asking a human to do the "hard work" of debugging your bot. **Be a contributor, not a burden.**


_Disclosure: This Guide was built in collaboration with an LLM. We developed the language around our human-in-the-loop policy, building on feedback from maintainers, collaborators, and hackers from previous hackathons. Gemini 3 helped put all of this text into a step-by-step guide, which was then reviewed by multiple UF staff members and previous unitaryHACK maintainers before being shared with the public._








