"""Tools for testing SVGfig."""

import collections
import functools
import glob
import itertools
import os
import os.path
import re
import unittest

from cupid.pyfig import PyFig


HERE = os.path.dirname(__file__)


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

    def result_file_name(self, slug, ext):
        """Make a file name for a test result.

        The name of the test is used as part of the file name, with `slug`
        added in, and an extension of `ext`, which should include the dot.

        """
        test_name = self._testMethodName
        assert test_name.startswith("test_")
        file_name = "{}_{}{}".format(test_name[5:], slug, ext)
        return os.path.join(HERE, "results", file_name)

    def assert_good_svg(self, svg):
        """Assert that an SVG result is correct.

        The name of the test is used to find a saved file of the correct
        output. `svg` is compared to it.  `svg` doesn't actually have to be
        SVG, we also use this function for HTML mixed with SVG.

        If the test fails, then `svg` is written to a file, and two .html files
        are written that show the figures, so they can be viewed in a browser
        and compared.

        """
        try:
            with open(self.result_file_name("ok", ".out")) as f:
                svg_good = canonicalize_svg(f.read())
        except IOError:                     # pragma: no cover
            # Maybe we don't have a good file to compare with.
            svg_good = "<svg></svg>"

        svg = canonicalize_svg(svg)
        if svg != svg_good:
            with open(self.result_file_name("xx", ".out"), "w") as out:
                out.write(svg)

            for kind, content in zip(["ok", "xx"], [svg_good, svg]):
                with open(self.result_file_name(kind, ".html"), "w") as out:
                    out.write("<!DOCTYPE html>\n<html><head><style>\n")
                    out.write(PyFig.CSS)
                    out.write("</style></head><body><div>")
                    out.write(content)
                    out.write("</div></body></html>\n")
        else:
            for file_parts in [("xx", ".out"), ("xx", ".html"), ("ok", ".html")]:
                fname = self.result_file_name(*file_parts)
                if os.path.exists(fname):
                    os.remove(fname)        # pragma: no cover

        self.assertMultiLineEqual(svg, svg_good)
