#!/usr/bin/env python3
"""
Setup script for ConversationThreadReconstructor.

Install:
    pip install .

Install in development mode:
    pip install -e .
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="conversationthreadreconstructor",
    version="1.0.0",
    author="FORGE (Team Brain)",
    author_email="logan@metaphy.com",
    description="Reconstruct complete conversation threads from BCH database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DonkRonk17/ConversationThreadReconstructor",
    py_modules=["conversationthreadreconstructor"],
    python_requires=">=3.8",
    install_requires=[],  # Zero dependencies!
    entry_points={
        "console_scripts": [
            "conversationthreadreconstructor=conversationthreadreconstructor:main",
            "threadrec=conversationthreadreconstructor:main",  # Short alias
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Text Processing :: General",
    ],
    keywords="conversation thread reconstruction sqlite bch team-brain",
    license="MIT",
)
