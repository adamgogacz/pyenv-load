# pyenv-load

A simple Python package to load environment variables from `.env` files or JSON files.

## Installation

You can install the package from PyPI:

```bash
pip install pyenv-load
```

Or using Poetry:

```bash
poetry add pyenv-load
```

## Usage

### Loading from a .env file

Create a `.env.local` file in your project directory:

```
DEBUG=True
API_KEY=my-secret-key
DB_HOST=localhost
DB_PORT=5432
```

Then, in your Python code:

```python
from pyenv_load import load_env

# Load from default .env.local in the current script's directory
load_env()

# Or specify a custom file and path
load_env(filename=".env.production", path="/path/to/config")

# Access the environment variables
import os
debug = os.environ.get("DEBUG")
api_key = os.environ.get("API_KEY")
```

### Loading from a JSON file

Create a `.env.json` file in your project directory:

```json
{
  "DEBUG": true,
  "API_KEY": "my-secret-key",
  "DB_HOST": "localhost",
  "DB_PORT": 5432
}
```

Then, in your Python code:

```python
from pyenv_load import load_env

# Load from a JSON file
load_env(filename=".env.json")

# Access the environment variables
import os
debug = os.environ.get("DEBUG")
api_key = os.environ.get("API_KEY")
```

## Features

- Load environment variables from `.env` files or JSON files
- Supports comments in `.env` files (first character [`#`] on a line)
- Validates environment variable names
- Handles quoted values in `.env` files
- Converts all values to strings when setting environment variables
- Properly formats complex JSON types (lists and dictionaries) using JSON serialization
- Automatic detection of file type based on file extension

### JSON Value Handling

When loading from JSON files:
- Simple values (strings, numbers, booleans, null) are converted using `str()`
- Complex values (arrays, objects) are converted using `json.dumps()`

For example, this JSON:
```json
{
  "STRING_KEY": "value",
  "NUMBER_KEY": 42,
  "ARRAY_KEY": [1, 2, 3],
  "OBJECT_KEY": {"nested": "value"}
}
```

Will produce these environment variables:
```
STRING_KEY=value
NUMBER_KEY=42
ARRAY_KEY=[1, 2, 3]
OBJECT_KEY={"nested": "value"}
```

## Environment Variable Rules

- Names must start with a letter or underscore
- Names can only contain letters, numbers, and underscores
- All values are converted to strings in the environment

## Error Handling

The `load_env` function returns:
- `True` if the file was loaded successfully
- `False` if an error occurred (with an error message printed to console)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
