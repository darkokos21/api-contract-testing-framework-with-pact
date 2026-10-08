# ContractGuard

### API Contract Testing & Compatibility Framework



ContractGuard is a production-inspired API contract testing framework built with **Python, pytest, Pact, FastAPI, Docker and GitHub Actions**.

The project demonstrates how **consumer-driven contract testing** can detect breaking API changes before they reach deployment.

---

## Why Contract Testing?

In distributed systems, API changes can unintentionally break consumers.

Traditional integration testing often discovers these problems only after services are deployed together.

Contract testing shifts this validation earlier by allowing the consumer to define its expectations and the provider to verify that it still satisfies them.

ContractGuard demonstrates this workflow using **Pact**.

---

## Architecture

```text
┌──────────────────────┐
│   OrderService       │
│      Consumer        │
│                      │
│ Python + pytest      │
│ Pact Consumer Test   │
└──────────┬───────────┘
           │
           │ Generates Pact Contract
           ▼
┌──────────────────────┐
│      Pact Broker     │
│                      │
│ Contract Repository  │
│ Compatibility Matrix │
└──────────┬───────────┘
           │
           │ Provider Verification
           ▼
┌──────────────────────┐
│   ProductService     │
│       Provider       │
│                      │
│ FastAPI              │
│ pytest + Pact        │
└──────────────────────┘

           │
           ▼
     can-i-deploy
           │
           ▼
     Deployment Gate
```

---

## Technology Stack

| Technology     | Purpose                            |
| -------------- | ---------------------------------- |
| Python         | Test automation                    |
| pytest         | Test execution                     |
| Pact           | Consumer-driven contract testing   |
| FastAPI        | Provider API                       |
| Requests       | HTTP client                        |
| Pact Broker    | Contract storage and compatibility |
| Docker Compose | Local service orchestration        |
| GitHub Actions | CI/CD                              |
| Pact CLI       | Publishing and deployment checks   |

---

## Project Structure

```text
contract-guard/
│
├── consumer/
│   ├── src/
│   │   └── product_client.py
│   ├── tests/
│   │   ├── conftest.py
│   │   └── test_product_contract.py
│   ├── conftest.py
│   └── requirements.txt
│
├── provider/
│   ├── app/
│   │   └── main.py
│   ├── tests/
│   │   ├── conftest.py
│   │   └── test_provider_contract.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── pacts/
│   └── .gitkeep
│
├── broker/
│   └── docker-compose.yml
│
├── .github/
│   └── workflows/
│       └── contract-tests.yml
│
├── docker-compose.yml
├── pytest.ini
├── .gitignore
├── .env.example
├── README.md
└── LICENSE
```

---

## Contract Testing Flow

### 1. Consumer defines expectations

The consumer defines the API interaction it expects from `ProductService`.

Example:

```python
(
    pact.upon_receiving("a request for an existing product")
    .given("product 101 exists")
    .with_request(
        method="GET",
        path="/products/101",
    )
    .will_respond_with(200)
    .with_body(
        {
            "id": match.integer(101),
            "name": match.regex(
                "Laptop",
                regex=r"^Laptop$",
            ),
            "price": match.decimal(1299.99),
            "available": match.boolean(True),
        }
    )
)
```

This expectation becomes the contract between `OrderService` and `ProductService`.

---

### 2. Pact generates the contract

Run the consumer tests:

```bash
cd consumer
pytest
```

The generated Pact file is written to:

```text
pacts/OrderService-ProductService.json
```

Generated Pact files are ignored by Git and regenerated during the test pipeline.

---

### 3. Contract is published

The contract is published to the Pact Broker:

```bash
pact broker publish "pacts/OrderService-ProductService.json" \
  --consumer-app-version "${GITHUB_SHA}" \
  --branch "${GITHUB_REF_NAME}" \
  --broker-base-url "${PACT_BROKER_BASE_URL}" \
  --broker-username "${PACT_BROKER_USERNAME}" \
  --broker-password "${PACT_BROKER_PASSWORD}" \
  --validate
```

The Pact Broker becomes the central source of truth for contract compatibility.

---

### 4. Provider verifies the contract

`ProductService` verifies that its current implementation satisfies the consumer contract.

The provider verification uses the Pact Broker:

```python
verifier = (
    Verifier(PROVIDER_NAME)
    .add_transport(url=PROVIDER_URL)
    .broker_source(
        broker_url,
        username=broker_username,
        password=broker_password,
    )
    .state_handler(
        f"{PROVIDER_URL}/_pact/provider-state",
        body=True,
    )
)
```

If the provider no longer satisfies the contract, the verification fails.

---

### 5. Deployment compatibility is checked

After provider verification succeeds, the provider version is recorded as deployed:

```bash
pact broker record-deployment \
  --pacticipant ProductService \
  --version "${GITHUB_SHA}" \
  --environment test
```

The consumer version can then check whether it is safe to deploy:

