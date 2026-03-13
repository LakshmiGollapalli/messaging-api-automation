# ReliableProvider (made-up) simulates a real provider
# Used for testing; no external network calls are made
import uuid
from providers.base_provider import BaseProvider
import random
from utils.logger import get_logger

logger = get_logger(__name__)


class ReliableMessageProvider(BaseProvider):

    def send(self, receiver, content):
        # Randomly accept or fail the message to simulate real provider behavior
        logger.info("Sending message", receiver=receiver)
        # provider_id is unique per message, even for the same provider.
        # It represents the provider's internal ID for this message.
        # This is used to track delivery status via webhook.
        if random.random() < 0.8:
            return {"status": "ACCEPTED", "provider_id": str(uuid.uuid4())}
        else:
            return {"status": "FAILED", "provider_id": str(uuid.uuid4())}
