"""
test_messages.py

This file contains API-level test cases for:

- Message creation
- Input validation
- Status retrieval
- Webhook update
- Error handling
"""

import pytest
from datetime import datetime, timezone

# ---------------------------------------------------
# Test: Create message (may fail randomly due to provider)
# ---------------------------------------------------


@pytest.mark.xfail(reason="Provider may randomly return 503, expected failure")
def test_create_valid_message(client):
    """
    Test successful message creation.

    Expected:
    - HTTP 201 (Created)
    - Response contains id and status
    """

    response = client.post("/messages", json={
        "receiver": "9876543210",
        "content": "Hello"
    })

    assert response.status_code == 201

    data = response.get_json()
    assert "id" in data
    assert data["status"] == "SENT"


def test_invalid_phone_number(client):
    """
    Test invalid phone number.

    Expected:
    - HTTP 400 (Bad Request)
    - Error message returned
    """

    response = client.post("/messages", json={
        "receiver": "123",   # Invalid number
        "content": "Hello"
    })

    assert response.status_code == 400


def test_empty_content(client):
    """
    Test empty message content.

    Expected:
    - HTTP 400 (Bad Request)
    """

    response = client.post("/messages", json={
        "receiver": "9876543210",
        "content": ""
    })

    assert response.status_code == 400

# ---------------------------------------------------
# Test: Get existing message (depends on message being created)
# ---------------------------------------------------


@pytest.mark.xfail(reason="Provider may randomly fail or ID may not exist on first run")
def test_get_existing_message(client):
    """
    Create message then fetch it.

    Expected:
    - HTTP 200
    """

    create_response = client.post("/messages", json={
        "receiver": "9876543210",
        "content": "Test"
    })

    message_id = create_response.get_json()["id"]

    get_response = client.get(f"/messages/{message_id}")

    assert get_response.status_code == 200


def test_get_non_existing_message(client):
    """
    Fetch message that does not exist.

    Expected:
    - HTTP 404 (Not Found)
    """

    response = client.get("/messages/9999")
    assert response.status_code == 404


# ---------------------------------------------------
# Test: Webhook / update status (provider may fail randomly)
# ---------------------------------------------------
@pytest.mark.xfail(reason="Provider may randomly fail when updating status")
def test_webhook_update_success(client):
    """
    Simulate webhook delivery update.

    Expected:
    - HTTP 200
    - Status updated to DELIVERED
    """

    create_response = client.post("/messages", json={
        "receiver": "9876543210",
        "content": "Webhook test"
    })

    data = create_response.get_json()
    provider_id = data["provider_id"]
    current_timestamp = datetime.now(timezone.utc).isoformat()
    webhook_response = client.post("/delivery-update", json={
        "provider_id": provider_id,
        "status": "DELIVERED",
        "timestamp": current_timestamp
    })

    assert webhook_response.status_code == 200
    updated_at = datetime.fromisoformat(webhook_response.json["updated_at"])

    # assert it matches what you sent
    assert updated_at.isoformat() == current_timestamp
    updated_data = webhook_response.get_json()

    assert updated_data["status"] == "DELIVERED"


def test_webhook_invalid_provider(client):
    """
    Webhook with unknown provider_id.

    Expected:
    - HTTP 404
    """

    response = client.post("/delivery-update", json={
        "provider_id": "invalid_123",
        "status": "DELIVERED"
    })

    assert response.status_code == 404
