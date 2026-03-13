import logging
import os
from datetime import datetime

SENSITIVE_FIELDS = ["receiver", "phone", "content"]


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
        return {
            k: mask_sensitive(v) if k.lower() in SENSITIVE_FIELDS else v
            for k, v in data.items()
        }

    return data


def setup_logging():
    """Configure logging once"""

    os.makedirs("logs", exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    log_file = f"logs/app_{today}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="a"),  # append mode
            logging.StreamHandler()  # also show logs in console
        ]
    )


class MaskedLogger:

    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def _format_kv(self, data):
        """Convert dict to key=value string"""
        return " ".join(f"{k}={v}" for k, v in data.items())

    def info(self, msg, **kwargs):
        masked = mask_sensitive(kwargs)
        kv_string = self._format_kv(masked)
        self.logger.info(f"{msg} {kv_string}")

    def error(self, msg, **kwargs):
        masked = mask_sensitive(kwargs)
        kv_string = self._format_kv(masked)
        self.logger.error(f"{msg} {kv_string}")


# configure logging once
setup_logging()


def get_logger(name):
    return MaskedLogger(name)
