from .box import Box
from .helpers import add_class, defarg, poparg
from .svgfig import SvgFig


class PyFig(SvgFig):
    def __init__(self, unit=25, y=None, y_stride=None, name_right=None, val_gap=None, **kwargs):
        super(PyFig, self).__init__(**kwargs)
        self.unit = unit
        self.y = y or 1#self.unit*4
        self.y_stride = y_stride or self.unit*3
        self.name_right = name_right or 1#self.unit*8
        self.val_left = self.name_right + (val_gap or self.unit*4)

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

    def name(self, **args):
        class_ = add_class("name", poparg(args, class_=None))
        return self.rect(class_=class_, **args)

    def auto_name(self, text, **args):
        width = self.unit * 2 + 12*len(text)
        return self.name(pos=self.next_name(), size=(width,50), text=text, **args)

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

    def reference(self, name, val, **args):
        sd_args = {}
        if self.should_draw(name, sd_args) and self.should_draw(val, sd_args):
            args.update(sd_args)
            self.connect(name.east, 0, val.west, 0, class_="arrow", **args)

    def frame(self, **args):
        text = poparg(args, text=None)
        class_ = poparg(args, class_=None)
        rclass = add_class("frame", class_)
        r = int(self.unit * .8)
        box = self.rect(class_=rclass, rx=r, ry=r, **args)
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
