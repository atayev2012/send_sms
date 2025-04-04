import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from unittest import mock
import sys
from utils import Args, Config


@pytest.fixture
def mock_toml_data():
    return {
        "request": {
            "method": "POST",
            "default_response_size": "1024",
            "timeout": "30",
            "url": "http://localhost:8080/api"
        },
        "user": {
            "username": "testuser",
            "password": "testpass"
        }
    }

@pytest.mark.parametrize(
    "test_argv, expected_sender, expected_recipient, expected_message",
    [
        (["send-sms.py", "1234567890", "0987654321", "Hello"], "+1234567890", "+0987654321", "Hello"),
        (["send-sms.py", "5551234567", "6669876543", "Test Message"], "+5551234567", "+6669876543", "Test Message"),
        (["send-sms.py", "1112223333", "4445556666", "Hello", "Extra", "Words"], "+1112223333", "+4445556666", "Hello Extra Words"),
    ],
)

def test_main_with_args(test_argv, expected_sender, expected_recipient, expected_message):

    args = Args(test_argv)
    assert args.sender == expected_sender
    assert args.recipient == expected_recipient
    assert args.message == expected_message



def test_config_class(mock_toml_data):
    with mock.patch('tomllib.load', return_value=mock_toml_data):
        config = Config(config_path="config.toml")

    assert config.method == "POST"
    assert config.default_response_size == "1024"
    assert config.timeout == 30
    assert config.username == "testuser"
    assert config.password == "testpass"
    assert config.host == "localhost"
    assert config.port == 8080
    assert config.path == "/api"