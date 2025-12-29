# Pytest Regression Analysis Framework

## Overview
This project is a production-grade test automation framework built using **pytest**, designed to go beyond basic test execution by providing **historical test analytics, regression detection, and CI/CD integration**.

Instead of treating test results as disposable, the framework persists results in a database and analyzes them across runs and application versions to detect:
- True regressions
- Flaky tests
- Fixed tests
- Newly added tests (pass/fail aware)

The framework is designed with **scalability, correctness, and CI-readiness** in mind.

---

## Key Features

### 1. Automated Result Capture
- Uses `pytest_runtest_logreport` hook to capture:
  - Test name (including parametrized cases)
  - PASS / FAIL status
  - Failure details
  - Per-test execution duration
- No test-level code pollution — tests remain clean.

---

### 2. Run-Level Tracking
- Each pytest execution is identified by a unique **run_id**  
  (`timestamp + machine IP`)
- Enables multiple executions per version without overwriting data.
- Supports flaky test analysis across runs.

---

### 3. Database-Backed Test Analytics
- Test results stored in **MySQL (Dockerized)**.
- Schema designed for:
  - Historical tracking
  - Parallel execution safety
  - Future extensibility

Stored fields include:
- run_id
- app_version
- test_name
- status
- duration
- failure details
- timestamp

---

### 4. Regression Detection
Compares **previous vs current application versions** using aggregated results:

| Scenario | Classification |
|--------|----------------|
| PASS → FAIL | Regression |
| FAIL → PASS | Fixed |
| FAIL intermittently | Flaky |
| PASS consistently | Stable |
| New test failing | Regression |
| New test passing | New coverage |

Flakiness is determined using **pass/fail ratios across runs**, not single executions.

---

### 5. HTML Regression Report
- Generates a standalone HTML report after test execution.
- Highlights:
  - Regressions (red)
  - Fixed tests (green)
  - Flaky tests (orange)
  - New tests (pass/fail color-coded)
- Includes total pytest session duration.
- Designed for CI/CD artifact publishing.

---

### 6. CI/CD Ready
- Works with GitHub Actions and Jenkins.
- Fails pipeline **only on real regressions or failing new tests**.
- Supports parallel execution (`pytest-xdist`) without corrupting results.

---

## Technology Stack
- **Python**
- **pytest**
- **MySQL (Docker)**
- **pytest hooks & fixtures**
- **HTML reporting**
- **GitHub Actions / Jenkins**

---

## Why This Framework
Most test frameworks answer:
> “Did tests pass?”

This framework answers:
> “Did the application regress, or are tests flaky?”

---


