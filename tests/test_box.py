"""Test Box()."""

import unittest

from box import Box


class BoxTest(unittest.TestCase):
    def test_basic(self):
        b = Box(dict(size=(10, 50), left=(100, 200)))
        # Basic properties
        self.assertEqual(b.center, (105, 200))
        self.assertEqual(b.size, (10, 50))

        # Components of center and size
        self.assertEqual(b.cx, 105)
        self.assertEqual(b.cy, 200)
        self.assertEqual(b.w, 10)
        self.assertEqual(b.h, 50)

        # Edges as points
        self.assertEqual(b.north, (105, 175))
        self.assertEqual(b.south, (105, 225))
        self.assertEqual(b.east, (110, 200))
        self.assertEqual(b.west, (100, 200))

        # Edges as coordinates
        self.assertEqual(b.top, 175)
        self.assertEqual(b.bottom, 225)
        self.assertEqual(b.left, 100)
        self.assertEqual(b.right, 110)

    def test_copying(self):
        b1 = Box(dict(size=(10, 50), left=(100, 200)))
        b2 = Box(dict(box=b1))
        self.assertEqual(b2.center, (105, 200))
        self.assertEqual(b2.size, (10, 50))
        self.assertEqual(b1, b2)

    def test_need_size(self):
        with self.assertRaisesRegexp(AssertionError, "specify a size"):
            Box(dict(left=(100, 200)))

    def test_need_position(self):
        with self.assertRaisesRegexp(AssertionError, "specify a position"):
            Box(dict(size=(10, 50)))

    def test_only_one_position(self):
        with self.assertRaisesRegexp(AssertionError, "duplicate position"):
            Box(dict(size=(10, 10), left=(100, 200), right=(300, 400)))

    def test_pos_argument(self):
        b1 = Box(dict(size=(10, 50), left=(100, 200)))
        b2 = Box(dict(size=(10, 50), pos=('left', (100, 200))))
        self.assertEqual(b1, b2)

    def test_pos_is_a_position(self):
        with self.assertRaisesRegexp(AssertionError, "duplicate position"):
            Box(dict(size=(10, 50), left=(100, 200), pos=('right', (300, 400))))

    def test_lots_of_ways_to_specify_position(self):
        b = Box(dict(size=(10, 50), left=(100, 200)))
        self.assertEqual(b, Box(dict(size=(10, 50), right=(110, 200))))
        self.assertEqual(b, Box(dict(size=(10, 50), center=(105, 200))))
        self.assertEqual(b, Box(dict(size=(10, 50), topleft=(100, 175))))
        self.assertEqual(b, Box(dict(size=(10, 50), topright=(110, 175))))
