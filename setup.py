"""Installer for Cupid."""

from setuptools import setup

with open("README.rst") as readme:
    long_description = readme.read()

setup(
    name="Cupid",
    version="0.5",
    description="Cupid SVG figure-drawing",
    long_description=long_description,
    author="Ned Batchelder",
    author_email="ned@nedbatchelder.com",
    packages=["cupid"],
    install_requires=[
        "svgwrite",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
