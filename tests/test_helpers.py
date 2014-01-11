"""Test the code in svgfig/helpers.py."""

import unittest

from helpers import defarg, poparg


class TestHelpers(unittest.TestCase):
    def test_poparg(self):
        kwargs = {'foo': 23}
        foo = poparg(kwargs, foo=17)
        self.assertEqual(foo, 23)
        self.assertEqual(kwargs, {})

    def test_poparg_defaulted_argument(self):
        kwargs = {'foo': 23}
        bar = poparg(kwargs, bar=17)
        self.assertEqual(bar, 17)
        self.assertEqual(kwargs, {'foo': 23})

    def test_poparg_one_of_many_arguments(self):
        kwargs = {'foo': 23, 'bar': 17, 'baz': 42}
        bar = poparg(kwargs, bar=1001)
        self.assertEqual(bar, 17)
        self.assertEqual(kwargs, {'foo': 23, 'baz': 42})

    def test_defarg_already_present(self):
        kwargs = {'foo': 23}
        defarg(kwargs, foo=17)
        self.assertEqual(kwargs, {'foo': 23})

    def test_defarg_missing(self):
        kwargs = {'foo': 23}
        defarg(kwargs, bar=42)
        self.assertEqual(kwargs, {'foo': 23, 'bar':42})
