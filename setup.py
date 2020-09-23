import os
from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="emailed-before",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"emailedbefore": ["py.typed"]},
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    setup_requires=[],
    install_requires=[
    ],
    tests_require=["mypy", "pytest", "pytest-cov", "pytest-runner"],
    version="0.1.0",
)
