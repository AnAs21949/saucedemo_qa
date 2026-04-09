# SauceDemo QA — Selenium vs Playwright Comparison

A complete QA automation portfolio project comparing **Selenium** and **Playwright** on the same web application ([saucedemo.com](https://www.saucedemo.com)), using identical test scenarios, architecture, and CI/CD pipeline. Built to demonstrate end-to-end quality engineering skills — from test strategy to execution to reporting.

---

## Why this project exists

Most QA portfolios show a single test suite running against a demo site. This project goes further: it implements the **same 43 test cases** in both Selenium and Playwright, then compares them with real data across speed, code volume, setup complexity, reliability, and CI integration. The result is a data-driven benchmark that mirrors the kind of framework evaluation a QA lead would perform before choosing a tool for a real project.

---

## QA strategy

### Approach

The test strategy follows a **risk-based approach** organized around the core user journeys of an e-commerce application: authentication, product browsing, cart management, and checkout. Test cases are categorized into three tiers using pytest markers.

**Smoke tests** cover the critical path — login with valid credentials, add a product to cart, complete a checkout. These run first and must all pass before regression tests execute. **Regression tests** cover broader functionality — sorting products, removing items from cart, verifying price calculations, multi-product checkout flows. **Negative tests** validate error handling — locked-out users, empty form submissions, invalid credentials.

### Test design

All tests are built on the **Page Object Model (POM)** architecture. Each page of the application has a corresponding Python class that encapsulates its locators and interactions. Tests never interact with raw selectors — they call page methods like `login_page.login(username, password)` or `cart_page.remove_item(item_name)`. This makes tests readable, maintainable, and framework-agnostic at the test level.

Test data is externalized in `data/project_data.json`, keeping test logic separate from test data. This allows the same test to run against multiple user types (standard, locked-out, problem, performance-glitch) without code duplication.

### Coverage

The 43 test cases are distributed across 5 functional areas, mapped to 4 Jira epics and 13 user stories.

| Area                         | Tests | Coverage                                                            |
| ---------------------------- | ----- | ------------------------------------------------------------------- |
| Login & authentication       | 8     | Valid login, invalid credentials, locked-out user, logout           |
| Inventory & product browsing | 10    | Product listing, sorting (A-Z, Z-A, price asc/desc), product detail |
| Cart management              | 9     | Add/remove single and multiple items, cart persistence, cart badge  |
| Checkout flow                | 12    | Complete purchase, form validation, price verification, cancel flow |
| Product detail page          | 4     | Navigation, add to cart from detail, back button                    |

---

## Project structure

```
saucedemo_qa/
├── selenium_tests/
│   ├── pages/              # Selenium POM classes
│   ├── tests/              # Selenium test files
│   ├── utils/              # Config loader, helpers
│   └── requirements.txt
├── playwright_tests/
│   ├── pages/              # Playwright POM classes
│   ├── tests/              # Playwright test files
│   ├── utils/              # Config loader, helpers
│   └── requirements.txt
├── data/
│   └── project_data.json   # Shared test data
├── benchmark/
│   └── BENCHMARK_REPORT.md # Framework comparison with metrics
├── .github/
│   └── workflows/
│       └── tests.yml       # CI/CD pipeline
├── Dockerfile.selenium     # Containerized Selenium execution
├── Dockerfile.playwright   # Containerized Playwright execution
├── docker-compose.yml      # Run both suites with one command
├── pytest.ini              # Pytest configuration
└── .dockerignore
```

---

## Key results

| Metric               | Selenium | Playwright |
| -------------------- | -------- | ---------- |
| CI execution time    | 1m 57s   | 1m 15s     |
| Local execution time | ~12m 30s | ~2m 20s    |
| Lines of code        | 713      | 581        |
| Tests passing        | 43/43    | 43/43      |
| Flaky tests          | 0        | 0          |

Playwright runs **36% faster in CI** and **81% faster locally**, with **18% less code** for identical coverage. Full analysis available in the [Benchmark Report](benchmark/BENCHMARK_REPORT.md).

---

## Tech stack

**Languages & frameworks:** Python 3.12, Selenium 4.27, Playwright, pytest 8.3

**Architecture:** Page Object Model (POM), data-driven testing (JSON)

**Reporting:** Allure, pytest-html

**CI/CD:** GitHub Actions — two parallel jobs (Selenium + Playwright), triggered on push to main

**Containerization:** Docker — separate Dockerfiles per suite, docker-compose for orchestration

**Project management:** Jira Scrum board — 4 epics, 13 user stories, 34 test cases

---

## How to run

### Prerequisites

Python 3.12+, pip, and Google Chrome (for Selenium) installed locally.

### Selenium suite

```bash
cd saucedemo_qa
pip install -r selenium_tests/requirements.txt
pytest selenium_tests/ --alluredir=allure-results
```

### Playwright suite

```bash
cd saucedemo_qa
pip install -r playwright_tests/requirements.txt
playwright install --with-deps chromium
pytest playwright_tests/
```

### Docker (both suites)

```bash
docker-compose up --build
```

### CI/CD

Tests run automatically on every push to `main` via GitHub Actions. Both suites execute in parallel on `ubuntu-latest`.

---

## Certifications

**ISTQB® Certified Tester — Foundation Level (CTFL 4.0)**

---

## Author

**Anas ABID** — Junior QA Automation Engineer

Bac+5 Engineering degree (Aéronautique & Systèmes Embarqués), ENSA Berrechid

[LinkedIn](https://www.linkedin.com/in/anas-abid) · [GitHub](https://github.com/AnAs21949)
