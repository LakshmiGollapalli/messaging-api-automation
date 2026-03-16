## Design Patterns / Flow

### 1. Service Layer Pattern
- `MessageService` handles all message logic  
- `app.py` only handles HTTP requests  
- **Benefit:** separation of concerns, easier to maintain

### 2. Strategy Pattern
- `BaseProvider` interface allows different providers  
- Currently using `FakeProvider` (simulated)  
- **Benefit:** can extend to other providers in the future  

### 3. Dependency Injection
- Provider is passed to `MessageService` at initialization  
- Code does **not create provider internally**  
- **Benefit:** flexible, testable, reusable  

### 4. Test Double / Fake Provider
- `FakeProvider` simulates responses (`ACCEPTED` / `FAILED`)  
- Avoids calling a real external service  
- **Benefit:** isolated, deterministic tests

### 5. Timestamp Handling
- `created_at` → automatically set when message is created  
- `updated_at` → updated on webhook calls  
- **Benefit:** traceable message lifecycle, easier future DB integration  

### 6. Example Flow
1. Client → POST `/messages`  
2. API calls `MessageService.create_message()`  
3. MessageService calls `provider.send_message()`  
4. Stores message in **in-memory dictionary**  
5. Webhook update changes message status (`SENT → DELIVERED`) with timestamp  

## 7. Exception Handling Pattern

- Implemented global exception handler using Flask `@app.errorhandler`.
- Standardized error response format.
- Ensures consistent API behavior across endpoints.

## 8. Logging Pattern

- Custom logger wrapper implemented.
- Sensitive data masking applied before logging.
- Structured log format used:
  timestamp | level | module | message
- Designed to support future file-based logging and cloud deployment.

### 9. AI-Assisted Guidance
- Design and test approaches were refined with **AI-assisted guidance**  
- **Benefit:** demonstrates ability to leverage modern tools for learning and productivity  