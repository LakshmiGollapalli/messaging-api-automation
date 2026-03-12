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
- Introduced support for multiple providers:
  - `ReliableMessageProvider`
  - `FastMessageProvider`
- Provider selection made configurable using environment variables.
- Removed hardcoded provider initialization from `app.py`.
- Added centralized logging across the application.
- Implemented masking of sensitive data (recipient phone numbers) in logs.

### Logging Improvements
Logging was added to the following components:

- `MessageService`
- Provider classes
- Webhook delivery updates

Sensitive data is masked to prevent exposure in logs.

### Benefit
- Improves system observability.
- Enables flexible provider selection without code changes.
- Simulates production-grade logging practices.

---

## Future Enhancements

Planned improvements to continue evolving the system:

- Add **request ID tracing** for end-to-end request tracking.
- Introduce **database persistence** instead of in-memory storage.
- Implement **retry mechanisms** for provider failures.
- Add **CI/CD pipeline integration** (e.g., automated testing and deployment).
- Add **metrics and monitoring** for system health.

---

## Summary

This project demonstrates how a messaging service can evolve from a simple prototype into a more production-ready system by gradually introducing:

- Better architecture
- Configurable integrations
- Observability improvements
- Extensibility for future enhancements
