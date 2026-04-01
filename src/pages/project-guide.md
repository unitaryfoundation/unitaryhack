---
title: Project Maintainer Guide
layout: project-guide.njk
metaDescription: Helpful information for project maintainers participating in unitaryHACK
date: 2026-04-01
permalink: /project-guide/index.html
eleventyNavigation:
  key: Maintainers
  order: 4
---

Our goal at Unitary Foundation is to build a quantum technology ecosystem that benefits the most people. That starts by **supporting and growing the great ecosystem of projects already out there that is maintained by awesome folks like you**.

It is always important for projects to find skilled and committed contributors that can do things like help develop new functionality, help with maintenance, and write tests and documentation. This can be challenging in open source in general, but can be especially difficult for open source projects that need specialized skill sets like quantum computing. **unitaryHACK aims to show folks what amazing projects are already out there, helping drive quantum computing forward, and helping you find new contributions for your projects.**

We have some outlines below for what you can expect before and during the event, as well as [the rules for the event]({{ '/rules/' | url }}).

## Maintainer Timeline 🗓️

* **ASAP** Maintainers from invited projects fill out our participation form (reach out to the UF team for access)
* **Mid-April** Bounty forms sent to participating maintainers
* **May 4th** Deadline to submit bounties for review
* **May 29th** All issues must be finalized
* **May 27 at 12:30 pm ET** Maintainers get together + Q&A
    - Review of the event + rules
    - Answer any questions folks have about the event
    - Give a short intro about your project
* **June 3rd** unitaryHACK opens
* **June 17th** unitaryHACK closes
* **June 24th** Awardees finalized


## Before the Hack ⌚

### Setting up your Github Repo
Get your project ready for more eyes on it! Some tips:
* If you have a `good first issue` label, it will be a good time to review it.
* Ensure you have `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` files at the root of your repo (or similar) so folks can learn how they should make their contributions.

In April, we will distribute a form to finalize which issues you'd like to put up for bounties, and the associated rewards. We will review the issues to make sure there is a good balance across the event. **We are keeping the bounties hidden until the day of the event to ensure fairness.**

### How to choose good issues for participants
To make sure that everyone can participate in the hackathon, we encourage project maintainers to tag a variety of issues that may or may not include quantum content, may or may not require devops skills, etc. We understand projects can be very targeted so if this is not possible that's totally fine! Our goal is to help connect eager and skilled contributors to your projects to help make the quantum open source ecosystem better 💖 We encourage you to reference our [Best practices for unitaryHACK Issues]({{ '/best-practices/' | url }}). for help in refining your issues to set contributors up for success.

