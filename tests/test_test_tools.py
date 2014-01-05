"""Tests of tests/tools.py"""

import unittest

from .tools import renumber_svg_ids


class RenumberTest(unittest.TestCase):

    def test_it(self):
        self.assertEqual(
            renumber_svg_ids("<svg id='id10' id='id20'>"),
            "<svg id='newid0' id='newid1'>"
        )
        self.assertEqual(
            renumber_svg_ids("<svg id='id10' also='#id10'>"),
            "<svg id='newid0' also='#newid0'>"
        )
        self.assertEqual(
            renumber_svg_ids("<svg id='id10' butnotid='id10'>"),
            "<svg id='newid0' butnotid='id10'>"
        )
