from svgfig import SvgFig, Box
from helpers import defarg, poparg


class PyFig(SvgFig):
    def name(self, **args):
        class_ = add_class("name", poparg(args, class_=None))
        return self.rect(class_=class_, **args)

    def int(self, **args):
        defarg(args, size=(50,50))
        class_ = add_class("int value", poparg(args, class_=None))
        return self.circle(class_=class_, **args)

    def string(self, **args):
        class_ = add_class("string value", poparg(args, class_=None))
        return self.pill(class_=class_, **args)

    def list(self, **args):
        defarg(args, size=(40, 50))
        texts = poparg(args, texts=['x', 'y', 'z'])
        box = Box(args)
        class_ = poparg(args, class_=None)
        class_ = add_class("list", class_)
        boxes = []
        for text in texts:
            b = self.rect(box=box, class_=class_, text=text, **args)
            boxes.append(b)
            box.translate(box.w, 0)
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
        box = self.rect(class_=rclass, rx=20, ry=20, **args)
        tclass = add_class("framelabel", class_)
        if self.should_draw(box, args):
            text_box = Box({'center':(box.cx, box.top+25), 'size':(box.w, 25)})
            # PAIN: having to dig out the opacity from args.
            self.text_for_box(text, box=text_box, class_=tclass, opacity=args.get('opacity', 1))
        return box


def add_class(add, class_):
    if class_:
        class_ += " "
    else:
        class_ = ""
    return class_ + add


class PyLayout(object):
    def __init__(self, y=100, y_stride=75, name_right=200, val_gap=100):
        self.y = y
        self.y_stride = y_stride
        self.name_right = name_right
        self.val_left = self.name_right + val_gap

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
        topright = (self.name_right + 25, self.y)
        self.y += 50
        return ('topright', topright)

    def end_frame(self):
        self.y += 25
