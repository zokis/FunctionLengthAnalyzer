# Function Length Analyzer

Function Length Analyzer is a Python tool that analyzes your Python project to find functions that are too long based on specified or default line limits. Functions exceeding a warning line limit are printed as warnings, and those exceeding an error line limit are printed as errors. The script walks through all Python files in a given directory, parses the AST (Abstract Syntax Tree) to identify functions, and calculates their lengths.

## Features

- Analyze single file or entire directory.
- Set custom error and warning line limits.
- Option to ignore test files.
- Supports configuration from `pyproject.toml`.
- Prints the result (warning/error) with the function name, file path, and lines count.
  
## Requirements

- Python 3.6+
  
To use the `toml` configuration, you need to install `toml`:
```bash
pip install toml
```

## Installation



## Usage

### Command Line

Run the script using the following command:

```bash
python function_length_analyzer [path...] [options]
```

#### Positional Arguments:

- `path`: Path of the Python project or file to analyze. Accepts multiple paths.

#### Options:

- `--ignore_test`: Ignore files starting with 'test_'.
- `--line_limit <int>`: Set the line limit error for functions. Default is from config or 60.
- `--warning_line_limit <int>`: Set the line limit warning for functions. Default is from config or 50.
- `--disable_output <bool>`: Enable or disable output.

### Configuration File

You can use a `pyproject.toml` file to configure the Function Length Analyzer. Here is an example configuration:

```toml
[tool.FunctionLengthAnalyzer]
error_line_limit = 80
warning_line_limit = 60
enable_output = true
ignore_directories = [".git", ".venv", "node_modules"]
ignore_files = ["conftest.py", "fixtures.py"]
```

In the absence of a `pyproject.toml` file, the script uses the following default configuration:

```python
DEFAULT_CONFIG = {
    "error_line_limit": 60,
    "warning_line_limit": 50,
    "enable_output": True,
    "ignore_directories": [".git", ".venv", "node_modules"],
    "ignore_files": ["conftest.py", "fixtures.py"],
}
```

## Example

```bash
python function_length_analyzer.py ./myproject --ignore_test --line_limit 80 --warning_line_limit 40
```

This command will analyze all Python files in `./myproject`, ignoring test files, with a warning limit of 40 lines and an error limit of 80 lines.

## Exit Status

The script exits with a status of `1` if any function exceeds the error line limit, allowing it to be used in CI/CD pipelines to enforce function length constraints.

## License

Feel free to use, modify, and distribute this script as you see fit.

## Contributing

If you have suggestions for improving the script, please create an issue or a pull request.
