# BaseProvider defines the contract for any messaging provider.
# We keep it abstract so we can plug in FakeProvider for testing.

class BaseProvider:
    def send(self, receiver, content):
        """
        Sends a message to external provider.

        This method must return:
        {
            "provider_id": str,
            "status": str
        }

        status can be:
        - ACCEPTED  -> Provider received request (not yet delivered)
        - FAILED    -> Provider rejected request
        """
        raise NotImplementedError("Provider must implement send()")
