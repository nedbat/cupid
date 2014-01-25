"""Box geometry."""

from __future__ import division

from .helpers import poparg


class Box(object):
    """A Box holds the geometry of a box with a position and a size.

    Because of how it is typically used, it takes a single dictionary of
    arguments.  The dictionary of arguments has arguments popped from it, and
    others ignored::

        >>> args = {'foo': 17, 'size': (10, 50), 'left': (100, 200)}
        >>> b = Box(args)
        >>> b.center
        (105.0, 200)
        >>> b.size
        (10, 50)
        >>> args
        {'foo': 17}

    The center and size are available as individual components also::

        >>> b.cx
        105.0
        >>> b.cy
        200
        >>> b.w
        10
        >>> b.h
        50

    You can ask about the edges of the box as coordinates (top, bottom, left,
    right) or points (north, south, east, west)::

        >>> b.north
        (105.0, 175.0)
        >>> b.south
        (105.0, 225.0)
        >>> b.top
        175.0
        >>> b.bottom
        225.0

    """

    def __init__(self, args):
        other_box = poparg(args, box=None)
        if other_box is not None:
            # Copy all the attributes of the other box.
            self.__dict__.update(other_box.__dict__)
            return

        size = poparg(args, size=None)
        assert size, "Have to specify a size!"

        pos_name = pos = None
        arg_names = "left center right top topleft topright".split()
        for arg_name in arg_names:
            arg = poparg(args, **{arg_name: None})
            if arg is not None:
                assert pos is None, "Got duplicate position: %s" % pos_name
                pos_name = arg_name
                pos = arg

        # Can specify position as pos=('topright', (100,200))
        pos_arg = poparg(args, pos=None)
        if pos_arg is not None:
            assert pos is None, "Got duplicate position: pos"
            pos_name, pos = pos_arg

        if pos_name == 'left':
            center = (pos[0]+size[0]/2, pos[1])
        elif pos_name == 'right':
            center = (pos[0]-size[0]/2, pos[1])
        elif pos_name == 'center':
            center = pos
        elif pos_name == 'top':
            center = (pos[0], pos[1]+size[1]/2)
        elif pos_name == 'topleft':
            center = (pos[0]+size[0]/2, pos[1]+size[1]/2)
        elif pos_name == 'topright':
            center = (pos[0]-size[0]/2, pos[1]+size[1]/2)
        else:
            assert False, "Have to specify a position!"

        self.cx, self.cy = center
        self.w, self.h = size

        self.rise = poparg(args, rise=0)
        self.set = poparg(args, set=999999)
        self.fade = poparg(args, fade=0)

    def __repr__(self):
        return "<Box ={0.w}x{0.h} @{0.cx},{0.cy}>".format(self)

    def __eq__(self, other):
        if not isinstance(other, Box):
            return False
        return (
            self.center == other.center and
            self.size == other.size and
            self.rise == other.rise and
            self.set == other.set and
            self.fade == other.fade
        )

    def __ne__(self, other):
        return not self == other

    def translate(self, dx, dy):
        """Create a new box just like this one, but translated.

        `dx` and `dy` are deltas for the center point.  The returned box is
        the same as this one, but the center has moved::

            >>> b = Box(dict(size=(10,20), center=(100,200)))
            >>> b2 = b.translate(1, 2)
            >>> b2.center
            (101, 202)
            >>> b2.size
            (10, 20)

        The original box is unchanged::

            >>> b.center
            (100, 200)

        """
        box = Box(dict(box=self))
        box.cx += dx
        box.cy += dy
        return box

    def scale(self, sx, sy=None):
        """Make a new box that is scaled from this one."""
        sy = sy or sx
        cx = self.cx * sx
        cy = self.cy * sy
        w = self.w * sx
        h = self.h * sy
        return Box(dict(size=(w, h), center=(cx, cy)))

    def union(self, other):
        """Create a new box that covers self and other."""
        left = min(self.left, other.left)
        right = max(self.right, other.right)
        top = min(self.top, other.top)
        bottom = max(self.bottom, other.bottom)
        width = right - left
        height = bottom - top
        box = Box(dict(size=(width, height), topleft=(left, top)))
        return box

    @property
    def center(self):
        """The center point of the box."""
        return self.cx, self.cy

    @property
    def size(self):
        """The width and height as a pair."""
        return self.w, self.h

    @property
    def top(self):
        """The y-coodinate of the top edge."""
        return self.cy - self.h/2

    @property
    def bottom(self):
        """The y-coordinate of the bottom edge."""
        return self.cy + self.h/2

    @property
    def left(self):
        """The x-coordinate of the left edge."""
        return self.cx - self.w/2

    @property
    def right(self):
        """The x-coordinate of the right edge."""
        return self.cx + self.w/2

    @property
    def north(self):
        """The point at the north of the box."""
        return self.cx, self.top

    @property
    def south(self):
        """The point at the south of the box."""
        return self.cx, self.bottom

    @property
    def east(self):
        """The point at the east of the box."""
        return self.right, self.cy

    @property
    def west(self):
        """The point at the west of the box."""
        return self.left, self.cy
