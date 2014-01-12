"""Get doctests into unittest discovery."""

import doctest

import cupid.box
import cupid.helpers

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(cupid.box))
    tests.addTests(doctest.DocTestSuite(cupid.helpers))
    return tests
