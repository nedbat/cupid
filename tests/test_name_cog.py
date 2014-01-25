"""SVGfig tests based on the original pynames cog figures."""

from __future__ import print_function

import textwrap

from .tools import SvgTest

# A fake cog

class FakeCog(object):
    def __init__(self):
        self._out = []

    def out(self, text):
        self._out.append(text)

    def outl(self, text):
        self._out.append(text)
        self._out.append("\n")

    def output(self):
        return "".join(self._out)

cog = FakeCog()

# Definitions from names.html

from contextlib import contextmanager
import random
import string

from cupid.pyfig import PyFig

@contextmanager
def vim_fold(label):
    cog.outl("<!-" "- " + label + " {" "{{ -" "->")
    yield
    cog.outl("<!-" "- }" "}} -" "->")

def pyfig_animation(code, figfunc, lines=None):
    num_lines = len(code.rstrip().splitlines())
    lines = lines or range(1, num_lines+1)
    with vim_fold("Animation"):
        for frame, line in enumerate([None]+list(lines)):
            div_class = "overlay"
            if frame > 0:
                div_class += " incremental"
            cog.outl('''<div class="{}">'''.format(div_class))
            #cog.outl('''<div style="height:0;margin:0;padding:0">''')
            select = ''
            if line is not None:
                select = ' select="{}"'.format(line)
            cog.outl('''<pre class="python tophalf"{}>'''.format(select))
            cog.out(code)
            cog.outl('''</pre>''')
            if frame > 0:
                cog.outl('''<div class="opaque bottomhalf" style="text-align:center">''')
                figfunc(frame)
                cog.outl('''</div>''')
            #cog.outl('''</div>''')
            cog.outl('''</div>''')


