"""Tests of tests/tools.py"""

import os
import unittest

from .tools import renumber_svg_ids, canonicalize_svg, SvgTest


class RenumberTest(unittest.TestCase):
    """Test the renumber_svg_ids function."""

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


class CanonicalizeTest(unittest.TestCase):
    """Test the canonicalize_svg function."""

    def test_it(self):
        self.assertEqual(
            canonicalize_svg("<svg></svg>"),
            canonicalize_svg("<svg>\n</svg>")
        )
        self.assertEqual(
            canonicalize_svg("<svg>\n   </svg>"),
            canonicalize_svg("<svg>\n</svg>")
        )


class SvgTestTest(SvgTest):
    """Test the custom methods in SvgTest."""

    def test_success(self):
        # assert_same_svg uses renumbering, so equivalent but not identical
        # SVG will pass the assert.
        self.assert_same_svg(
            "<svg id='id10'><x id='id20' y='#id10'/></svg>",
            "<svg id='id99'><x id='id98' y='#id99'/></svg>"
        )

    def test_failure(self):
        # assert_same_svg will get write failures to files for examination.
        # The rewriting includes the new numbering, and also some newlines for
        # making the SVG more readable.
        with self.assertRaises(AssertionError):
            self.assert_same_svg(
                "<svg id='id10'><x id='id20' y='#id10'/></svg>",
                "<svg id='id99'><x id='id98' y='#id97'/></svg>"
            )

        # assert_same_svg has written two html files with the two strings.
        self.addCleanup(os.remove, "test_failure_1.html")
        self.addCleanup(os.remove, "test_failure_2.html")
        with open("test_failure_1.html") as t1:
            self.assertIn(
                "<svg id='newid0'>\n<x id='newid1' y='#newid0'/>\n</svg>",
                t1.read()
            )
        with open("test_failure_2.html") as t2:
            self.assertIn(
                "<svg id='newid0'>\n<x id='newid1' y='#newid2'/>\n</svg>",
                t2.read()
            )
