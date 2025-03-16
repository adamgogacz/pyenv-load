"""Tests for loading environment variables from JSON files."""

import os
import json
import tempfile
from pathlib import Path
import sys

import pytest

from pyenv_load import load_env


@pytest.fixture
def json_file():
    """Create a temporary JSON file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        data = {
            "STRING_KEY": "string_value",
            "INT_KEY": 42,
            "FLOAT_KEY": 3.14,
            "BOOL_KEY": True,
            "NULL_KEY": None,
            "NESTED_KEY": {"nested": "value"},
            "ARRAY_KEY": [1, 2, 3],
        }
        json.dump(data, f)
        f.name_path = Path(f.name)

    yield f.name_path

    # Cleanup
    os.unlink(f.name_path)


def test_load_json_env(json_file):
    """Test loading environment variables from a JSON file."""
    # Clear environment variables that might interfere with the test
    for key in [
        "STRING_KEY",
        "INT_KEY",
        "FLOAT_KEY",
        "BOOL_KEY",
        "NULL_KEY",
        "NESTED_KEY",
        "ARRAY_KEY",
    ]:
        if key in os.environ:
            del os.environ[key]

    # Load environment variables
    result = load_env(filename=str(json_file), path=str(json_file.parent))

    # Check if loading was successful
    assert result is True

    # Check if variables were set correctly and converted to strings
    assert os.environ["STRING_KEY"] == "string_value"
    assert os.environ["INT_KEY"] == "42"
    assert os.environ["FLOAT_KEY"] == "3.14"
    assert os.environ["BOOL_KEY"] == "True"
    assert os.environ["NULL_KEY"] == "None"
    # Complex types should use json.dumps formatting
    assert os.environ["NESTED_KEY"] == '{"nested": "value"}'
    assert os.environ["ARRAY_KEY"] == "[1, 2, 3]"


def test_invalid_json_file():
    """Test loading environment variables from an invalid JSON file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("{ invalid json }")  # Invalid JSON
        f.name_path = Path(f.name)

    try:
        # Load environment variables
        result = load_env(filename=str(f.name_path), path=str(f.name_path.parent))

        # Check if loading failed
        assert result is False

    finally:
        # Cleanup
        os.unlink(f.name_path)


def test_non_dict_json():
    """Test loading environment variables from a JSON file with a non-dict root."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([1, 2, 3], f)  # Array instead of object
        f.name_path = Path(f.name)

    try:
        # Load environment variables
        result = load_env(filename=str(f.name_path), path=str(f.name_path.parent))

        # Check if loading failed
        assert result is False

    finally:
        # Cleanup
        os.unlink(f.name_path)


def test_invalid_key_in_json():
    """Test loading environment variables from a JSON file with invalid keys."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        data = {
            "VALID_KEY": "value",
            "123INVALID": "value",  # Invalid key (starts with number)
        }
        json.dump(data, f)
        f.name_path = Path(f.name)

    try:
        # Clear environment variables that might interfere with the test
        for key in ["VALID_KEY", "123INVALID"]:
            if key in os.environ:
                del os.environ[key]

        # Load environment variables
        result = load_env(filename=str(f.name_path), path=str(f.name_path.parent))

        # Check if loading was successful (should still return True even with warnings)
        assert result is True

        # Check if valid variable was set
        assert os.environ["VALID_KEY"] == "value"

        # Check if invalid variable was not set
        assert "123INVALID" not in os.environ

    finally:
        # Cleanup
        os.unlink(f.name_path)


def test_load_env_json_from_same_dir():
    """Test loading environment variables from a .env.json file in the tests directory."""

    # Clear environment variables that might interfere with the test
    for key in ["APP_NAME", "DEBUG", "PORT", "ALLOWED_HOSTS", "DATABASE"]:
        if key in os.environ:
            del os.environ[key]

    # The .env.json file is assumed to exist in the tests directory
    # Get the directory of the current test file
    current_dir = Path(__file__).parent

    # Load environment variables without specifying a path
    # This should find .env.json in the same directory as this test file
    result = load_env(filename=".env.json", path=current_dir)

    # Check if loading was successful
    assert result is True

    # Check if variables were set correctly
    assert os.environ["APP_NAME"] == "test-app"
    assert os.environ["DEBUG"] == "True"
    assert os.environ["PORT"] == "8080"
    assert os.environ["ALLOWED_HOSTS"] == '["localhost", "127.0.0.1"]'
    assert "DATABASE" in os.environ
    # Check that the nested JSON object was properly serialized
    assert '"host"' in os.environ["DATABASE"]
    assert '"port"' in os.environ["DATABASE"]
    assert '"user"' in os.environ["DATABASE"]