class PyNameCogTest(SvgTest):

    def setUp(self):
        cog.__init__()

    def assert_cog_output(self):
        output = textwrap.dedent(cog.output())
        self.assert_good_svg(output)

    def test_fig_names_refer_to_values(self):
        code = '''\
            x = 23
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame, y=25, name_right=200, val_gap=75)

            x = fig.auto_name("x")
            c = fig.int(pos=fig.val_for_name(x), text="23")
            fig.reference(x, c)

            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [])

        self.assert_cog_output()

    def test_many_names_can_refer_to_one_value(self):
        code = '''\
            x = 23
            y = x
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame, y=25, name_right=200, val_gap=75)

            n_x = fig.auto_name("x")
            i_23 = fig.int(pos=fig.val_for_name(n_x), text="23", set=2)
            fig.reference(n_x, i_23)
            n_y = fig.auto_name("y", rise=2)
            c_23 = (n_x.cy + n_y.cy) / 2
            i_23 = fig.int(left=(fig.val_left, c_23), text="23", rise=2)
            fig.reference(n_x, i_23)
            fig.reference(n_y, i_23)
            cog.outl(fig.tostring())

        pyfig_animation(code, figure)

        self.assert_cog_output()

    def test_names_are_reassigned_independently(self):
        code = '''\
            x = 23
            y = x
            x = 12
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame, y=25, name_right=200, val_gap=75)

            n_x = fig.auto_name("x", set=3)
            i_23 = fig.int(pos=fig.val_for_name(n_x), text="23", set=2)
            fig.reference(n_x, i_23)
            fig.next_name()  # Burn a name to space them out.
            n_y = fig.auto_name("y", rise=2)
            c_23 = (n_x.cy + n_y.cy) / 2
            i_23 = fig.int(left=(fig.val_left, c_23), text="23", rise=2)
            fig.reference(n_x, i_23)
            fig.reference(n_y, i_23)

            n_x = fig.name(center=n_x.center, size=n_x.size, text="x")
            i_12 = fig.int(pos=fig.val_for_name(n_x), text="12", rise=3)
            fig.reference(n_x, i_12)

            cog.outl(fig.tostring())

        pyfig_animation(code, figure)

        self.assert_cog_output()

    def test_values_live_until_no_references(self):
        code = '''\
            x = "hello"
            ...
            x = "world"
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame, y=25, name_right=200, val_gap=75)

            n_x = fig.auto_name("x", set=2)
            n_hidden = fig.auto_name("", set=0)
            s_hello = fig.string(pos=fig.val_for_name(n_x), size=(120,50), text=repr("hello"), set=2, fade=1)
            fig.reference(n_x, s_hello)
            n_x = fig.name(center=n_x.center, size=n_x.size, text="x", rise=2)
            s_hello = fig.string(pos=fig.val_for_name(n_hidden), size=(120, 50), text=repr("world"), rise=2)
            fig.reference(n_x, s_hello)

            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [1, 3, 3])

        self.assert_cog_output()

    def test_assignment_never_copies_data(self):
        code = '''\
            nums = [1, 2, 3]
            other = nums
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame, y=25, name_right=200, val_gap=75)

            n_nums = fig.auto_name("nums")
            l_nums = fig.list(texts="123", pos=fig.val_for_name(n_nums))
            fig.reference(n_nums, l_nums[0])

            n_other = fig.auto_name("other", rise=2)
            fig.reference(n_other, l_nums[0])

            cog.outl(fig.tostring())

        pyfig_animation(code, figure)

        self.assert_cog_output()

    def test_changes_are_visible_through_all_names(self):
        code = '''\
            nums = [1, 2, 3]
            other = nums
            nums.append(4)
            print(other)     # [1, 2, 3, 4] !!!
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame, y=25, name_right=200, val_gap=75)

            n_nums = fig.auto_name("nums")
            l_nums = fig.list(texts="123", pos=fig.val_for_name(n_nums))
            fig.reference(n_nums, l_nums[0])

            n_other = fig.auto_name("other", rise=2)
            fig.reference(n_other, l_nums[0])

            l_nums = fig.list(texts=["1", "2", "3" ,"4"], center=l_nums[0].center, rise=3)
            cog.outl(fig.tostring())

        pyfig_animation(code, figure)

        self.assert_cog_output()

    def test_immutable_values_are_safe(self):
        code = '''\
            x = "hello"
            y = x
            x = x + " there"
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame, y=25, name_right=200, val_gap=75)

            n_x = fig.auto_name("x", set=4)
            n_y = fig.auto_name("y", rise=2)
            s_hello = fig.string(pos=fig.val_for_name(n_y), size=(120,50), text=repr("hello"))
            fig.reference(n_x, s_hello)
            fig.reference(n_y, s_hello)
            s_there = fig.string(pos=fig.val_for_name(n_x), size=(200, 50), text=repr("hello there"), rise=3)
            n_x = fig.name(center=n_x.center, size=n_x.size, text="x", rise=4)
            fig.reference(n_x, s_there)
            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [1, 2, 3, 3])

        self.assert_cog_output()

    def test_references_can_be_more_than_just_names(self):
        code = '''\
            nums = [1, 2, 3]
            x = nums[1]
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame, y=25, name_right=200, val_gap=75)

            n_nums = fig.auto_name("nums")
            l_nums = fig.list(texts="123", pos=fig.val_for_name(n_nums), set=2)
            fig.reference(n_nums, l_nums[0])
            l_nums = fig.list(texts=["", "", ""], pos=fig.val_for_name(n_nums), rise=2)
            fig.reference(n_nums, l_nums[0])
            n_hidden = fig.auto_name("", set=0)
            int_y = n_hidden.cy
            ints = [fig.int(left=(fig.val_left+i*60, int_y), text=str(i+1), rise=2) for i in range(3)]
            for i in range(3):
                fig.connect(l_nums[i].center, 90, ints[i].north, 90, start_marker=fig.DOT, class_="arrow", rise=2)

            n_x = fig.auto_name("x", rise=3)
            fig.connect(n_x.east, 0, ints[1].south, -90, class_="arrow", rise=3)

            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [1, 1, 2])

        self.assert_cog_output()

    def test_function_arguments_are_assignments(self):
        code = '''\
            def func(x):
                print(x)
                return

            num = 17
            func(num)
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame, y=25, name_right=200, val_gap=75)

            n_num = fig.auto_name("num")
            i_17 = fig.int(pos=fig.val_for_name(n_num), text="17")
            fig.reference(n_num, i_17)

            fig.frame(pos=fig.next_frame(), size=(200, 125), text="func", rise=2, set=5, fade=1)
            n_x = fig.auto_name("x", rise=2, set=5, fade=1)
            fig.reference(n_x, i_17)

            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [5, 6, 1, 2, 3, 6])

        self.assert_cog_output()

    def test_augment_twice(self):
        code = '''\
            def augment_twice(a_list, val):
                a_list.append(val)
                a_list.append(val)
                return      # not really necessary

            nums = [1, 2, 3]
            augment_twice(nums, 7)
            print(nums)         # [1, 2, 3, 7, 7]
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame, y=25, name_right=200, val_gap=75)

            n_nums = fig.auto_name("nums")
            l_nums = fig.list(texts=["1", "2", "3"], pos=fig.val_for_name(n_nums))
            fig.reference(n_nums, l_nums[0])

            fig.frame(pos=fig.next_frame(), size=(200,200), text="augment_twice", rise=2, set=6, fade=1)
            n_a_list = fig.auto_name("a_list", rise=2, set=6, fade=1)
            fig.reference(n_a_list, l_nums[0])
            n_val = fig.auto_name("val", rise=2, set=6, fade=1)
            i_val = fig.int(pos=fig.val_for_name(n_val), text="7", rise=2, set=7, fade=1)
            fig.reference(n_val, i_val)

            l_nums = fig.list(texts=["1", "2", "3", "7"], center=l_nums[0].center, rise=4)
            fig.highlight(box=l_nums[-1], rise=4, set=5)
            l_nums = fig.list(texts=["1", "2", "3", "7", "7"], center=l_nums[0].center, rise=5)
            fig.highlight(box=l_nums[-1], rise=5, set=6)
            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [6,7,1,2,3,4,4,8])

        self.assert_cog_output()

    def test_augment_twice_bad(self):
        code = '''\
            def augment_twice_bad(a_list, val):
                a_list = a_list + [val, val]
                return      # not really necessary

            nums = [1, 2, 3]
            augment_twice_bad(nums, 7)
            print(nums)         # [1, 2, 3]
            '''

        def figure(frame):
            fig = PyFig(size=(550,400), frame_num=frame, y=25, name_right=230, val_gap=75)

            n_nums = fig.auto_name("nums")
            l_nums = fig.list(texts=["1", "2", "3"], pos=fig.val_for_name(n_nums))
            fig.reference(n_nums, l_nums[0])

            fig.frame(pos=fig.next_frame(), size=(230,200), text="augment_twice_bad", rise=2, set=6, fade=1)
            n_a_list = fig.auto_name("a_list", rise=2, set=5)
            fig.reference(n_a_list, l_nums[0])
            n_val = fig.auto_name("val", rise=2, set=6, fade=1)
            i_val = fig.int(pos=fig.val_for_name(n_val), text="7", rise=2, set=7, fade=1)
            fig.reference(n_val, i_val)

            n_a_list = fig.name(center=n_a_list.center, size=n_a_list.size, text="a_list", rise=5, set=6, fade=1)
            l_a_list = fig.list(texts=["1", "2", "3", "7", "7"], pos=fig.val_for_name(n_a_list), rise=4, set=7, fade=1)
            fig.reference(n_a_list, l_a_list[0])

            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [5, 6, 1, 2, 2, 3, 3, 7])

        self.assert_cog_output()

    def test_augment_twice_good(self):
        code = '''\
            def augment_twice_good(a_list, val):
                a_list = a_list + [val, val]
                return a_list

            nums = [1, 2, 3]
            nums = augment_twice_good(nums, 7)
            print(nums)         # [1, 2, 3, 7, 7]
            '''

        def figure(frame):
            fig = PyFig(size=(550,400), frame_num=frame, y=25, name_right=230, val_gap=75)

            n_nums = fig.auto_name("nums")
            l_nums = fig.list(texts=["1", "2", "3"], pos=fig.val_for_name(n_nums), set=8, fade=1)
            fig.reference(n_nums, l_nums[0])

            the_frame = fig.frame(pos=fig.next_frame(), size=(230,200), text="augment_twice_bad", rise=2, set=7, fade=1)
            n_a_list = fig.auto_name("a_list", rise=2, set=5)
            fig.reference(n_a_list, l_nums[0])
            n_val = fig.auto_name("val", rise=2, set=6, fade=1)
            i_val = fig.int(pos=fig.val_for_name(n_val), text="7", rise=2, set=6, fade=1)
            fig.reference(n_val, i_val)

            n_a_list = fig.name(center=n_a_list.center, size=n_a_list.size, text="a_list", rise=5, set=6, fade=1)
            l_a_list = fig.list(texts=["1", "2", "3", "7", "7"], pos=fig.val_for_name(n_a_list), rise=4)
            fig.reference(n_a_list, l_a_list[0])

            n_return = fig.name(center=(the_frame.right, n_a_list.cy), size=(25,25), text="", rise=6, set=8)
            fig.reference(n_return, l_a_list[0])

            n_nums = fig.name(center=n_nums.center, size=n_nums.size, text="nums", rise=8)
            fig.reference(n_nums, l_a_list[0])

            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [5, 6, 1, 2, 2, 3, 6, 6, 7])

        self.assert_cog_output()

    def test_any_name_can_refer_to_any_value_at_any_time(self):
        code = '''\
            x = 12
            x = "hello"
            x = [1, 2, 3]
            x[1] = "two"
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame, y=25, name_right=200, val_gap=75)

            x0 = fig.auto_name("", set=0)
            x = fig.auto_name("x")
            x2 = fig.auto_name("", set=0)
            x3 = fig.auto_name("", set=0)

            i_12 = fig.int(pos=fig.val_for_name(x0), text="12", set=2, fade=10)
            fig.reference(x, i_12)
            s_hello = fig.string(pos=fig.val_for_name(x), text=repr("hello"), size=(130,50), rise=2, set=3, fade=10)
            fig.reference(x, s_hello)
            l_123 = fig.list(pos=fig.val_for_name(x2), texts="123", rise=3)
            fig.reference(x, l_123[0])
            l_1s3 = fig.list(pos=fig.val_for_name(x2), texts="1 3", rise=4)
            fig.reference(x, l_1s3[0])
            s_two = fig.string(center=(l_123[1].cx, x3.cy), text=repr("two"), size=(100, 50), rise=4)
            fig.connect(l_1s3[1].center, 90, s_two.north, 90, class_="arrow", start_marker=fig.DOT, rise=4)

            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [])

        self.assert_cog_output()

    def test_names_have_no_type_values_have_no_scope(self):
        # Random figure!

        class MyRandom(object):
            """A custom implementation of a few methods from random.Random.

            For this test to succeed, the random choices must always be the same.
            But Python 3 implements these methods differently, so the same seed
            doesn't produce the same choices.  The .random() method is the same,
            so as long as we only depend on that, this code will work the same
            on both Python 2 and Python 3.  For other Python implementations,
            we'll have to use a static list of random numbers.

            """
            def __init__(self, seed):
                self.r = random.Random(seed)
            def randint(self, a, b):
                return int(a+int(self.r.random()*(b-a+1)))
            def choice(self, seq):
                return seq[int(self.r.random() * len(seq))]

        fig = PyFig(size=(400,600), scale=0.55, y=25, name_right=200, val_gap=175)

        r = MyRandom(14)   # seeded to make it pretty good.

        def rand_name():
            return "".join(r.choice(string.ascii_lowercase) for i in range(r.randint(3,7)))

        def lightly_shuffle(seq):
            """Reorder a list randomly, but don't move things too far."""
            numbered = list(enumerate(seq))
            def jitter(p):
                return p[0]+r.randint(-3,3)
            shuffled = [x for i,x in sorted(numbered, key=jitter)]
            return shuffled

        names = []
        for i in range(r.randint(2,3)):
            names.append(fig.auto_name(rand_name()))

        for f in range(3):
            num_vars = r.randint(2,3)
            fig.frame(pos=fig.next_frame(), size=(200,50+75*num_vars), text="func_"+rand_name())
            for i in range(num_vars):
                names.append(fig.auto_name(rand_name()))
            fig.end_frame()

        values = []
        for name in names:
            pos = fig.val_for_name(name)
            type = r.choice(['int']*2 + ['string']*4 + ['list']*8)
            if type == 'int':
                val = fig.int(pos=pos, text=str(r.randint(5,20)))
            elif type == 'string':
                s = rand_name()
                val = fig.string(pos=pos, text=repr(s), size=(70+10*len(s), 50))
            else:
                assert type == 'list'
                els = r.randint(4, 10)
                val = fig.list(pos=pos, texts=[str(r.randint(5,20)) for i in range(els)])
                val = val[0]
            values.append(val)

        # Mix things up
        shuffled = lightly_shuffle(names)
        for name, val in zip(shuffled, values):
            fig.reference(name, val)

        cog.outl(fig.tostring())

        self.assert_cog_output()
