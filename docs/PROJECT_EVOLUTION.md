# Project Evolution

This document tracks the incremental evolution of the Messaging Service project.  
The goal is to simulate how a real backend service evolves over time through multiple development sprints and architectural improvements.

---

## Overview

The project implements a simple message sending system with the following goals:

- Demonstrate backend service architecture
- Simulate external provider integrations
- Implement asynchronous delivery updates via webhook
- Improve observability and extensibility over time

The system is built using a layered architecture:

- **Flask API Layer** – Handles incoming client requests
- **Service Layer** – Contains business logic (`MessageService`)
- **Provider Layer** – Integrates with external message providers
- **Utilities** – Logging, masking, configuration helpers

---

## Sprint 0 – Initial Messaging Service

### Features
- Implemented a Flask API for sending messages.
- Introduced `MessageService` to handle message processing.
- Created a `FakeProvider` to simulate sending messages.
- Implemented webhook endpoint for delivery status updates.
- Used in-memory storage for messages.

### Purpose
Establish a basic system architecture separating API handling from business logic.

---

## Sprint 1 – Timestamp Support

### Changes
- Added `created_at` and `updated_at` fields to message records.
- Webhook updates now update the `updated_at` timestamp.
- Improved tracking of message lifecycle events.

### Benefit
Provides better traceability and prepares the system for future database persistence.

---

## Sprint 2 – Multiple Providers and Centralized Logging

### Changes

- Introduced support for multiple message providers:
  - `ReliableMessageProvider`
  - `FastMessageProvider`

- Removed the earlier `FakeProvider` implementation used during initial development.
- Updated the provider layer so that `MessageService` can dynamically load the configured provider.
- Provider selection is controlled through configuration (environment variable).

### Logging Improvements

- Added centralized logging across the application.
- Logging introduced in:
  - `MessageService`
  - Provider classes
  - Webhook delivery updates

- Sensitive data such as recipient phone numbers is masked in logs (all digits masked except last four).

- This change simulates real-world integrations with external messaging providers while improving system observability through structured logging.
---

## Sprint 3 – Request Tracking and Enhanced Logging

### Problem
As the system evolved with multiple providers and asynchronous webhook updates, debugging message flows became harder. Logs needed better traceability and structure to help identify issues across different components.

### Solution
Introduced request-level tracking and improved the logging system for better observability.

---

### Request ID Tracking

A `request_id` is generated for each incoming API request. This allows multiple messages created from the same request to be correlated in logs and system traces.

Each message stored in the `messages` dictionary now contains:

- `message_id`
- `request_id`
- `receiver`
- `content`
- `status`
- `provider_id`

Webhook updates continue to use `message_id` to update message status.

---

### Logging Improvements

#### 1. Daily Log Files

Logs are written to a file with the current date appended to the filename.

Example:
logs/app_2026-03-13.log
logs/app_2026-03-14.log

Logs are appended to the existing file during each run instead of overwriting previous logs.

---

#### 2. Structured Logging (Key–Value Format)

Logs were previously printed using dictionary format.

Example (old format):
Creating message for receiver {'receiver': '****3210'}

This was replaced with **structured key–value logging**, which is easier to search and analyze in log aggregation systems.

Example (new format):
Message created  message_id=1 request_id=21cd569c-e083-4125-a702-7b20799de530

### Benefits

- Improved debugging and traceability
- Easier log searching and filtering
- Log files organized by date
- Better correlation of events using `request_id`
## Sprint 4 – Continuous Integration (CI)

Introduced automated CI pipeline using **GitHub Actions** to ensure code quality and test reliability.

### Key Enhancements

- Added **GitHub Actions workflow** (`.github/workflows/ci.yml`)
- Automated execution of:
  - **Flake8** for static code analysis
  - **Pytest** for running test suite
- Added `.flake8` configuration file to define linting rules
- Ensured CI pipeline runs on repository pushes and pull requests
- Fixed dependency compatibility by pinning **Werkzeug version** with Flask

### CI Pipeline Flow

1. Checkout repository
2. Setup Python runtime
3. Install project dependencies
4. Run static code analysis (Flake8)
5. Execute automated tests (Pytest)

### Outcome

The project now supports **automated validation of code quality and functionality**, ensuring new changes do not introduce regressions.

## Sprint 5 – Exception Handling & CI Improvements

### Added:
- Centralized exception handling
- Health check endpoint and also added root / endpoint
- Improved pytest configuration
- GitHub Actions CI pipeline
- Logging improvements

### Notes:
- Tests run automatically on push to main branch
- Code quality enforced using flake8 in CI

## Future Enhancements

Planned improvements to continue evolving the system:


- Introduce **database persistence** instead of in-memory storage.
- Implement **retry mechanisms** for provider failures.
- Add **CI/CD pipeline integration** (e.g., automated testing and deployment).
- Add **metrics and monitoring** for system health.

---

