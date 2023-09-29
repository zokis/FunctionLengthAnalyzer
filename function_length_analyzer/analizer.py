import ast
import os
import argparse


DEFAULT_CONFIG = {
    "error_line_limit": 60,
    "warning_line_limit": 50,
    "enable_output": True,
    "ignore_directories": [".git", ".venv", "node_modules"],
    "ignore_files": ["conftest.py", "fixtures.py"],
}


class FunctionLengthAnalyzer:
    def __init__(self, config):
        self.config = config
        self.visited_functions = set()
        self.too_long_functions = False

    def visit_functions(self, node, classname, filepath):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            key = (filepath, node.name, node.lineno, node.end_lineno)
            if key in self.visited_functions:
                return
            self.visited_functions.add(key)
            lines = node.end_lineno - node.lineno + 1
            if lines > self.config["warning_line_limit"]:
                name = f"{classname}.{node.name}" if classname else node.name
                error_or_warning = "warning"
                function_or_method = "method" if classname else "function"
                if lines >= self.config["error_line_limit"]:
                    self.too_long_functions = True
                    error_or_warning = "error"

                if self.config["enable_output"]:
                    print(
                        f"({error_or_warning}) The {function_or_method} '{name}' in file '{filepath}' has {lines} lines."
                    )

    def analyze_file(self, filepath, ignore_test):
        basename = os.path.basename(filepath)
        if ignore_test and (
            basename.startswith("test_") or basename in self.config["ignore_files"]
        ):
            return
        try:
            with open(filepath, "r") as file:
                tree = ast.parse(file.read(), filename=filepath)
        except SyntaxError as e:
            print(f"The file '{filepath}' has errors {e}.")
            return
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        self.visit_functions(child, node.name, filepath)
                continue
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.visit_functions(node, None, filepath)

    def analyze_directory(self, directory, ignore_test):
        for dirpath, dirnames, filenames in os.walk(directory):
            if any(name in dirpath for name in self.config["ignore_directories"]):
                continue
            for filename in [f for f in filenames if f.endswith(".py")]:
                self.analyze_file(os.path.join(dirpath, filename), ignore_test)


def load_config():
    try:
        import toml

        config = toml.load("pyproject.toml")["tool"]["FunctionLengthAnalyzer"]
        for key in DEFAULT_CONFIG:
            if key not in config:
                config[key] = DEFAULT_CONFIG[key]
    except Exception:
        config = DEFAULT_CONFIG
    return config


def main():
    config = load_config()

    parser = argparse.ArgumentParser(
        description="Analyze Python project or files to find large functions."
    )
    parser.add_argument(
        "path", nargs="*", help="Path of the Python project or file to analyze."
    )
    parser.add_argument(
        "--ignore_test", action="store_true", help="Ignore files starting with 'test_'."
    )
    parser.add_argument(
        "--line_limit",
        type=int,
        default=config["error_line_limit"],
        help="Line limit error for functions.",
    )
    parser.add_argument(
        "--warning_line_limit",
        type=int,
        default=config["warning_line_limit"],
        help="Line limit warning for functions.",
    )
    parser.add_argument(
        "--disable_output",
        type=bool,
        default=not config["enable_output"],
        help="Enable or disable output.",
    )
    args = parser.parse_args()
    config["enable_output"] = not args.disable_output
    analyzer = FunctionLengthAnalyzer(config)

    for path in args.path:
        if os.path.isfile(path):
            analyzer.analyze_file(path, args.ignore_test)
        elif os.path.isdir(path):
            analyzer.analyze_directory(path, args.ignore_test)

    if analyzer.too_long_functions:
        exit(1)


if __name__ == "__main__":
    main()