```bash
pact broker can-i-deploy \
  --pacticipant OrderService \
  --version "${GITHUB_SHA}" \
  --to-environment test
```

If compatibility is not confirmed, the deployment gate fails.

---

# Running Locally

## 1. Clone the repository

```bash
git clone https://github.com/darkokos21/api-contract-testing-framework-with-pact.git
cd api-contract-testing-framework-with-pact
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Or on Linux/macOS:

```bash
source .venv/bin/activate
```

---

## 3. Install consumer dependencies

```bash
pip install -r consumer/requirements.txt
```

---

## 4. Install provider dependencies

```bash
pip install -r provider/requirements.txt
```

---

# Start the Provider and Pact Broker

Start the complete environment with Docker Compose:

```bash
docker compose up -d
```

Check running containers:

```bash
docker ps
```

The environment contains:

- PostgreSQL
- Pact Broker
- ProductService

---

# Pact Broker

The Pact Broker is available at:

```text
http://localhost:9292
```

Default demo credentials:

```text
Username: pact
Password: pact
```

The broker stores:

- Consumer contracts
- Provider verification results
- Application versions
- Branches
- Environments
- Deployment records
- Compatibility information

---

# Verify the Provider

Run provider verification:

```bash
pytest provider/tests/test_provider_contract.py -v
```

A successful verification confirms that the provider satisfies the consumer contract.

---

# Demonstrating a Breaking Change

ContractGuard includes an intentional breaking-change scenario.

The consumer expects:

```json
{
  "id": 101,
  "name": "Laptop",
  "price": 1299.99,
  "available": true
}
```

The contract requires the exact value:

```python
"name": match.regex(
    "Laptop",
    regex=r"^Laptop$",
)
```

Now change the provider response from:

```json
"name": "Laptop"
```

to:

```json
"name": "Gaming Laptop"
```

Rebuild the provider:

```bash
docker compose up -d --build provider
```

Run provider verification again:

```bash
pytest provider/tests/test_provider_contract.py -v
```

The verification fails because:

```text
Expected 'Gaming Laptop' to match '^Laptop$'
```

This demonstrates how Pact catches an incompatible API change before deployment.

Restore the provider implementation:

```json
"name": "Laptop"
```

Then rebuild:

```bash
docker compose up -d --build provider
```

The contract verification should pass again.

---

# CI/CD Pipeline

GitHub Actions executes the complete contract testing workflow in a single job.

The pipeline performs:

```text
Checkout
   ↓
Install Python dependencies
   ↓
Run Consumer Contract Tests
   ↓
Generate Pact Contract
   ↓
Start PostgreSQL + Pact Broker + Provider
   ↓
Wait for Pact Broker
   ↓
Wait for Provider
   ↓
Publish Pact
   ↓
Verify Provider Contract
   ↓
Record Provider Deployment
   ↓
can-i-deploy
```

Keeping these steps in a single CI job ensures the Pact Broker state is available throughout the complete workflow.

---

# Quality Gate

The final deployment decision is controlled by Pact:

```bash
pact broker can-i-deploy \
  --pacticipant OrderService \
  --version "${GITHUB_SHA}" \
  --to-environment test
```

### Successful scenario

```text
Consumer contract
        ↓
Provider verification
        ↓
Deployment recorded
        ↓
Compatibility confirmed
        ↓
Deployment allowed
```

### Breaking-change scenario

```text
Consumer contract
        ↓
Provider verification
        ↓
Contract mismatch
        ↓
Verification fails
        ↓
Deployment blocked
```

This creates a practical **API compatibility quality gate** inside CI/CD.

---

# What This Project Demonstrates

This project demonstrates practical experience with:

- Consumer-driven contract testing
- Pact
- Pact Broker
- Provider verification
- API compatibility testing
- Python test automation
- pytest
- FastAPI
- Docker Compose
- GitHub Actions
- CI/CD quality gates
- Deployment compatibility checks
- Breaking API change detection
- Versioned contracts
- Provider states
- Automated integration testing

It also demonstrates an important QA principle:

> API compatibility should be validated before deployment, not after consumers break.

---

# Future Extensions

Potential future improvements include:

- Multiple consumers
- Multiple providers
- Authentication contract testing
- Schema evolution scenarios
- Pact Broker environments
- Release/version compatibility dashboards
- Contract testing for asynchronous messaging
- Integration with Jira or Slack
- Automated rollback on contract incompatibility

These are intentionally kept outside the initial implementation to keep the framework focused and easy to understand.

---

# Portfolio Objective

ContractGuard was created as a **portfolio-quality QA Automation / SDET project** demonstrating how modern teams can combine:

```text
API Testing
     +
Consumer-Driven Contracts
     +
Provider Verification
     +
Docker
     +
CI/CD
     +
Deployment Gates
```

The goal is to demonstrate practical knowledge of **API automation, distributed-system compatibility, CI/CD quality engineering and modern contract testing practices**.

The project is intentionally small enough to understand quickly while still representing a realistic engineering workflow.
