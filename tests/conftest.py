"""
conftest.py

This file contains shared pytest fixtures.
Fixtures help us avoid repeating setup code in every test.
"""

import pytest
import sys
import os
from app import app as flask_app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def client():
    """
    Creates a Flask test client.

    Flask test client allows us to simulate HTTP requests
    without running the actual server.

    This keeps tests fast and isolated.
    """
    flask_app.config["TESTING"] = True

    with flask_app.test_client() as client:
        yield client
