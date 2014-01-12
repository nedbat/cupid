"""Get doctests into unittest discovery."""

import doctest

import box
import helpers

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(box))
    tests.addTests(doctest.DocTestSuite(helpers))
    return tests