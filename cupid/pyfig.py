from __future__ import division
from .box import Box
from .helpers import add_class, defarg, poparg
from .svgfig import SvgFig


class PyFig(SvgFig):
    def __init__(self,
            unit=25, y=None, y_stride=None, name_right=None, val_gap=None,
            name_shape='rect',
            **kwargs
            ):

        super(PyFig, self).__init__(**kwargs)
        self.unit = unit
        self.y = y or self.unit
        self.y_stride = y_stride or self.unit*3
        self.name_right = name_right or self.unit*8
        self.val_left = self.name_right + (val_gap or self.unit*3)
        self.name_shape = name_shape
        self.code_for_top = None

    def top_code(self, code):
        """Add a line of code to the top of the figure."""
        self.code_for_top = (self.y, code)
        self.y += self.unit*1.5

    def finish_figure(self):
        if self.code_for_top:
            y, code = self.code_for_top
            fig_box = self.bounding_box()
            self.text(code, center=(fig_box.cx, y), size=(fig_box.w, self.unit*2), class_="top_code")
        super(PyFig, self).finish_figure()

    def next_name(self):
        """Produce a position for the next name."""
        topright = (self.name_right, self.y)
        self.y += self.y_stride
        return ('topright', topright)

    def val_for_name(self, name):
        """Produce a position for a val alongside `name`."""
        left = (self.val_left, name.cy)
        return ('left', left)

    def next_frame(self):
        """Produce a position for the next frame."""
        topright = (self.name_right + self.unit, self.y)
        self.y += self.unit * 2
        return ('topright', topright)

    def end_frame(self):
        self.y += self.unit

    def name(self, shape=None, **args):
        class_ = add_class("name", poparg(args, class_=None))
        shape_method = getattr(self, shape or self.name_shape)
        return shape_method(class_=class_, **args)

    def auto_name(self, text, **args):
        width = int(self.unit * 2 + (self.unit * text_width(text)))
        return self.name(pos=self.next_name(), size=(width,self.unit*2), text=text, **args)

    def int(self, **args):
        defarg(args, size=(self.unit*2, self.unit*2))
        class_ = add_class("int value", poparg(args, class_=None))
        return self.circle(class_=class_, **args)

    def string(self, **args):
        class_ = add_class("string value", poparg(args, class_=None))
        return self.pill(class_=class_, **args)

    def list(self, **args):
        defarg(args, size=(int(self.unit*1.6), self.unit*2))
        texts = poparg(args, texts=['x', 'y', 'z'])
        box = Box(args)
        class_ = poparg(args, class_=None)
        class_ = add_class("list", class_)
        boxes = []
        for text in texts:
            b = self.rect(box=box, class_=class_, text=text, **args)
            boxes.append(b)
            box = box.translate(box.w, 0)
        return boxes

    def reference(self, name, val, scooch=None, **args):
        sd_args = {}
        if self.should_draw(name, sd_args) and self.should_draw(val, sd_args):
            args.update(sd_args)
            dst = val.west
            dst_angle = 0
            if scooch:
                dst = dst[0], dst[1] + scooch*self.unit
                dst_angle = scooch*-90
            self.connect(name.east, 0, dst, dst_angle, class_="arrow", **args)

    def frame(self, n_names=None, **args):
        text = poparg(args, text=None)
        class_ = poparg(args, class_=None)
        rclass = add_class("frame", class_)

        if 'pos' not in args:
            args['pos'] = self.next_frame()

        size = poparg(args, size=(200, 200))
        if n_names:
            size = (
                size[0],
                (
                    self.unit +                     # The top margin and frame label
                    (n_names * self.y_stride) +     # The names
                    self.unit                       # The bottom margin
                )
            )

        r = int(self.unit * .8)
        box = self.rect(class_=rclass, rx=r, ry=r, size=size, **args)
        tclass = add_class("framelabel", class_)
        if self.should_draw(box, args):
            text_box = Box({'center':(box.cx, box.top+self.unit), 'size':(box.w, self.unit)})
            # PAIN: having to dig out the opacity from args.
            self.text_for_box(text, box=text_box, class_=tclass, opacity=args.get('opacity', 1))
        return box

    # CSS to normalize the styling.  Use this in your pages containing figures.
    CSS = SvgFig.CSS + """
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
    """

# Crude glyph width for typical fonts.
# The string encodes the widths of characters (starting with space), in tenths
# of the point size, "0" = .1, "1" = .2, etc.
# The widths are the average of Times and Helvetica.
#          !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
WIDTHS = "22344862223522224444444444225554966665576236586757655668665222442444442442242744442324464443135"
GLYPH_WIDTHS = { chr(c): (int(w)+1)/10 for c, w in enumerate(WIDTHS, ord(' ')) }

def text_width(text):
    """Rough guess of the rendered width of the text.

    Returns:
        A float, the width of the text as a multiple of the point size.

    """
    # Really crude guess would be: return len(text)/2
    return sum(GLYPH_WIDTHS.get(c, .5) for c in text)
