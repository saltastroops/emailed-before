from setuptools import setup, find_packages

setup(
    name="mailed-before",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    setup_requires=[],
    install_requires=[
    ],
    tests_require=["mypy", "pytest", "pytest-cov", "pytest-runner"],
    version="0.1.0",
)
