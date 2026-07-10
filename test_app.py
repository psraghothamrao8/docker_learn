import os
from app import get_message

def test_get_message():
    # We temporarily set a secret to test if the code reads it
    os.environ["MY_SECRET"] = "password123"
    assert "password123" in get_message()