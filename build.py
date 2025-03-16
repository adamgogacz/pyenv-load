#!/usr/bin/env python3
"""Build script for pyenv-load."""

import shutil
import subprocess
from pathlib import Path


def run_command(command):
    """Run a shell command and print output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=True)
    print(f"Command completed with exit code: {result.returncode}")
    return result


def clean_build_dirs():
    """Clean build directories."""
    print("Cleaning build directories...")
    dirs_to_clean = ["dist", "build", "*.egg-info"]
    for dir_pattern in dirs_to_clean:
        for path in Path(".").glob(dir_pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"Removed: {path}")


def main():
    """Main build function."""
    # Clean previous build artifacts
    clean_build_dirs()

    # Run tests
    print("\nRunning tests...")
    run_command("poetry run pytest")

    # Run linting and type checking
    print("\nRunning code quality checks...")
    run_command("poetry run black --check src/pyenv_load")
    run_command("poetry run isort --check-only src/pyenv_load")
    run_command("poetry run mypy src/pyenv_load")

    # Build package
    print("\nBuilding package...")
    run_command("poetry build")

    # Output instructions
    print("\n" + "=" * 80)
    print("Build completed successfully!")
    print("=" * 80)
    print("\nTo publish to PyPI:")
    print("1. Make sure you have credentials configured:")
    print("   poetry config pypi-token.pypi your-token")
    print("2. Run the publish command:")
    print("   poetry publish")
    print("\nTo publish to TestPyPI first:")
    print("1. Configure TestPyPI:")
    print("   poetry config repositories.testpypi https://test.pypi.org/legacy/")
    print("2. Set your TestPyPI token:")
    print("   poetry config pypi-token.testpypi your-test-token")
    print("3. Publish to TestPyPI:")
    print("   poetry publish -r testpypi")


if __name__ == "__main__":
    main()
