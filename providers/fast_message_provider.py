# FastProvider (made-up) simulates another Message provider
# Used for testing; no external network calls are made

from providers.base_provider import BaseProvider
import random
import uuid
from utils.logger import get_logger

logger = get_logger(__name__)

class FastMessageProvider(BaseProvider):
    def send(self, receiver, content):
        # Randomly accept or fail the message
        logger.info("Sending message", receiver=receiver, content=content)
        # provider_id is unique per message, even for the same provider.
        # It represents the provider's internal ID for this message.
        # This is used to track delivery status via webhook.
        if random.random() < 0.5:
            return {"status": "ACCEPTED", "provider_id": str(uuid.uuid4())}
        else:
            return {"status": "FAILED", "provider_id": str(uuid.uuid4())}