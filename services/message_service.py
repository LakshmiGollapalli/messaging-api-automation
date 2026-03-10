"""
MessageService contains business logic.

It:
- Validates input
- Calls provider
- Stores message in memory
- Handles status transitions
"""

class MessageService:

    def __init__(self, provider):
        self.provider = provider
        self.messages = {}  # In-memory storage (acts like database)
        self.current_id = 1

    def create_message(self, receiver, content):
        """
        Creates and sends a message.

        HTTP Status Codes used by API layer:
        201 -> Created successfully
        400 -> Invalid input (bad phone number / empty content)
        503 -> Provider failure
        """

        # Basic validation

        if not receiver.isdigit() or len(receiver) != 10:
            return {"error": "Invalid phone number"}, 400

        if not content:
            return {"error": "Content cannot be empty"}, 400

        # Send to provider
        provider_response = self.provider.send(content)

        if provider_response["status"] == "FAILED":
            # 503 Service Unavailable
            # Used when external dependency fails
            return {"error": "Provider failure"}, 503

        message_id = self.current_id
        self.current_id += 1

        # Store message
        self.messages[message_id] = {
            "id": message_id,
            "receiver": receiver,
            "content": content,
            "status": "SENT",  # Initial internal state
            "provider_id": provider_response["provider_id"]
        }

        return self.messages[message_id], 201

    def get_message(self, message_id):
        """
        Returns message details.

        200 -> Success
        404 -> Message not found
        """
        message = self.messages.get(message_id)
        if not message:
            return {"error": "Message not found"}, 404

        return message, 200

    def update_status(self, provider_id, status, timestamp=None):
        """
        Simulates webhook update.

        200 -> Status updated
        404 -> Provider ID not found
        400 -> Invalid status transition
        """

        for msg in self.messages.values():
            if msg["provider_id"] == provider_id:

                # Prevent invalid state transitions
                if msg["status"] == "FAILED":
                    return {"error": "Cannot update failed message"}, 400

                msg["status"] = status
                msg["updated_at"] = timestamp
                return msg, 200

        return {"error": "Provider ID not found"}, 404