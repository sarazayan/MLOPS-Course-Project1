from setuptools import setup, find_packages
import os

# Read requirements.txt if it exists
requirements = []
if os.path.exists("requirements.txt"):
    with open("requirements.txt") as f:
        requirements = f.read().splitlines()

setup(
    name="mlops-project-1",
    version="0.1.0",
    author="sara",
    description="MLOps Project 1",
    packages=find_packages(include=['src*', 'utils*', 'config*']),
    install_requires=requirements,
    python_requires=">=3.7",
    zip_safe=False,
)