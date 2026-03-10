# Design Patterns in Messaging API Project

## 1. Service Layer Pattern
- `MessageService` handles all message logic
- `app.py` only handles HTTP
- Benefit: separation of concerns

## 2. Strategy Pattern
- `BaseProvider` interface with multiple providers
- `FakeProvider1` and `FakeProvider2` can be swapped
- Benefit: easily extend to new providers

## 3. Dependency Injection
- Provider is passed to MessageService at initialization
- Code does not create provider internally
- Benefit: flexible, testable, reusable

## 4. Test Double / Fake Provider
- FakeProvider simulates responses (ACCEPTED / FAILED)
- Avoids calling real external service
- Benefit: isolated, deterministic tests

## 5. Example Flow
1. Client → POST /messages
2. API calls `MessageService.create_message()`
3. MessageService calls `provider.send_message()`
4. Stores message in in-memory dictionary
5. Webhook update changes message status