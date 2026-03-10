import random
from providers.base_provider import BaseProvider


class FakeProvider(BaseProvider):
    """
    FakeProvider simulates an external SMS provider.

    We use this instead of calling real external systems.
    This makes our tests stable and deterministic.
    """

    def send(self, message):
        # Simulate provider behavior:
        # 80% chance message is accepted
        # 20% chance provider failure
        print("Inside fake provider send method")
        if random.random() < 0.8:
            return {
                "provider_id": f"fake_{random.randint(1000,9999)}",
                "status": "ACCEPTED"

            }
        else:
            return {
                "provider_id": None,
                "status": "FAILED"
            }