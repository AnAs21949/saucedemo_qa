# Selenium vs Playwright — Benchmark Comparison Report

## Project context

This report compares Selenium and Playwright on the same application (saucedemo.com) using identical test scenarios. Both suites were built in Python with pytest and the Page Object Model (POM) architecture, targeting the same 43 test cases across login, inventory, cart, checkout, and product detail features.

The goal is to provide a data-driven recommendation for QA teams evaluating which framework to adopt, based on real metrics — not opinions.

---

## Test environment

| Parameter              | Value                                      |
| ---------------------- | ------------------------------------------ |
| Application under test | [saucedemo.com](https://www.saucedemo.com) |
| Language               | Python 3.12                                |
| Test runner            | pytest 8.3.4                               |
| Architecture           | Page Object Model (POM)                    |
| CI platform            | GitHub Actions (ubuntu-latest)             |
| Test count             | 43 per suite                               |
| Reporting              | Allure + pytest-html                       |

---

## Results summary

| Metric                | Selenium | Playwright | Difference            |
| --------------------- | -------- | ---------- | --------------------- |
| CI execution time     | 1m 57s   | 1m 15s     | Playwright 36% faster |
| Local execution time  | ~12m 30s | ~2m 20s    | Playwright 81% faster |
| Lines of code (total) | 713      | 581        | Playwright 18% leaner |
| Tests passing         | 43/43    | 43/43      | Equal                 |
| Flaky tests observed  | 0        | 0          | Equal                 |

---

## Analysis by dimension

### 1. Execution speed

The most significant difference emerged in local execution. Selenium took approximately 12 minutes 30 seconds to run the full suite, while Playwright completed the same 43 tests in 2 minutes 20 seconds — an 81% reduction.

In CI (GitHub Actions), the gap narrowed to 36% because pipeline overhead (checkout, dependency installation, environment setup) added fixed time to both jobs. Still, Playwright finished in 1 minute 15 seconds compared to Selenium's 1 minute 57 seconds.

**Why the difference?** Selenium communicates with the browser through the WebDriver protocol, which involves HTTP requests between the test code and the browser driver. Playwright uses the Chrome DevTools Protocol (CDP), which communicates directly with the browser over a WebSocket connection — fewer hops, lower latency per action.

### 2. Lines of code and maintainability

Playwright required 581 lines of Python to implement the full suite, compared to 713 for Selenium — 18% less code for identical coverage.

The primary reason is Playwright's built-in auto-wait mechanism. In Selenium, every interaction needs explicit wait logic (WebDriverWait, expected conditions) to avoid flaky tests on dynamic pages. In Playwright, every action automatically waits for the element to be visible, enabled, and stable before interacting. This eliminates an entire category of boilerplate code from page objects and test files.

### 3. Browser and driver management

**Selenium** requires three components to be installed and version-matched independently: the Selenium library (pip), a browser (Chrome), and a browser driver (chromedriver). Chrome and chromedriver must be compatible versions — a Chrome auto-update can silently break the entire test suite. In CI, this means adding extra steps to install Chrome and manage drivers (via webdriver-manager or manual configuration).

**Playwright** bundles everything. A single `playwright install` command downloads the correct browser binaries for the installed Playwright version. There is no version mismatch risk. In CI, this reduces setup to one line.

This difference is clearly visible in the Dockerfiles: the Selenium Dockerfile requires a multi-line `apt-get` block to add Google's repository and install Chrome, while the Playwright Dockerfile needs only `playwright install --with-deps chromium`.

### 4. Reliability and flakiness

Neither suite produced flaky tests across all CI and local runs. This is largely attributable to the POM architecture and careful test design rather than framework choice.

However, Playwright's auto-wait mechanism provides a structural advantage for reliability. In Selenium, a missed or incorrectly configured wait is the most common source of test flakiness. Playwright eliminates this class of failure entirely by design.

### 5. CI/CD integration

Both frameworks integrate cleanly with GitHub Actions, running in parallel jobs on `ubuntu-latest`.

The Playwright job is simpler to configure: install Python, install dependencies, run `playwright install`, run tests. The Selenium job requires additional steps for Chrome installation and driver management.

Both jobs produce Allure and HTML reports as CI artifacts.

---

## Recommendation

For a team starting a new test automation project in 2025–2026, **Playwright is the stronger choice** for the following reasons: it executes faster (36–81% depending on environment), requires less code to maintain (18% fewer lines), eliminates browser/driver version management, and removes the most common source of test flakiness (missing waits) by design.

**Selenium remains relevant** in organizations with existing Selenium infrastructure, teams that need to test browsers not supported by Playwright (e.g., older IE/Edge versions), or projects where the larger Selenium ecosystem (Grid, extensive community resources) provides specific value.

The ideal approach — demonstrated in this project — is to understand both frameworks and make data-driven decisions based on project requirements.

---

## Repository

All source code, test suites, CI configuration, and Dockerfiles are available at: [github.com/AnAs21949/saucedemo_qa](https://github.com/AnAs21949/saucedemo_qa)
