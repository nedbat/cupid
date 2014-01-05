"""Tools for testing SVGfig."""

import functools
import itertools
import re
import unittest


def renumber_svg_ids(svg):
    """Renumber the ids in `svg`.

    Ids are either "id='id10'" or "#id10".  Same ids get the same renumbered
    id, to keep the meaning the same.

    Return the same string, but with new ids.

    """
    id_map = {}
    new_ids = ("newid{}".format(i) for i in itertools.count())

    def new_repl(match, new=None):
        r"""re.sub function for renumbering.

        Match has an id in \1.  Re-number it with a new id, then return `new`
        with the new id in place of "{}".

        """
        found_id = match.group(1)
        if found_id not in id_map:
            id_map[found_id] = next(new_ids)
        return new.format(id_map[found_id])

    # Replace ids that look like: id="id123"
    svg = re.sub(
        r"""\bid=['"](id\d+)['"]""",
        functools.partial(new_repl, new="id='{}'"),
        svg
    )
    # Replace ids that look like: #id123
    svg = re.sub(
        r"""#(id\d+)\b""",
        functools.partial(new_repl, new="#{}"),
        svg
    )

    return svg


class SvgTest(unittest.TestCase):
    """Base class for tests of SVG output."""

    maxDiff = None  # Show me error diffs, no matter how long.

    def assert_same_svg(self, svg1, svg2):
        """Assert that two SVG figures are the same.

        SVG has ids in it that might differ.  Replace them, but preserve
        identity within the SVG.

        """
        svg1 = renumber_svg_ids(svg1)
        svg1 = svg1.replace("><", ">\n<")
        svg2 = renumber_svg_ids(svg2)
        svg2 = svg2.replace("><", ">\n<")
        if svg1 != svg2:
            for i, svg in enumerate([svg1, svg2], start=1):
                fname = "{}_{}.html".format(self._testMethodName, i)
                with open(fname, "w") as svgout:
                    svgout.write("<!DOCTYPE html>\n<html><head><style>\n")
                    svgout.write(SVG_STYLE)
                    svgout.write("</style></head><body><div>")
                    svgout.write(svg)
                    svgout.write("</div></body></html>\n")
        self.assertMultiLineEqual(svg1, svg2)


SVG_STYLE = """
svg {
    stroke: black;
    fill: white;
}

svg text {
    stroke: none;
    fill: black;
}

svg .name {
    stroke: black;
    stroke-width: 2;
    fill: #ddd;
}

svg .value {
    stroke: black;
    stroke-width: 1;
    fill: white;
}

svg .list {
    stroke: black;
    stroke-width: 1;
    fill: white;
}

svg .arrow {
    fill: none;
    stroke: black;
    stroke-width: 1;
}

svg .frame {
    stroke-width: 3;
    stroke: #666;
    stroke-dasharray: 10 10;
    fill: none;
}

svg text.framelabel {
    font-size: 75%;
    font-family: monospace;
}

svg .highlight {
    stroke-width: 5;
    stroke: #f00;
    fill: none;
    opacity: 0.5;
}

svg .grid {
    stroke: #8ff; stroke-width: 1; fill: none;
}
svg .grid .half {
    stroke-dasharray: 12.5 12.5;
    stroke-dashoffset: 6.25;
    stroke-dasharray: 2 2;
    stroke-dashoffset: 1;
}
svg .grid .tiny {
    stroke-dasharray: 1 2;
    stroke: #cff;
}
svg .grid .number {
    font-size: .5em;
    stroke: none;
    fill: #0cc;
}

svg .framenum {
    font-size: .75em;
    stroke: none;
    fill: #f00;
}
"""
