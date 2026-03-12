import logging

SENSITIVE_FIELDS = ["receiver", "phone", "email"]  # you can expand this list

def mask_sensitive(data):
    """
    If data is a string (like phone), mask all digits except last 4 digits.
    If data is a dict, mask sensitive keys recursively.
    """
    if isinstance(data, str):
        if len(data) >= 4:
            return f"****{data[-4:]}"
        return "****"
    elif isinstance(data, dict):
        return {k: mask_sensitive(v) if k.lower() in SENSITIVE_FIELDS else v
                for k, v in data.items()}
    return data  # leave other types untouched

class MaskedLogger:
    def __init__(self, name):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        self.logger = logging.getLogger(name)

    def info(self, msg, **kwargs):
        # mask sensitive info in kwargs
        masked = mask_sensitive(kwargs)
        self.logger.info(f"{msg} {masked}")

    def error(self, msg, **kwargs):
        masked = mask_sensitive(kwargs)
        self.logger.error(f"{msg} {masked}")

def get_logger(name):
    return MaskedLogger(name)