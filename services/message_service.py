"""
MessageService contains business logic.

It:
- Validates input
- Calls provider
- Stores message in memory
- Handles status transitions
"""
from datetime import datetime,timezone
import os
import json
from providers.reliable_message_provider import ReliableMessageProvider
from providers.fast_message_provider import FastMessageProvider
from utils.logger import get_logger
logger = get_logger(__name__)

class MessageService:


    def __init__(self):
        self.providers = self.load_providers()
        self.messages = {}  # In-memory storage (acts like database)
        self.current_id = 1

    def load_providers(self):
        """Load provider instances from config file"""
        with open("config/providers_config.json") as f:
            config = json.load(f)

        provider_instances = []
        for p_name in config.get("providers", []):
            if p_name == "ReliableMessageProvider":
                provider_instances.append(ReliableMessageProvider())
            elif p_name == "FastMessageProvider":
                provider_instances.append(FastMessageProvider())
            # future providers: add elif

        return provider_instances

    def select_provider(self):
        """Select provider dynamically: from environment variable (Jenkins) or default first provider"""
        provider_name = os.getenv("PROVIDER_NAME")  # Jenkins can pass this


        if provider_name:
            for p in self.providers:
                if p.__class__.__name__ == provider_name:
                    return p
        # fallback to first provider in config
        return self.providers[0] if self.providers else None

    def create_message(self, receiver, content):
        """
        Creates and sends a message.

        HTTP Status Codes used by API layer:
        201 -> Created successfully
        400 -> Invalid input (bad phone number / empty content)
        503 -> Provider failure
        """

        # Basic validation
        logger.info("Creating message for receiver", receiver=receiver)
        if not receiver.isdigit() or len(receiver) != 10:
            return {"error": "Invalid phone number"}, 400

        if not content:
            return {"error": "Content cannot be empty"}, 400

        """Send message via selected provider"""
        provider = self.select_provider()

        if not provider:
            return {"status": "FAILED", "error": "No provider available", "provider_id": None}
        provider_response = provider.send(receiver,content)
        logger.info("Provider response: ", provider_response = provider_response)
        # Send to provider -- old logic
        # provider_response = self.provider.send(content)

        if provider_response["status"] == "FAILED":
            # 503 Service Unavailable
            # Used when external dependency fails
            logger.error("Provider failed to send message of receiver", receiver=receiver)
            return {"error": "Provider failure"}, 503

        message_id = self.current_id
        self.current_id += 1

        # Store message
        self.messages[message_id] = {
            "id": message_id,
            "receiver": receiver,
            "content": content,
            "status": "SENT",  # Initial internal state
            "provider_id": provider_response["provider_id"],
             "created_at": datetime.now(timezone.utc),  # timezone-aware
             "updated_at": datetime.now(timezone.utc)
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
        logger.info("Updating message status for provider_id ",provider_id = provider_id)
        for msg in self.messages.values():
            if msg["provider_id"] == provider_id:

                # Prevent invalid state transitions
                if msg["status"] == "FAILED":
                    return {"error": "Cannot update failed message"}, 400

                msg["status"] = status
                # Use provided timestamp if exists, else UTC now
                msg["updated_at"] = timestamp if timestamp else datetime.now(timezone.utc)
                logger.info(f"Message status updated to {status}")
                return msg, 200

        return {"error": "Provider ID not found"}, 404