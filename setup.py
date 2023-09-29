from setuptools import setup, find_packages

setup(
    name="function_length_analyzer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "toml; python_version >= '3.6'",  # toml é opcional, mas será instalado se python_version >= 3.6
    ],
    entry_points={
        "console_scripts": [
            "function_length_analyzer = function_length_analyzer.analyzer:main",
        ],
    },
)