### Examples of Good Issues
- New features (quantum):
    - [Example 1](https://github.com/unitaryfoundation/ucc/issues/170) (UCC)
    - [Example 2](https://github.com/qBraid/qbraid-qir/issues/78) (qBraid)
    - [Example 3](https://github.com/qutip/QuantumToolbox.jl/issues/95) (quantum-toolbox.jl)
- Bug fixes:
    - [Example 1](https://github.com/qutip/qutip/issues/2400) (QuTiP)
    - [Example 2](https://github.com/amazon-braket/amazon-braket-sdk-python/issues/603) (Amazon Braket SDK)
    - [Example 3](https://github.com/unitaryfoundation/mitiq/issues/2354) (Mitiq)
- Tests & profiling:
    - [Profiling example](https://github.com/unitaryfoundation/mitiq/issues/2161) (Mitiq)
    - [Tests example 1](https://github.com/scqubits/scqubits/issues/220) (SC Qubits)
    - [Tests example 2](https://github.com/qBraid/qBraid/issues/624) (qBraid)
- Docs & examples:
    - [Docs example](https://github.com/NVIDIA/cuda-quantum/issues/1624) (CUDA Quantum)
    - [Tutorial example 1](https://github.com/Quantum-Universal-Education/Quantum-Universal-Education.github.io/issues/16) (Universal Quantum Education)
    - [Tutorial Example 2](https://github.com/tencent-quantum-lab/tensorcircuit/issues/212) (TensorCircuit)
- Refactoring:
    - [Example 1](https://github.com/vprusso/toqito/issues/168) (Toqito)
    - [Example 2](https://github.com/Qiskit/openqasm3_parser/issues/163) (QASM3 Parser)
    - [Example 3](https://github.com/pasqal-io/qadence/issues/368) (Qadence)


## During the Hack 🛠️

As the hackathon progresses (and sometimes right away if there are eager folks who read up on the project), you should get some useful PRs! **If a PR does not meet a minimum bar for quality, or if another PR has been accepted, please provide some details through PR comments that it is not accepted.**

For bountied issues, once you have accepted a pull request (or closed an issue) please assign the hacker to the issue so that our bots can understand it as complete, and distribute the bounty accordingly. There will be no split bounties this year. **Bounties will not be distributed until the end of the event, so if there is any confusion, please don't hesitate to reach out** to [hack@unitary.foundation](mailto:hack@unitary.foundation).

### Maintainer Tips and Tricks During the HACK
- We recommend turning on github notifications for issue/PR events, so you can respond to activity as quickly as your bandwidth allows. The quicker hackers receive responses to their questions and/or PRs, the less confusion there is in general
- Stay active in the UF Discord server, specifically the unitaryHACK channel. You can easily share information there and quickly ask questions to the UF team 
- Reminder that a goal of unitaryHACK is to retain contributors to your projects. This is an opportunity to cultivate lasting relationships with the hackers so you can continue to work with them well into the future!

### AI Moderation
* We recommend incorporating an LLM to oversee initial PR reviews for all reviews, several fellow maintainers have suggested CodeRabbit. This will cut down on you personally having to review submissions that may not be as serious.
* Familiarize yourself with the unitaryHACK [Hacker Guide to Ethical AI] and feel free to share it along to any hackers you think are in danger of violating the guide.
* Loop in Veena if you’re not sure of how to proceed


## FAQ 🤔

### What will be expected of me/my team?
In preparation for the hackathon, your project will need to curate a series of bountied issues. These can range in difficulty, however they should be well scoped and provide slightly more background than normal. This way, an external contributor with the right skills can get oriented quickly.

During the hackathon the expectation is that PRs opened by hackers are addressed in a reasonable time frame. **Since many hackers are contributing on nights and weekends, giving feedback with ample time to make subsequent changes is very important.**

### What does the maintainer workflow look like? 
Logistically, these are the steps a maintainer will take during the hackathon.
1. Hacker opens a PR on your project.
2. Maintainer reviews/requests changes as needed.
3. When PR is merged (or approved),  maintainer adds hacker to the issue as an `assignee` so our bots can understand who the bounty should be distributed to. If there are multiple hackers working as a team, have them decide who will receive the bounty and only assign that one hacker.

### How much activity should we expect to see?

In previous years we've seen some projects garner more attention, and some less. Generally, the more time you've taken to carefully select, scope, and detail issues to be put up for bounty, the more attention you should expect your project to see. 

### I closed an issue, but the unitaryHACK website still shows it as open. What should I do?

A bot will scrape all the issues participating in unitaryHACK **every 2 hours** during the event.
If it has been more than 4 hours since you closed the issue, and it still shows as open, please reach out to the UF team on the `uhack-maintainers` channel on Discord.

### Who owns the code contributed during unitaryHACK? 

Please note that the Unitary Foundation is unable to provide specific legal advice. That being said, contributions made to a tool typically fall under the tool's open source license unless otherwise explicitly stated.

### What should I do if I have questions or need support? 

Reach out to the UF team at [hack@unitary.foundation](mailto:hack@unitary.foundation). Or if you need to get to us even quicker, ping Veena on the UF Discord server. 

## Helpful resources 🤝

- [A maintainers guide to Hacktoberfest](https://medium.com/gitcoin/a-maintainers-guide-to-hacktoberfest-21405c8ff09f)
- [Tips and tricks for maintaining your repo and your mental health](https://www.twilio.com/blog/how-to-hacktoberfest-tips-and-tricks-for-maintaining-your-repo-and-your-mental-health)
- [Promoting your open source project](https://github.com/zenika-open-source/promote-open-source-project/blob/master/README.md)
- [Write the docs guide](https://www.writethedocs.org/guide/)
