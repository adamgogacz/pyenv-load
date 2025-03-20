"""Tests for loading environment variables from .env files."""

import os
import tempfile
from pathlib import Path

import pytest

from pyenv_load import load_env


@pytest.fixture
def env_file():
    """Create a temporary .env file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("# This is a comment\n")
        f.write("KEY1=value1\n")
        f.write("KEY2='value2'\n")
        f.write('KEY3="value3"\n')
        f.write("KEY4=value with spaces\n")
        f.write("KEY5=value with #\n")
        f.write("  SPACED_KEY  =  spaced value  \n")
        f.write("EMPTY_KEY=\n")
        f.write("\n")  # Empty line
        f.write("# Another comment\n")
        f.write("  # Indented comment\n")
        f.write("EXPANDED_KEY=$KEY1/suffix\n")
        f.name_path = Path(f.name)

    yield f.name_path

    # Cleanup
    os.unlink(f.name_path)


def test_load_dotenv(env_file):
    """Test loading environment variables from a .env file."""
    # Clear environment variables that might interfere with the test
    for key in [
        "KEY1",
        "KEY2",
        "KEY3",
        "KEY4",
        "KEY5",
        "SPACED_KEY",
        "EMPTY_KEY",
        "EXPANDED_KEY",
    ]:
        if key in os.environ:
            del os.environ[key]

    # Load environment variables
    result = load_env(filename=str(env_file), path=str(env_file.parent))

    # Check if loading was successful
    assert result is True

    # Check if variables were set correctly
    assert os.environ["KEY1"] == "value1"
    assert os.environ["KEY2"] == "value2"
    assert os.environ["KEY3"] == "value3"
    assert os.environ["KEY4"] == "value with spaces"
    assert os.environ["KEY5"] == "value with #"
    assert os.environ["SPACED_KEY"] == "spaced value"
    assert os.environ["EMPTY_KEY"] == ""
    assert os.environ["EXPANDED_KEY"] == "value1/suffix"


def test_load_nonexistent_file():
    """Test loading environment variables from a nonexistent file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = load_env(filename="nonexistent.env", path=temp_dir)
        assert result is False


def test_invalid_env_file():
    """Test loading environment variables from an invalid .env file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("INVALID_LINE\n")  # No equals sign
        f.write("123INVALID=value\n")  # Invalid key (starts with number)
        f.name_path = Path(f.name)

    try:
        # Clear environment variables that might interfere with the test
        for key in ["INVALID_LINE", "123INVALID"]:
            if key in os.environ:
                del os.environ[key]

        # Load environment variables
        result = load_env(filename=str(f.name_path), path=str(f.name_path.parent))

        # Check if loading was successful (should still return True even with warnings)
        assert result is True

        # Check if invalid variables were not set
        assert "INVALID_LINE" not in os.environ
        assert "123INVALID" not in os.environ

    finally:
        # Cleanup
        os.unlink(f.name_path)


def test_load_env_from_same_dir():
    """Test loading environment variables from a .env.local file in the tests directory."""

    # Clear environment variables that might interfere with the test
    for key in ["APP_NAME", "DEBUG", "PORT", "ALLOWED_HOSTS", "DATABASE"]:
        if key in os.environ:
            del os.environ[key]

    # The .env.local file is assumed to exist in the tests directory
    # Get the directory of the current test file
    current_dir = Path(__file__).parent

    # Load environment variables without specifying a path
    # This should find .env.local in the same directory as this test file
    result = load_env(filename=".env.local", path=current_dir)

    # Check if loading was successful
    assert result is True

    # Check if variables were set correctly
    assert os.environ["VAR_0"] == "123.5"
    assert os.environ["VAR_1"] == "string"
    assert os.environ["VAR_2"] == r"[\"hello#world\"]"
