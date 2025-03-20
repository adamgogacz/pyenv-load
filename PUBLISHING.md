# Publishing to PyPI

This guide outlines the steps to build, test, and publish the `pyenv-load` package to PyPI.

## Prerequisites

- Poetry installed and configured
- A PyPI account
- API token from PyPI or TestPyPI

## First-time Setup

### 1. Create an API token on PyPI

1. Log in to [PyPI](https://pypi.org/)
2. Go to your account settings
3. Create an API token
4. Save the token securely (you won't be able to see it again)

### 2. Configure Poetry with your token

```bash
poetry config pypi-token.pypi your-token
```

## Building and Publishing

### Option 1: Using the build script

The included `build.py` script automates testing, linting, and building:

```bash
python3 build.py
```

After the build completes successfully, publish with:

```bash
poetry publish
```

### Option 2: Manual Process

1. Clean previous builds:

```bash
rm -rf dist/ build/ *.egg-info/
```

2. Run tests:

```bash
poetry run pytest
```

3. Check code quality:

```bash
poetry run black --check .
poetry run isort --check-only .
poetry run mypy .
```

4. Build the package:

```bash
poetry build
```

5. Publish to PyPI:

```bash
poetry publish
```

## Testing on TestPyPI First (Recommended)

1. Configure TestPyPI in Poetry:

```bash
poetry config repositories.testpypi https://test.pypi.org/legacy/
```

2. Set your TestPyPI token:

```bash
poetry config pypi-token.testpypi your-test-token
```

3. Build the package:

```bash
poetry build
```

4. Publish to TestPyPI:

```bash
poetry publish --repository testpypi
```

5. Verify installation from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ pyenv-load
```

## Version Management

1. Update the version in `pyproject.toml`:

```toml
[tool.poetry]
version = "0.1.1"  # Increment version as needed
```

2. Also update version in `pyenv_load/__init__.py`:

```python
__version__ = "0.1.1"
```

3. Create a Git tag for the new version:

```bash
git tag v0.1.1
git push origin v0.1.1
```

## Troubleshooting

- **"File exists" error**: Make sure you're using a unique version number
- **"Invalid classifier" warning**: Ensure all classifiers in `pyproject.toml` are valid
- **Description rendering issues**: Validate your README.md is valid Markdown

## GitHub Workflow (Optional)

Consider setting up GitHub Actions for automated testing and publishing.
