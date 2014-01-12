"""Installer for Cupid."""

from setuptools import setup

setup(
    name="Cupid",
    version="0.4",
    description="Cupid SVG figure-drawing",
    author="Ned Batchelder",
    author_email="ned@nedbatchelder.com",
    packages=["cupid"],
    install_requires=[
        "svgwrite",
    ],
)
