"""Make figures with SVG."""

import math

import svgwrite

from .box import Box
from .helpers import poparg


class SvgFig(object):

    def __init__(self, frame_num=None, scale=None, draw_grid=False, label_frames=False, **extra):
        self.scale = scale
        self.size = extra.get('size')
        self.dwg = svgwrite.Drawing(debug=True, **extra)

        need_container = scale or not self.size

        if need_container:
            self.root = self.dwg.g()
            if scale:
                self.root.scale(scale)
            self.dwg.add(self.root)
        else:
            self.root = self.dwg

        self.frame_num = frame_num
        self.bbox = None

        # Markers we might eventually create.
        self._arrow = None
        self._dot = None

        # Draw a grid if desired.
        if draw_grid:
            self._draw_a_grid(size or (1000, 1000))

        # Indicate which animation frame this is, if desired.
        if label_frames:
            self.dwg.add(self.dwg.text(str(frame_num), insert=(2, 20), class_="framenum"))

    def _draw_a_grid(self, size):
        grid = self.dwg.g(class_="grid")
        self.dwg.add(grid)

        def lineclass(d):
            if d == 0:
                return "whole"
            elif d == 50:
                return "half"
            else:
                return "tiny"

        w, h = size
        for x in range(0, w, 100):
            grid.add(self.dwg.text(str(x), insert=(x+2, 7), class_="number"))
            for d in range(0, 100, 10):
                grid.add(self.dwg.polyline([(x+d, 0), (x+d, h)], class_=lineclass(d)))
        for y in range(0, h, 100):
            grid.add(self.dwg.text(str(y), insert=(2, y+7), class_="number"))
            for d in range(0, 100, 10):
                grid.add(self.dwg.polyline([(0, y+d), (w, y+d)], class_=lineclass(d)))

    def _add_to_bbox(self, box):
        """Accumulate `box` into the bounding box."""
        if self.bbox:
            self.bbox = self.bbox.union(box)
        else:
            self.bbox = box

    @property
    def ARROW(self):
        if self._arrow is None:
            # Define our arrow.
            self._arrow = self.dwg.marker(
                insert=(10,5), size=(10,10), orient="auto",
            )
            self._arrow.viewbox(0, 0, 10, 10)
            self._arrow.add(self.dwg.path(d="M 0,0 L 10,5 L 0,10 L 1,5 z", stroke="none", fill="black"))
            self.dwg.defs.add(self._arrow)
        return self._arrow

    @property
    def DOT(self):
        if self._dot is None:
            # Define our dot.
            self._dot = self.dwg.marker(
                insert=(2,2), size=(4,4), orient="auto",
            )
            self._dot.viewbox(0, 0, 4, 4)
            self._dot.add(self.dwg.circle(center=(2,2), r=2, fill="black"))
            self.dwg.defs.add(self._dot)
        return self._dot

    def tostring(self):
        if not self.size:
            margin = 10
            bbox = self.bbox
            #if self.scale:
            #    bbox = bbox.scale(self.scale)
            tx, ty = bbox.left, bbox.top
            self.root.translate(margin-tx, margin-ty)
            w, h = bbox.size
            self.dwg['width'] = w + margin * 2
            self.dwg['height'] = h + margin * 2
        return self.dwg.tostring()

    def should_draw(self, box, args):
        if self.frame_num is None:
            should_draw = True
        else:
            last_frame = box.set + box.fade
            should_draw = (box.rise <= self.frame_num < last_frame)
            if self.frame_num >= box.set:
                args['opacity'] = 0.25

        return should_draw

    def rect(self, **args):
        box = Box(args)
        text = poparg(args, text=None)
        if self.should_draw(box, args):
            r = self.dwg.rect(
                insert=(box.left, box.top),
                size=box.size,
                **args
            )
            self.root.add(r)

            self.text_for_box(text, box)
        self._add_to_bbox(box)
        return box

    def circle(self, **args):
        box = Box(args)
        text = poparg(args, text=None)
        if self.should_draw(box, args):
            c = self.dwg.circle(
                center=box.center,
                r=box.size[0]/2,
                **args
            )
            self.root.add(c)

            self.text_for_box(text, box)
        self._add_to_bbox(box)
        return box

    def pill(self, **args):
        size = args.get('size')
        rad = size[1]/2
        return self.rect(rx=rad, ry=rad, **args)

    def text_for_box(self, text, box, **args):
        if text and self.should_draw(box, args):
            t = self.dwg.text(text, insert=box.center, text_anchor="middle", dy=[".3em"], **args)
            self.root.add(t)

    def line(self, start, end, **extra):
        l = self.dwg.polyline([start, end], **extra)
        l['marker-end'] = self.ARROW.get_funciri()
        self.root.add(l)

    def connect(self, start, startdir, end, enddir, jump=None, start_marker=None, **args):
        # Bleh: hack to get should_draw info from args.
        args['center'] = start
        args['size'] = (0,0)
        should_draw_box = Box(args)

        if self.should_draw(should_draw_box, args):
            if jump is None:
                jump = distance(start, end) / 4
            start_jump = offset(start, startdir, jump)
            end_jump = offset(end, enddir+180, jump)
            mid = midpoint(start_jump, end_jump)
            pre_mid = toward(mid, jump, start_jump)
            post_mid = toward(mid, jump, end_jump)

            pathops = []
            pathops.append(pathop("M", start))
            pathops.append(pathop("C", start_jump, pre_mid, mid))
            pathops.append(pathop("C", post_mid, end_jump, end))

            p = self.dwg.path(" ".join(pathops), fill="none", **args)
            p['marker-end'] = self.ARROW.get_funciri()
            if start_marker:
                p['marker-start'] = start_marker.get_funciri()
            self.root.add(p)

    def highlight(self, box, **args):
        """Draw some kind of highlight around `box`."""
        args['center'] = box.center
        args['size'] = box.size
        should_draw_box = Box(args)

        if self.should_draw(should_draw_box, args):
            padding = 10
            highlight_size = (box.size[0] + padding, box.size[1] + padding)
            self.rect(center=box.center, size=highlight_size, rx=5, ry=5, class_="highlight")

    # CSS to normalize the styling.  Use this in your pages containing figures.
    CSS = """
    svg {
        stroke: black;
        fill: white;
    }

    svg text {
        stroke: none;
        fill: black;
    }

    svg .arrow {
        fill: none;
        stroke: black;
        stroke-width: 1;
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

def pathop(op, *coords):
    res = op
    for x, y in coords:
        res += " {0:d},{1:d}".format(int(x), int(y))
    return res

def offset(point, angle, dist):
    x, y = point
    angle = math.radians(angle)
    x += dist * math.cos(angle)
    y += dist * math.sin(angle)
    return x, y

def distance(start, end):
    x0, y0 = start
    x1, y1 = end
    dx = x1 - x0
    dy = y1 - y0
    start_to_end = math.sqrt(dx*dx + dy*dy)
    return start_to_end

def midpoint(start, end):
    x0, y0 = start
    x1, y1 = end
    return (x0+x1)/2, (y0+y1)/2

def toward(start, dist, end):
    x0, y0 = start
    x1, y1 = end
    dx = x1 - x0
    dy = y1 - y0
    start_to_end = math.sqrt(dx*dx + dy*dy)
    frac = float(dist) / start_to_end
    return x0 + frac*dx, y0 + frac*dy
