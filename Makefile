# Makefile for cupid

.PHONY: default test clean sterile

default: test

test:
	tox

clean:
	-rm -f *.pyc */*.pyc */*/*.pyc */*/*/*.pyc */*/*/*/*.pyc */*/*/*/*/*.pyc
	-rm -rf __pycache__ */__pycache__ */*/__pycache__ */*/*/__pycache__ */*/*/*/__pycache__ */*/*/*/*/__pycache__
	-rm -f MANIFEST
	-rm -rf *.egg-info build dist
	-rm -rf htmlcov
	-rm -f .coverage .coverage.*

sterile: clean
	-rm -rf .tox
