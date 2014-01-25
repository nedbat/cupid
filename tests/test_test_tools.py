"""Tests of tests/tools.py"""

import glob
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
        self.assert_good_svg("<svg id='id10'><x id='id20' y='#id10'/></svg>")

    def test_failure(self):
        # assert_good_svg will get write failures to files for examination.
        # The rewriting includes the new numbering, and also some newlines for
        # making the SVG more readable.

        # There should be no result files stored for this test.
        self.assertEqual(glob.glob(self.result_file_name("*", ".*")), [])

        # Write a bogus "ok" file, so the test will fail.
        ok_out_filename = self.result_file_name("ok", ".out")
        self.addCleanup(os.remove, ok_out_filename)
        with open(ok_out_filename, "w") as ok_out:
            ok_out.write(
                "<svg id='id99'><x id='id98' y='#id97'/></svg>\n"
            )

        # Now assert_good_svg will raise an AssertionError.
        with self.assertRaises(AssertionError):
            self.assert_good_svg(
                "<svg id='id10'><x id='id20' y='#id10'/></svg>",
            )

        # assert_good_svg has written an out file and two html files.
        xx_out_filename = self.result_file_name("xx", ".out")
        self.addCleanup(os.remove, xx_out_filename)
        with open(xx_out_filename) as xx_out:
            self.assertIn(
                "<svg id='newid0'>\n<x id='newid1' y='#newid0'/>\n</svg>",
                xx_out.read()
            )

        ok_html_filename = self.result_file_name("ok", ".html")
        self.addCleanup(os.remove, ok_html_filename)
        with open(ok_html_filename) as ok_html:
            self.assertIn(
                "<svg id='newid0'>\n<x id='newid1' y='#newid2'/>\n</svg>",
                ok_html.read()
            )

        xx_html_filename = self.result_file_name("xx", ".html")
        self.addCleanup(os.remove, xx_html_filename)
        with open(xx_html_filename) as xx_html:
            self.assertIn(
                "<svg id='newid0'>\n<x id='newid1' y='#newid0'/>\n</svg>",
                xx_html.read()
            )
