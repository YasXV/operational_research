from setuptools import setup, find_packages

setup(
    name="graphe",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "networkx",
        "pytest",
    ],
    entry_points={
        "console_scripts": [
            "graphe-exemple=exemples.exemple1:main",
        ]
    },
)