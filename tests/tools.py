"""Tools for testing SVGfig."""

import collections
import functools
import glob
import itertools
import os
import re
import unittest

from cupid.pyfig import PyFig


def renumber_svg_ids(svg):
    """Renumber the ids in `svg`.

    Ids are either "id='id10'" or "#id10".  Same ids get the same renumbered
    id, to keep the meaning the same.

    Return the same string, but with new ids.

    """
    new_ids = ("newid{}".format(i) for i in itertools.count())
    id_map = collections.defaultdict(lambda: next(new_ids))

    def new_repl(match, new_id_fmt):
        r"""re.sub function for renumbering.

        The `match` object has an id in \1.  Re-number it with a new id, then
        return `new_id_fmt` with the new id in place of "{}".

        """
        found_id = match.group(1)
        return new_id_fmt.format(id_map[found_id])

    # Replace ids that look like: id="id123"
    svg = re.sub(
        r"""\bid=['"](id\d+)['"]""",
        functools.partial(new_repl, new_id_fmt="id='{}'"),
        svg
    )
    # Replace ids that look like: #id123
    svg = re.sub(
        r"""#(id\d+)\b""",
        functools.partial(new_repl, new_id_fmt="#{}"),
        svg
    )

    return svg


def canonicalize_svg(svg):
    """Remove unimportant details from SVG, for better comparison."""
    svg = renumber_svg_ids(svg)
    svg = svg.replace("><", ">\n<")
    svg = re.sub(r"^\s+<", "<", svg, flags=re.MULTILINE)
    return svg


class SvgTest(unittest.TestCase):
    """Base class for tests of SVG output."""

    maxDiff = None  # Show me error diffs, no matter how long.

    def assert_same_svg(self, svg1, svg2):
        """Assert that two SVG figures are the same.

        SVG has ids in it that might differ.  Replace them, but preserve
        identity within the SVG.

        """
        svg1 = canonicalize_svg(svg1)
        svg2 = canonicalize_svg(svg2)
        if svg1 != svg2:
            for i, svg in enumerate([svg1, svg2], start=1):
                fname = "{}_{}.html".format(self._testMethodName, i)
                with open(fname, "w") as svgout:
                    svgout.write("<!DOCTYPE html>\n<html><head><style>\n")
                    svgout.write(PyFig.CSS)
                    svgout.write("</style></head><body><div>")
                    svgout.write(svg)
                    svgout.write("</div></body></html>\n")
        else:
            # Remove any remaining previous test failures.
            for fname in glob.glob("{}_?.html".format(self._testMethodName)):
                os.remove(fname)        # pragma: no cover
        self.assertMultiLineEqual(svg1, svg2)
