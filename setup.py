"""Packaging configuration"""

from setuptools import setup, find_packages

setup(
    name="hermes-analyzer",
    version="0.1.0",
    description="Hermes AI Agent conversation analyzer - Track token usage, tool calls, and costs",
    author="stephenki",
    author_email="stephenki@users.noreply.github.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "hermes-analyzer=hermes_analyzer.cli:main",
        ],
    },
    install_requires=[
        "Jinja2>=3.1.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    keywords="hermes agent analyzer token-usage",
    url="https://github.com/stephenki/hermes-analyzer",
)
