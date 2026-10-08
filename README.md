# ContractGuard

### API Contract Testing & Compatibility Framework

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Pact](https://img.shields.io/badge/Pact-Contract%20Testing-purple)
![FastAPI](https://img.shields.io/badge/FastAPI-Provider-green)
![pytest](https://img.shields.io/badge/pytest-Test%20Automation-yellow)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-black)

ContractGuard is a production-inspired API contract testing framework built with
Python, pytest, Pact, FastAPI, Docker and GitHub Actions.

The project demonstrates how consumer-driven contract testing can detect
breaking API changes before they reach deployment.

---

## Why Contract Testing?

Traditional API testing can confirm that a provider works correctly in
isolation, but it does not always prove that existing consumers can still
interact with a changed provider.

Contract testing addresses this compatibility problem.

ContractGuard demonstrates:

- Consumer-driven API contracts
- Pact consumer testing
- Provider contract verification
- Pact Broker integration
- Provider state management
- Contract versioning
- CI/CD compatibility checks
- Deployment safety gates

---

## Architecture

```text
                   ContractGuard
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌─────────────────┐             ┌─────────────────┐
│  OrderService   │             │ ProductService  │
│    Consumer     │             │    Provider     │
│                 │             │                 │
│ Python + pytest │             │ FastAPI         │
└────────┬────────┘             └────────┬────────┘
         │                               │
         │ Generate Pact                 │ Verify Pact
         ▼                               │
┌──────────────────────────────────────────────┐
│                  Pact Broker                 │
│                                              │
│ Contracts + Verification Results + Matrix   │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ can-i-deploy    │
              │ Deployment Gate │
              └─────────────────┘