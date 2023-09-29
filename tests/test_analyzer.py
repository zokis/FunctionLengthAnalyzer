import pytest
from function_length_analyzer.analizer import (
    FunctionLengthAnalyzer,
    load_config,
)


@pytest.fixture
def large_file():
    return (
        "def example_function():\n"
        "    a = 1\n"
        "    b = 2\n"
        "    c = 3\n"
        "    d = 4\n"
        "    e = 5\n"
        "    f = 6\n"
        "    g = 7\n"
        "    h = 8\n"
        "    i = 9\n"
        "    j = 10\n"
        "    k = 11\n"
        "    l = 12\n"
        "    return a + l\n"
    )


@pytest.fixture
def warning_file():
    return (
        "def example_function():\n"
        "    a = 1\n"
        "    b = 2\n"
        "    c = 3\n"
        "    d = 19\n"
        "    e = 11\n"
        "    f = 12\n"
        "    return a + f\n"
    )


@pytest.fixture
def small_file():
    return "def example_function():\n    pass\n"


@pytest.fixture
def function_length_analyzer():
    config = load_config()
    return FunctionLengthAnalyzer(config)


@pytest.fixture
def function_length_analyzer_limit_10():
    return FunctionLengthAnalyzer(
        {
            "error_line_limit": 10,
            "warning_line_limit": 5,
            "enable_output": True,
            "ignore_directories": [".git", ".venv", "node_modules"],
            "ignore_files": ["conftest.py", "fixtures.py"],
        }
    )


def test_visit_functions(function_length_analyzer, tmpdir, small_file):
    tmpfile = tmpdir.join("example.py")
    tmpfile.write_text(
        small_file,
        encoding="utf-8",
    )
    function_length_analyzer.analyze_file(str(tmpfile), False)
    assert not function_length_analyzer.too_long_functions


def test_analyze_file_with_error(
    function_length_analyzer_limit_10, tmpdir, capsys, large_file
):
    function_length_analyzer = function_length_analyzer_limit_10
    tmpfile = tmpdir.join("error_file.py")
    tmpfile.write_text(
        large_file,
        encoding="utf-8",
    )
    function_length_analyzer.analyze_file(str(tmpfile), False)
    assert function_length_analyzer.too_long_functions is True
    captured = capsys.readouterr()
    assert "(error)" in captured.out


def test_analyze_file_with_warning(
    function_length_analyzer_limit_10, tmpdir, capsys, warning_file
):
    function_length_analyzer = function_length_analyzer_limit_10
    tmpfile = tmpdir.join("error_file.py")
    tmpfile.write_text(
        warning_file,
        encoding="utf-8",
    )
    function_length_analyzer.analyze_file(str(tmpfile), False)
    assert function_length_analyzer.too_long_functions is False
    captured = capsys.readouterr()
    assert "(warning)" in captured.out


def test_analyze_file(function_length_analyzer, tmpdir, small_file):
    tmpfile = tmpdir.join("good_file.py")
    tmpfile.write_text(
        small_file,
        encoding="utf-8",
    )
    function_length_analyzer.analyze_file(str(tmpfile), False)
    assert not function_length_analyzer.too_long_functions


def test_analyze_directory(function_length_analyzer, tmpdir, small_file):
    tmpdir.mkdir("example_directory")
    tmpfile = tmpdir.join("example_directory", "example_file.py")
    tmpfile.write_text(
        small_file,
        encoding="utf-8",
    )
    function_length_analyzer.analyze_directory(str(tmpdir), False)
    assert not function_length_analyzer.too_long_functions


def test_ignore_test_files(function_length_analyzer, tmpdir, small_file):
    tmpfile = tmpdir.join("test_ignore.py")
    tmpfile.write_text(
        small_file,
        encoding="utf-8",
    )
    function_length_analyzer.analyze_file(str(tmpfile), True)
    assert not function_length_analyzer.too_long_functions


def test_ignore_files(function_length_analyzer_limit_10, tmpdir, large_file):
    function_length_analyzer = function_length_analyzer_limit_10
    tmpfile = tmpdir.join("conftest.py")
    tmpfile.write_text(large_file, encoding="utf-8")
    function_length_analyzer.analyze_file(str(tmpfile), True)
    assert function_length_analyzer.too_long_functions is False


def test_warning_limit(function_length_analyzer_limit_10, tmpdir, warning_file):
    tmpfile = tmpdir.join("warning_file.py")
    tmpfile.write_text(warning_file, encoding="utf-8")
    function_length_analyzer_limit_10.analyze_file(str(tmpfile), False)
    assert not function_length_analyzer_limit_10.too_long_functions


def test_ignore_directories(function_length_analyzer, tmpdir, large_file):
    tmpdir.mkdir("node_modules")
    tmpfile = tmpdir.join("node_modules", "test.py")
    tmpfile.write_text(large_file, encoding="utf-8")
    function_length_analyzer.analyze_directory(str(tmpdir), False)
    assert not function_length_analyzer.too_long_functions


def test_load_config(function_length_analyzer):
    config = function_length_analyzer.config
    assert isinstance(config, dict)
    assert "error_line_limit" in config
    assert "warning_line_limit" in config
