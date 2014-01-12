"""SVGfig tests based on the original pynames cog figures."""

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

from cupid.pyfig import PyFig, PyLayout

@contextmanager
def vim_fold(label):
    cog.outl("<!-" "- " + label + " {" "{{ -" "->")
    yield
    cog.outl("<!-" "- }" "}} -" "->")

def pyfig_animation(code, figfunc, lines=None):
    num_lines = len(code.rstrip().splitlines())
    lines = lines or range(1, num_lines+1)
    with vim_fold("Animation"):
        for frame, line in enumerate([None]+lines):
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

def auto_name(fig, layout, text, **args):
    width = 50 + 12*len(text)
    return fig.name(pos=layout.next_name(), size=(width,50), text=text, **args)



class PyNameCogTest(SvgTest):

    def setUp(self):
        cog.__init__()

    def assert_cog_output(self, text):
        text = textwrap.dedent(text)
        output = textwrap.dedent(cog.output())
        print "-----------------------"
        print text
        print "-----------------------"
        print output
        print "-----------------------"
        self.assert_same_svg(text, output)

    def test_fig_names_refer_to_values(self):
        code = '''\
            x = 23
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame)
            layout = PyLayout(y=25, name_right=200, val_gap=75)

            x = auto_name(fig, layout, "x")
            c = fig.int(pos=layout.val_for_name(x), text="23")
            fig.reference(x, c)

            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [])

        self.assert_cog_output("""\
            <!-- Animation {{{ -->
            <div class="overlay">
            <pre class="python tophalf">
                        x = 23
                        </pre>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="1">
                        x = 23
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id1" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="62" x="138" y="25" /><text dy=".3em" text-anchor="middle" x="169" y="50">x</text><circle class="int value" cx="300" cy="50" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="50">23</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id1)" /></svg>
            </div>
            </div>
            <!-- }}} -->
            """)

    def test_many_names_can_refer_to_one_value(self):
        code = '''\
            x = 23
            y = x
            '''

        def figure(frame):
            layout = PyLayout(y=25, name_right=200, val_gap=75)
            fig = PyFig(size=(500,400), frame_num=frame)

            n_x = auto_name(fig, layout, "x")
            i_23 = fig.int(pos=layout.val_for_name(n_x), text="23", set=2)
            fig.reference(n_x, i_23)
            n_y = auto_name(fig, layout, "y", rise=2)
            c_23 = (n_x.cy + n_y.cy) / 2
            i_23 = fig.int(left=(layout.val_left, c_23), text="23", rise=2)
            fig.reference(n_x, i_23)
            fig.reference(n_y, i_23)
            cog.outl(fig.tostring())

        pyfig_animation(code, figure)

        self.assert_cog_output("""\
            <!-- Animation {{{ -->
            <div class="overlay">
            <pre class="python tophalf">
                        x = 23
                        y = x
                        </pre>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="1">
                        x = 23
                        y = x
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id2" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="62" x="138" y="25" /><text dy=".3em" text-anchor="middle" x="169" y="50">x</text><circle class="int value" cx="300" cy="50" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="50">23</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id2)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="2">
                        x = 23
                        y = x
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id3" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="62" x="138" y="25" /><text dy=".3em" text-anchor="middle" x="169" y="50">x</text><rect class="name" height="50" width="62" x="138" y="100" /><text dy=".3em" text-anchor="middle" x="169" y="125">y</text><circle class="int value" cx="300" cy="87" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="87">23</text><path class="arrow" d="M 200,50 C 220,50 223,52 237,68 C 251,84 254,87 275,87" fill="none" marker-end="url(#id3)" /><path class="arrow" d="M 200,125 C 221,125 223,121 237,106 C 251,90 253,87 275,87" fill="none" marker-end="url(#id3)" /></svg>
            </div>
            </div>
            <!-- }}} -->
            """)

    def test_names_are_reassigned_independently(self):
        code = '''\
            x = 23
            y = x
            x = 12
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame)
            layout = PyLayout(y=25, name_right=200, val_gap=75)

            n_x = auto_name(fig, layout, "x", set=3)
            i_23 = fig.int(pos=layout.val_for_name(n_x), text="23", set=2)
            fig.reference(n_x, i_23)
            layout.next_name()  # Burn a name to space them out.
            n_y = auto_name(fig, layout, "y", rise=2)
            c_23 = (n_x.cy + n_y.cy) / 2
            i_23 = fig.int(left=(layout.val_left, c_23), text="23", rise=2)
            fig.reference(n_x, i_23)
            fig.reference(n_y, i_23)

            n_x = fig.name(center=n_x.center, size=n_x.size, text="x")
            i_12 = fig.int(pos=layout.val_for_name(n_x), text="12", rise=3)
            fig.reference(n_x, i_12)

            cog.outl(fig.tostring())

        pyfig_animation(code, figure)

        self.assert_cog_output("""\
            <!-- Animation {{{ -->
            <div class="overlay">
            <pre class="python tophalf">
                        x = 23
                        y = x
                        x = 12
                        </pre>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="1">
                        x = 23
                        y = x
                        x = 12
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id4" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="62" x="138" y="25" /><text dy=".3em" text-anchor="middle" x="169" y="50">x</text><circle class="int value" cx="300" cy="50" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="50">23</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id4)" /><rect class="name" height="50" width="62" x="138" y="25" /><text dy=".3em" text-anchor="middle" x="169" y="50">x</text></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="2">
                        x = 23
                        y = x
                        x = 12
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id5" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="62" x="138" y="25" /><text dy=".3em" text-anchor="middle" x="169" y="50">x</text><rect class="name" height="50" width="62" x="138" y="175" /><text dy=".3em" text-anchor="middle" x="169" y="200">y</text><circle class="int value" cx="300" cy="125" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="125">23</text><path class="arrow" d="M 200,50 C 226,50 230,62 237,87 C 244,112 248,125 275,125" fill="none" marker-end="url(#id5)" /><path class="arrow" d="M 200,200 C 226,200 230,187 237,162 C 244,137 248,125 275,125" fill="none" marker-end="url(#id5)" /><rect class="name" height="50" width="62" x="138" y="25" /><text dy=".3em" text-anchor="middle" x="169" y="50">x</text></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="3">
                        x = 23
                        y = x
                        x = 12
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id6" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="62" x="138" y="175" /><text dy=".3em" text-anchor="middle" x="169" y="200">y</text><circle class="int value" cx="300" cy="125" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="125">23</text><path class="arrow" d="M 200,200 C 226,200 230,187 237,162 C 244,137 248,125 275,125" fill="none" marker-end="url(#id6)" /><rect class="name" height="50" width="62" x="138" y="25" /><text dy=".3em" text-anchor="middle" x="169" y="50">x</text><circle class="int value" cx="300" cy="50" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="50">12</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id6)" /></svg>
            </div>
            </div>
            <!-- }}} -->
            """)

    def test_values_live_until_no_references(self):
        code = '''\
            x = "hello"
            ...
            x = "world"
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame)
            layout = PyLayout(y=25, name_right=200, val_gap=75)

            n_x = auto_name(fig, layout, "x", set=2)
            n_hidden = auto_name(fig, layout, "", set=0)
            s_hello = fig.string(pos=layout.val_for_name(n_x), size=(120,50), text=repr("hello"), set=2, fade=1)
            fig.reference(n_x, s_hello)
            n_x = fig.name(center=n_x.center, size=n_x.size, text="x", rise=2)
            s_hello = fig.string(pos=layout.val_for_name(n_hidden), size=(120, 50), text=repr("world"), rise=2)
            fig.reference(n_x, s_hello)

            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [1, 3, 3])

        self.assert_cog_output("""\
            <!-- Animation {{{ -->
            <div class="overlay">
            <pre class="python tophalf">
                        x = "hello"
                        ...
                        x = "world"
                        </pre>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="1">
                        x = "hello"
                        ...
                        x = "world"
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id7" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="62" x="138" y="25" /><text dy=".3em" text-anchor="middle" x="169" y="50">x</text><rect class="string value" height="50" rx="25" ry="25" width="120" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">'hello'</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id7)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="3">
                        x = "hello"
                        ...
                        x = "world"
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id8" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="string value" height="50" opacity="0.25" rx="25" ry="25" width="120" x="275" y="25" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="335" y="50">'hello'</text><rect class="name" height="50" width="62" x="138" y="25" /><text dy=".3em" text-anchor="middle" x="169" y="50">x</text><rect class="string value" height="50" rx="25" ry="25" width="120" x="275" y="100" /><text dy=".3em" text-anchor="middle" x="335" y="125">'world'</text><path class="arrow" d="M 200,50 C 226,50 230,62 237,87 C 244,112 248,125 275,125" fill="none" marker-end="url(#id8)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="3">
                        x = "hello"
                        ...
                        x = "world"
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id9" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="62" x="138" y="25" /><text dy=".3em" text-anchor="middle" x="169" y="50">x</text><rect class="string value" height="50" rx="25" ry="25" width="120" x="275" y="100" /><text dy=".3em" text-anchor="middle" x="335" y="125">'world'</text><path class="arrow" d="M 200,50 C 226,50 230,62 237,87 C 244,112 248,125 275,125" fill="none" marker-end="url(#id9)" /></svg>
            </div>
            </div>
            <!-- }}} -->
            """)

    def test_assignment_never_copies_data(self):
        code = '''\
            nums = [1, 2, 3]
            other = nums
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame)
            layout = PyLayout(y=25, name_right=200, val_gap=75)

            n_nums = auto_name(fig, layout, "nums")
            l_nums = fig.list(texts="123", pos=layout.val_for_name(n_nums))
            fig.reference(n_nums, l_nums[0])

            n_other = auto_name(fig, layout, "other", rise=2)
            fig.reference(n_other, l_nums[0])

            cog.outl(fig.tostring())

        pyfig_animation(code, figure)

        self.assert_cog_output("""\
            <!-- Animation {{{ -->
            <div class="overlay">
            <pre class="python tophalf">
                        nums = [1, 2, 3]
                        other = nums
                        </pre>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="1">
                        nums = [1, 2, 3]
                        other = nums
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id10" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id10)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="2">
                        nums = [1, 2, 3]
                        other = nums
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id11" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id11)" /><rect class="name" height="50" width="110" x="90" y="100" /><text dy=".3em" text-anchor="middle" x="145" y="125">other</text><path class="arrow" d="M 200,125 C 226,125 230,112 237,87 C 244,62 248,50 275,50" fill="none" marker-end="url(#id11)" /></svg>
            </div>
            </div>
            <!-- }}} -->
            """)

    def test_changes_are_visible_through_all_names(self):
        code = '''\
            nums = [1, 2, 3]
            other = nums
            nums.append(4)
            print other     # [1, 2, 3, 4] !!!
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame)
            layout = PyLayout(y=25, name_right=200, val_gap=75)

            n_nums = auto_name(fig, layout, "nums")
            l_nums = fig.list(texts="123", pos=layout.val_for_name(n_nums))
            fig.reference(n_nums, l_nums[0])

            n_other = auto_name(fig, layout, "other", rise=2)
            fig.reference(n_other, l_nums[0])

            l_nums = fig.list(texts=["1", "2", "3" ,"4"], center=l_nums[0].center, rise=3)
            cog.outl(fig.tostring())

        pyfig_animation(code, figure)

        self.assert_cog_output("""\
            <!-- Animation {{{ -->
            <div class="overlay">
            <pre class="python tophalf">
                        nums = [1, 2, 3]
                        other = nums
                        nums.append(4)
                        print other     # [1, 2, 3, 4] !!!
                        </pre>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="1">
                        nums = [1, 2, 3]
                        other = nums
                        nums.append(4)
                        print other     # [1, 2, 3, 4] !!!
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id12" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id12)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="2">
                        nums = [1, 2, 3]
                        other = nums
                        nums.append(4)
                        print other     # [1, 2, 3, 4] !!!
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id13" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id13)" /><rect class="name" height="50" width="110" x="90" y="100" /><text dy=".3em" text-anchor="middle" x="145" y="125">other</text><path class="arrow" d="M 200,125 C 226,125 230,112 237,87 C 244,62 248,50 275,50" fill="none" marker-end="url(#id13)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="3">
                        nums = [1, 2, 3]
                        other = nums
                        nums.append(4)
                        print other     # [1, 2, 3, 4] !!!
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id14" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id14)" /><rect class="name" height="50" width="110" x="90" y="100" /><text dy=".3em" text-anchor="middle" x="145" y="125">other</text><path class="arrow" d="M 200,125 C 226,125 230,112 237,87 C 244,62 248,50 275,50" fill="none" marker-end="url(#id14)" /><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><rect class="list" height="50" width="40" x="395" y="25" /><text dy=".3em" text-anchor="middle" x="415" y="50">4</text></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="4">
                        nums = [1, 2, 3]
                        other = nums
                        nums.append(4)
                        print other     # [1, 2, 3, 4] !!!
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id15" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id15)" /><rect class="name" height="50" width="110" x="90" y="100" /><text dy=".3em" text-anchor="middle" x="145" y="125">other</text><path class="arrow" d="M 200,125 C 226,125 230,112 237,87 C 244,62 248,50 275,50" fill="none" marker-end="url(#id15)" /><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><rect class="list" height="50" width="40" x="395" y="25" /><text dy=".3em" text-anchor="middle" x="415" y="50">4</text></svg>
            </div>
            </div>
            <!-- }}} -->
            """)

    def test_immutable_values_are_safe(self):
        code = '''\
            x = "hello"
            y = x
            x = x + " there"
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame)
            layout = PyLayout(y=25, name_right=200, val_gap=75)

            n_x = auto_name(fig, layout, "x", set=4)
            n_y = auto_name(fig, layout, "y", rise=2)
            s_hello = fig.string(pos=layout.val_for_name(n_y), size=(120,50), text=repr("hello"))
            fig.reference(n_x, s_hello)
            fig.reference(n_y, s_hello)
            s_there = fig.string(pos=layout.val_for_name(n_x), size=(200, 50), text=repr("hello there"), rise=3)
            n_x = fig.name(center=n_x.center, size=n_x.size, text="x", rise=4)
            fig.reference(n_x, s_there)
            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [1, 2, 3, 3])

        self.assert_cog_output("""\
            <!-- Animation {{{ -->
            <div class="overlay">
            <pre class="python tophalf">
                        x = "hello"
                        y = x
                        x = x + " there"
                        </pre>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="1">
                        x = "hello"
                        y = x
                        x = x + " there"
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id16" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="62" x="138" y="25" /><text dy=".3em" text-anchor="middle" x="169" y="50">x</text><rect class="string value" height="50" rx="25" ry="25" width="120" x="275" y="100" /><text dy=".3em" text-anchor="middle" x="335" y="125">'hello'</text><path class="arrow" d="M 200,50 C 226,50 230,62 237,87 C 244,112 248,125 275,125" fill="none" marker-end="url(#id16)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="2">
                        x = "hello"
                        y = x
                        x = x + " there"
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id17" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="62" x="138" y="25" /><text dy=".3em" text-anchor="middle" x="169" y="50">x</text><rect class="name" height="50" width="62" x="138" y="100" /><text dy=".3em" text-anchor="middle" x="169" y="125">y</text><rect class="string value" height="50" rx="25" ry="25" width="120" x="275" y="100" /><text dy=".3em" text-anchor="middle" x="335" y="125">'hello'</text><path class="arrow" d="M 200,50 C 226,50 230,62 237,87 C 244,112 248,125 275,125" fill="none" marker-end="url(#id17)" /><path class="arrow" d="M 200,125 C 218,125 218,125 237,125 C 256,125 256,125 275,125" fill="none" marker-end="url(#id17)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="3">
                        x = "hello"
                        y = x
                        x = x + " there"
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id18" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="62" x="138" y="25" /><text dy=".3em" text-anchor="middle" x="169" y="50">x</text><rect class="name" height="50" width="62" x="138" y="100" /><text dy=".3em" text-anchor="middle" x="169" y="125">y</text><rect class="string value" height="50" rx="25" ry="25" width="120" x="275" y="100" /><text dy=".3em" text-anchor="middle" x="335" y="125">'hello'</text><path class="arrow" d="M 200,50 C 226,50 230,62 237,87 C 244,112 248,125 275,125" fill="none" marker-end="url(#id18)" /><path class="arrow" d="M 200,125 C 218,125 218,125 237,125 C 256,125 256,125 275,125" fill="none" marker-end="url(#id18)" /><rect class="string value" height="50" rx="25" ry="25" width="200" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">'hello there'</text></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="3">
                        x = "hello"
                        y = x
                        x = x + " there"
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id19" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="62" x="138" y="100" /><text dy=".3em" text-anchor="middle" x="169" y="125">y</text><rect class="string value" height="50" rx="25" ry="25" width="120" x="275" y="100" /><text dy=".3em" text-anchor="middle" x="335" y="125">'hello'</text><path class="arrow" d="M 200,125 C 218,125 218,125 237,125 C 256,125 256,125 275,125" fill="none" marker-end="url(#id19)" /><rect class="string value" height="50" rx="25" ry="25" width="200" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">'hello there'</text><rect class="name" height="50" width="62" x="138" y="25" /><text dy=".3em" text-anchor="middle" x="169" y="50">x</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id19)" /></svg>
            </div>
            </div>
            <!-- }}} -->
            """)

    def test_references_can_be_more_than_just_names(self):
        code = '''\
            nums = [1, 2, 3]
            x = nums[1]
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame)
            layout = PyLayout(y=25, name_right=200, val_gap=75)

            n_nums = auto_name(fig, layout, "nums")
            l_nums = fig.list(texts="123", pos=layout.val_for_name(n_nums), set=2)
            fig.reference(n_nums, l_nums[0])
            l_nums = fig.list(texts=["", "", ""], pos=layout.val_for_name(n_nums), rise=2)
            fig.reference(n_nums, l_nums[0])
            n_hidden = auto_name(fig, layout, "", set=0)
            int_y = n_hidden.cy
            ints = [fig.int(left=(layout.val_left+i*60, int_y), text=str(i+1), rise=2) for i in range(3)]
            for i in range(3):
                fig.connect(l_nums[i].center, 90, ints[i].north, 90, start_marker=fig.DOT, class_="arrow", rise=2)

            n_x = auto_name(fig, layout, "x", rise=3)
            fig.connect(n_x.east, 0, ints[1].south, -90, class_="arrow", rise=3)

            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [1, 1, 2])

        self.assert_cog_output("""\
            <!-- Animation {{{ -->
            <div class="overlay">
            <pre class="python tophalf">
                        nums = [1, 2, 3]
                        x = nums[1]
                        </pre>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="1">
                        nums = [1, 2, 3]
                        x = nums[1]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id20" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker><marker id="id21" markerHeight="4" markerWidth="4" orient="auto" refX="2" refY="2" viewBox="0,0,4,4"><circle cx="2" cy="2" fill="black" r="2" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id20)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="1">
                        nums = [1, 2, 3]
                        x = nums[1]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id22" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker><marker id="id23" markerHeight="4" markerWidth="4" orient="auto" refX="2" refY="2" viewBox="0,0,4,4"><circle cx="2" cy="2" fill="black" r="2" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><rect class="list" height="50" width="40" x="315" y="25" /><rect class="list" height="50" width="40" x="355" y="25" /><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id22)" /><circle class="int value" cx="300" cy="125" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="125">1</text><circle class="int value" cx="360" cy="125" r="25" /><text dy=".3em" text-anchor="middle" x="360" y="125">2</text><circle class="int value" cx="420" cy="125" r="25" /><text dy=".3em" text-anchor="middle" x="420" y="125">3</text><path class="arrow" d="M 295,50 C 295,62 295,62 297,75 C 299,87 300,87 300,100" fill="none" marker-end="url(#id22)" marker-start="url(#id23)" /><path class="arrow" d="M 335,50 C 335,63 337,65 347,75 C 357,84 360,86 360,100" fill="none" marker-end="url(#id22)" marker-start="url(#id23)" /><path class="arrow" d="M 375,50 C 375,66 381,69 397,75 C 413,80 420,83 420,100" fill="none" marker-end="url(#id22)" marker-start="url(#id23)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="2">
                        nums = [1, 2, 3]
                        x = nums[1]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id24" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker><marker id="id25" markerHeight="4" markerWidth="4" orient="auto" refX="2" refY="2" viewBox="0,0,4,4"><circle cx="2" cy="2" fill="black" r="2" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><rect class="list" height="50" width="40" x="315" y="25" /><rect class="list" height="50" width="40" x="355" y="25" /><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id24)" /><circle class="int value" cx="300" cy="125" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="125">1</text><circle class="int value" cx="360" cy="125" r="25" /><text dy=".3em" text-anchor="middle" x="360" y="125">2</text><circle class="int value" cx="420" cy="125" r="25" /><text dy=".3em" text-anchor="middle" x="420" y="125">3</text><path class="arrow" d="M 295,50 C 295,62 295,62 297,75 C 299,87 300,87 300,100" fill="none" marker-end="url(#id24)" marker-start="url(#id25)" /><path class="arrow" d="M 335,50 C 335,63 337,65 347,75 C 357,84 360,86 360,100" fill="none" marker-end="url(#id24)" marker-start="url(#id25)" /><path class="arrow" d="M 375,50 C 375,66 381,69 397,75 C 413,80 420,83 420,100" fill="none" marker-end="url(#id24)" marker-start="url(#id25)" /><rect class="name" height="50" width="62" x="138" y="175" /><text dy=".3em" text-anchor="middle" x="169" y="200">x</text><path class="arrow" d="M 200,200 C 241,200 259,198 300,195 C 342,193 360,191 360,150" fill="none" marker-end="url(#id24)" /></svg>
            </div>
            </div>
            <!-- }}} -->
            """)

    def test_function_arguments_are_assignments(self):
        code = '''\
            def func(x):
                print x
                return

            num = 17
            func(num)
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame)
            layout = PyLayout(y=25, name_right=200, val_gap=75)

            n_num = auto_name(fig, layout, "num")
            i_17 = fig.int(pos=layout.val_for_name(n_num), text="17")
            fig.reference(n_num, i_17)

            fig.frame(pos=layout.next_frame(), size=(200, 125), text="func", rise=2, set=5, fade=1)
            n_x = auto_name(fig, layout, "x", rise=2, set=5, fade=1)
            fig.reference(n_x, i_17)

            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [5, 6, 1, 2, 3, 6])

        self.assert_cog_output("""\
            <!-- Animation {{{ -->
            <div class="overlay">
            <pre class="python tophalf">
                        def func(x):
                            print x
                            return

                        num = 17
                        func(num)
                        </pre>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="5">
                        def func(x):
                            print x
                            return

                        num = 17
                        func(num)
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id26" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="86" x="114" y="25" /><text dy=".3em" text-anchor="middle" x="157" y="50">num</text><circle class="int value" cx="300" cy="50" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="50">17</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id26)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="6">
                        def func(x):
                            print x
                            return

                        num = 17
                        func(num)
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id27" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="86" x="114" y="25" /><text dy=".3em" text-anchor="middle" x="157" y="50">num</text><circle class="int value" cx="300" cy="50" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="50">17</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id27)" /><rect class="frame" height="125" rx="20" ry="20" width="200" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="125" y="125">func</text><rect class="name" height="50" width="62" x="138" y="150" /><text dy=".3em" text-anchor="middle" x="169" y="175">x</text><path class="arrow" d="M 200,175 C 236,175 236,148 237,112 C 238,76 238,50 275,50" fill="none" marker-end="url(#id27)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="1">
                        def func(x):
                            print x
                            return

                        num = 17
                        func(num)
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id28" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="86" x="114" y="25" /><text dy=".3em" text-anchor="middle" x="157" y="50">num</text><circle class="int value" cx="300" cy="50" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="50">17</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id28)" /><rect class="frame" height="125" rx="20" ry="20" width="200" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="125" y="125">func</text><rect class="name" height="50" width="62" x="138" y="150" /><text dy=".3em" text-anchor="middle" x="169" y="175">x</text><path class="arrow" d="M 200,175 C 236,175 236,148 237,112 C 238,76 238,50 275,50" fill="none" marker-end="url(#id28)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="2">
                        def func(x):
                            print x
                            return

                        num = 17
                        func(num)
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id29" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="86" x="114" y="25" /><text dy=".3em" text-anchor="middle" x="157" y="50">num</text><circle class="int value" cx="300" cy="50" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="50">17</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id29)" /><rect class="frame" height="125" rx="20" ry="20" width="200" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="125" y="125">func</text><rect class="name" height="50" width="62" x="138" y="150" /><text dy=".3em" text-anchor="middle" x="169" y="175">x</text><path class="arrow" d="M 200,175 C 236,175 236,148 237,112 C 238,76 238,50 275,50" fill="none" marker-end="url(#id29)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="3">
                        def func(x):
                            print x
                            return

                        num = 17
                        func(num)
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id30" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="86" x="114" y="25" /><text dy=".3em" text-anchor="middle" x="157" y="50">num</text><circle class="int value" cx="300" cy="50" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="50">17</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id30)" /><rect class="frame" height="125" opacity="0.25" rx="20" ry="20" width="200" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="0.25" text-anchor="middle" x="125" y="125">func</text><rect class="name" height="50" opacity="0.25" width="62" x="138" y="150" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="169" y="175">x</text><path class="arrow" d="M 200,175 C 236,175 236,148 237,112 C 238,76 238,50 275,50" fill="none" marker-end="url(#id30)" opacity="0.25" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="6">
                        def func(x):
                            print x
                            return

                        num = 17
                        func(num)
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id31" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="86" x="114" y="25" /><text dy=".3em" text-anchor="middle" x="157" y="50">num</text><circle class="int value" cx="300" cy="50" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="50">17</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id31)" /></svg>
            </div>
            </div>
            <!-- }}} -->
            """)

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
            fig = PyFig(size=(500,400), frame_num=frame)
            layout = PyLayout(y=25, name_right=200, val_gap=75)

            n_nums = auto_name(fig, layout, "nums")
            l_nums = fig.list(texts=["1", "2", "3"], pos=layout.val_for_name(n_nums))
            fig.reference(n_nums, l_nums[0])

            fig.frame(pos=layout.next_frame(), size=(200,200), text="augment_twice", rise=2, set=6, fade=1)
            n_a_list = auto_name(fig, layout, "a_list", rise=2, set=6, fade=1)
            fig.reference(n_a_list, l_nums[0])
            n_val = auto_name(fig, layout, "val", rise=2, set=6, fade=1)
            i_val = fig.int(pos=layout.val_for_name(n_val), text="7", rise=2, set=7, fade=1)
            fig.reference(n_val, i_val)

            l_nums = fig.list(texts=["1", "2", "3", "7"], center=l_nums[0].center, rise=4)
            fig.highlight(box=l_nums[-1], rise=4, set=5)
            l_nums = fig.list(texts=["1", "2", "3", "7", "7"], center=l_nums[0].center, rise=5)
            fig.highlight(box=l_nums[-1], rise=5, set=6)
            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [6,7,1,2,3,4,4,8])

        self.assert_cog_output("""\
            <!-- Animation {{{ -->
            <div class="overlay">
            <pre class="python tophalf">
                        def augment_twice(a_list, val):
                            a_list.append(val)
                            a_list.append(val)
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="6">
                        def augment_twice(a_list, val):
                            a_list.append(val)
                            a_list.append(val)
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id32" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id32)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="7">
                        def augment_twice(a_list, val):
                            a_list.append(val)
                            a_list.append(val)
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id33" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id33)" /><rect class="frame" height="200" rx="20" ry="20" width="200" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="125" y="125">augment_twice</text><rect class="name" height="50" width="122" x="78" y="150" /><text dy=".3em" text-anchor="middle" x="139" y="175">a_list</text><path class="arrow" d="M 200,175 C 236,175 236,148 237,112 C 238,76 238,50 275,50" fill="none" marker-end="url(#id33)" /><rect class="name" height="50" width="86" x="114" y="225" /><text dy=".3em" text-anchor="middle" x="157" y="250">val</text><circle class="int value" cx="300" cy="250" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="250">7</text><path class="arrow" d="M 200,250 C 218,250 218,250 237,250 C 256,250 256,250 275,250" fill="none" marker-end="url(#id33)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="1">
                        def augment_twice(a_list, val):
                            a_list.append(val)
                            a_list.append(val)
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id34" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id34)" /><rect class="frame" height="200" rx="20" ry="20" width="200" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="125" y="125">augment_twice</text><rect class="name" height="50" width="122" x="78" y="150" /><text dy=".3em" text-anchor="middle" x="139" y="175">a_list</text><path class="arrow" d="M 200,175 C 236,175 236,148 237,112 C 238,76 238,50 275,50" fill="none" marker-end="url(#id34)" /><rect class="name" height="50" width="86" x="114" y="225" /><text dy=".3em" text-anchor="middle" x="157" y="250">val</text><circle class="int value" cx="300" cy="250" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="250">7</text><path class="arrow" d="M 200,250 C 218,250 218,250 237,250 C 256,250 256,250 275,250" fill="none" marker-end="url(#id34)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="2">
                        def augment_twice(a_list, val):
                            a_list.append(val)
                            a_list.append(val)
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id35" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id35)" /><rect class="frame" height="200" rx="20" ry="20" width="200" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="125" y="125">augment_twice</text><rect class="name" height="50" width="122" x="78" y="150" /><text dy=".3em" text-anchor="middle" x="139" y="175">a_list</text><path class="arrow" d="M 200,175 C 236,175 236,148 237,112 C 238,76 238,50 275,50" fill="none" marker-end="url(#id35)" /><rect class="name" height="50" width="86" x="114" y="225" /><text dy=".3em" text-anchor="middle" x="157" y="250">val</text><circle class="int value" cx="300" cy="250" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="250">7</text><path class="arrow" d="M 200,250 C 218,250 218,250 237,250 C 256,250 256,250 275,250" fill="none" marker-end="url(#id35)" /><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><rect class="list" height="50" width="40" x="395" y="25" /><text dy=".3em" text-anchor="middle" x="415" y="50">7</text><rect class="highlight" height="60" rx="5" ry="5" width="50" x="390" y="20" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="3">
                        def augment_twice(a_list, val):
                            a_list.append(val)
                            a_list.append(val)
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id36" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id36)" /><rect class="frame" height="200" rx="20" ry="20" width="200" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="125" y="125">augment_twice</text><rect class="name" height="50" width="122" x="78" y="150" /><text dy=".3em" text-anchor="middle" x="139" y="175">a_list</text><path class="arrow" d="M 200,175 C 236,175 236,148 237,112 C 238,76 238,50 275,50" fill="none" marker-end="url(#id36)" /><rect class="name" height="50" width="86" x="114" y="225" /><text dy=".3em" text-anchor="middle" x="157" y="250">val</text><circle class="int value" cx="300" cy="250" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="250">7</text><path class="arrow" d="M 200,250 C 218,250 218,250 237,250 C 256,250 256,250 275,250" fill="none" marker-end="url(#id36)" /><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><rect class="list" height="50" width="40" x="395" y="25" /><text dy=".3em" text-anchor="middle" x="415" y="50">7</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><rect class="list" height="50" width="40" x="395" y="25" /><text dy=".3em" text-anchor="middle" x="415" y="50">7</text><rect class="list" height="50" width="40" x="435" y="25" /><text dy=".3em" text-anchor="middle" x="455" y="50">7</text><rect class="highlight" height="60" rx="5" ry="5" width="50" x="430" y="20" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="4">
                        def augment_twice(a_list, val):
                            a_list.append(val)
                            a_list.append(val)
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id37" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id37)" /><rect class="frame" height="200" opacity="0.25" rx="20" ry="20" width="200" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="0.25" text-anchor="middle" x="125" y="125">augment_twice</text><rect class="name" height="50" opacity="0.25" width="122" x="78" y="150" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="139" y="175">a_list</text><path class="arrow" d="M 200,175 C 236,175 236,148 237,112 C 238,76 238,50 275,50" fill="none" marker-end="url(#id37)" opacity="0.25" /><rect class="name" height="50" opacity="0.25" width="86" x="114" y="225" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="157" y="250">val</text><circle class="int value" cx="300" cy="250" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="250">7</text><path class="arrow" d="M 200,250 C 218,250 218,250 237,250 C 256,250 256,250 275,250" fill="none" marker-end="url(#id37)" opacity="0.25" /><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><rect class="list" height="50" width="40" x="395" y="25" /><text dy=".3em" text-anchor="middle" x="415" y="50">7</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><rect class="list" height="50" width="40" x="395" y="25" /><text dy=".3em" text-anchor="middle" x="415" y="50">7</text><rect class="list" height="50" width="40" x="435" y="25" /><text dy=".3em" text-anchor="middle" x="455" y="50">7</text></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="4">
                        def augment_twice(a_list, val):
                            a_list.append(val)
                            a_list.append(val)
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id38" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id38)" /><circle class="int value" cx="300" cy="250" opacity="0.25" r="25" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="300" y="250">7</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><rect class="list" height="50" width="40" x="395" y="25" /><text dy=".3em" text-anchor="middle" x="415" y="50">7</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><rect class="list" height="50" width="40" x="395" y="25" /><text dy=".3em" text-anchor="middle" x="415" y="50">7</text><rect class="list" height="50" width="40" x="435" y="25" /><text dy=".3em" text-anchor="middle" x="455" y="50">7</text></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="8">
                        def augment_twice(a_list, val):
                            a_list.append(val)
                            a_list.append(val)
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id39" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="102" y="25" /><text dy=".3em" text-anchor="middle" x="151" y="50">nums</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><path class="arrow" d="M 200,50 C 218,50 218,50 237,50 C 256,50 256,50 275,50" fill="none" marker-end="url(#id39)" /><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><rect class="list" height="50" width="40" x="395" y="25" /><text dy=".3em" text-anchor="middle" x="415" y="50">7</text><rect class="list" height="50" width="40" x="275" y="25" /><text dy=".3em" text-anchor="middle" x="295" y="50">1</text><rect class="list" height="50" width="40" x="315" y="25" /><text dy=".3em" text-anchor="middle" x="335" y="50">2</text><rect class="list" height="50" width="40" x="355" y="25" /><text dy=".3em" text-anchor="middle" x="375" y="50">3</text><rect class="list" height="50" width="40" x="395" y="25" /><text dy=".3em" text-anchor="middle" x="415" y="50">7</text><rect class="list" height="50" width="40" x="435" y="25" /><text dy=".3em" text-anchor="middle" x="455" y="50">7</text></svg>
            </div>
            </div>
            <!-- }}} -->
            """)

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
            fig = PyFig(size=(550,400), frame_num=frame)
            layout = PyLayout(y=25, name_right=230, val_gap=75)

            n_nums = auto_name(fig, layout, "nums")
            l_nums = fig.list(texts=["1", "2", "3"], pos=layout.val_for_name(n_nums))
            fig.reference(n_nums, l_nums[0])

            fig.frame(pos=layout.next_frame(), size=(230,200), text="augment_twice_bad", rise=2, set=6, fade=1)
            n_a_list = auto_name(fig, layout, "a_list", rise=2, set=5)
            fig.reference(n_a_list, l_nums[0])
            n_val = auto_name(fig, layout, "val", rise=2, set=6, fade=1)
            i_val = fig.int(pos=layout.val_for_name(n_val), text="7", rise=2, set=7, fade=1)
            fig.reference(n_val, i_val)

            n_a_list = fig.name(center=n_a_list.center, size=n_a_list.size, text="a_list", rise=5, set=6, fade=1)
            l_a_list = fig.list(texts=["1", "2", "3", "7", "7"], pos=layout.val_for_name(n_a_list), rise=4, set=7, fade=1)
            fig.reference(n_a_list, l_a_list[0])

            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [5, 6, 1, 2, 2, 3, 3, 7])

        self.assert_cog_output("""\
            <!-- Animation {{{ -->
            <div class="overlay">
            <pre class="python tophalf">
                        def augment_twice_bad(a_list, val):
                            a_list = a_list + [val, val]
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice_bad(nums, 7)
                        print(nums)         # [1, 2, 3]
                        </pre>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="5">
                        def augment_twice_bad(a_list, val):
                            a_list = a_list + [val, val]
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice_bad(nums, 7)
                        print(nums)         # [1, 2, 3]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id40" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" width="40" x="305" y="25" /><text dy=".3em" text-anchor="middle" x="325" y="50">1</text><rect class="list" height="50" width="40" x="345" y="25" /><text dy=".3em" text-anchor="middle" x="365" y="50">2</text><rect class="list" height="50" width="40" x="385" y="25" /><text dy=".3em" text-anchor="middle" x="405" y="50">3</text><path class="arrow" d="M 230,50 C 248,50 248,50 267,50 C 286,50 286,50 305,50" fill="none" marker-end="url(#id40)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="6">
                        def augment_twice_bad(a_list, val):
                            a_list = a_list + [val, val]
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice_bad(nums, 7)
                        print(nums)         # [1, 2, 3]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id41" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" width="40" x="305" y="25" /><text dy=".3em" text-anchor="middle" x="325" y="50">1</text><rect class="list" height="50" width="40" x="345" y="25" /><text dy=".3em" text-anchor="middle" x="365" y="50">2</text><rect class="list" height="50" width="40" x="385" y="25" /><text dy=".3em" text-anchor="middle" x="405" y="50">3</text><path class="arrow" d="M 230,50 C 248,50 248,50 267,50 C 286,50 286,50 305,50" fill="none" marker-end="url(#id41)" /><rect class="frame" height="200" rx="20" ry="20" width="230" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="140" y="125">augment_twice_bad</text><rect class="name" height="50" width="122" x="108" y="150" /><text dy=".3em" text-anchor="middle" x="169" y="175">a_list</text><path class="arrow" d="M 230,175 C 266,175 266,148 267,112 C 268,76 268,50 305,50" fill="none" marker-end="url(#id41)" /><rect class="name" height="50" width="86" x="144" y="225" /><text dy=".3em" text-anchor="middle" x="187" y="250">val</text><circle class="int value" cx="330" cy="250" r="25" /><text dy=".3em" text-anchor="middle" x="330" y="250">7</text><path class="arrow" d="M 230,250 C 248,250 248,250 267,250 C 286,250 286,250 305,250" fill="none" marker-end="url(#id41)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="1">
                        def augment_twice_bad(a_list, val):
                            a_list = a_list + [val, val]
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice_bad(nums, 7)
                        print(nums)         # [1, 2, 3]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id42" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" width="40" x="305" y="25" /><text dy=".3em" text-anchor="middle" x="325" y="50">1</text><rect class="list" height="50" width="40" x="345" y="25" /><text dy=".3em" text-anchor="middle" x="365" y="50">2</text><rect class="list" height="50" width="40" x="385" y="25" /><text dy=".3em" text-anchor="middle" x="405" y="50">3</text><path class="arrow" d="M 230,50 C 248,50 248,50 267,50 C 286,50 286,50 305,50" fill="none" marker-end="url(#id42)" /><rect class="frame" height="200" rx="20" ry="20" width="230" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="140" y="125">augment_twice_bad</text><rect class="name" height="50" width="122" x="108" y="150" /><text dy=".3em" text-anchor="middle" x="169" y="175">a_list</text><path class="arrow" d="M 230,175 C 266,175 266,148 267,112 C 268,76 268,50 305,50" fill="none" marker-end="url(#id42)" /><rect class="name" height="50" width="86" x="144" y="225" /><text dy=".3em" text-anchor="middle" x="187" y="250">val</text><circle class="int value" cx="330" cy="250" r="25" /><text dy=".3em" text-anchor="middle" x="330" y="250">7</text><path class="arrow" d="M 230,250 C 248,250 248,250 267,250 C 286,250 286,250 305,250" fill="none" marker-end="url(#id42)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="2">
                        def augment_twice_bad(a_list, val):
                            a_list = a_list + [val, val]
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice_bad(nums, 7)
                        print(nums)         # [1, 2, 3]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id43" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" width="40" x="305" y="25" /><text dy=".3em" text-anchor="middle" x="325" y="50">1</text><rect class="list" height="50" width="40" x="345" y="25" /><text dy=".3em" text-anchor="middle" x="365" y="50">2</text><rect class="list" height="50" width="40" x="385" y="25" /><text dy=".3em" text-anchor="middle" x="405" y="50">3</text><path class="arrow" d="M 230,50 C 248,50 248,50 267,50 C 286,50 286,50 305,50" fill="none" marker-end="url(#id43)" /><rect class="frame" height="200" rx="20" ry="20" width="230" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="140" y="125">augment_twice_bad</text><rect class="name" height="50" width="122" x="108" y="150" /><text dy=".3em" text-anchor="middle" x="169" y="175">a_list</text><path class="arrow" d="M 230,175 C 266,175 266,148 267,112 C 268,76 268,50 305,50" fill="none" marker-end="url(#id43)" /><rect class="name" height="50" width="86" x="144" y="225" /><text dy=".3em" text-anchor="middle" x="187" y="250">val</text><circle class="int value" cx="330" cy="250" r="25" /><text dy=".3em" text-anchor="middle" x="330" y="250">7</text><path class="arrow" d="M 230,250 C 248,250 248,250 267,250 C 286,250 286,250 305,250" fill="none" marker-end="url(#id43)" /><rect class="list" height="50" width="40" x="305" y="150" /><text dy=".3em" text-anchor="middle" x="325" y="175">1</text><rect class="list" height="50" width="40" x="345" y="150" /><text dy=".3em" text-anchor="middle" x="365" y="175">2</text><rect class="list" height="50" width="40" x="385" y="150" /><text dy=".3em" text-anchor="middle" x="405" y="175">3</text><rect class="list" height="50" width="40" x="425" y="150" /><text dy=".3em" text-anchor="middle" x="445" y="175">7</text><rect class="list" height="50" width="40" x="465" y="150" /><text dy=".3em" text-anchor="middle" x="485" y="175">7</text></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="2">
                        def augment_twice_bad(a_list, val):
                            a_list = a_list + [val, val]
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice_bad(nums, 7)
                        print(nums)         # [1, 2, 3]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id44" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" width="40" x="305" y="25" /><text dy=".3em" text-anchor="middle" x="325" y="50">1</text><rect class="list" height="50" width="40" x="345" y="25" /><text dy=".3em" text-anchor="middle" x="365" y="50">2</text><rect class="list" height="50" width="40" x="385" y="25" /><text dy=".3em" text-anchor="middle" x="405" y="50">3</text><path class="arrow" d="M 230,50 C 248,50 248,50 267,50 C 286,50 286,50 305,50" fill="none" marker-end="url(#id44)" /><rect class="frame" height="200" rx="20" ry="20" width="230" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="140" y="125">augment_twice_bad</text><rect class="name" height="50" width="86" x="144" y="225" /><text dy=".3em" text-anchor="middle" x="187" y="250">val</text><circle class="int value" cx="330" cy="250" r="25" /><text dy=".3em" text-anchor="middle" x="330" y="250">7</text><path class="arrow" d="M 230,250 C 248,250 248,250 267,250 C 286,250 286,250 305,250" fill="none" marker-end="url(#id44)" /><rect class="name" height="50" width="122" x="108" y="150" /><text dy=".3em" text-anchor="middle" x="169" y="175">a_list</text><rect class="list" height="50" width="40" x="305" y="150" /><text dy=".3em" text-anchor="middle" x="325" y="175">1</text><rect class="list" height="50" width="40" x="345" y="150" /><text dy=".3em" text-anchor="middle" x="365" y="175">2</text><rect class="list" height="50" width="40" x="385" y="150" /><text dy=".3em" text-anchor="middle" x="405" y="175">3</text><rect class="list" height="50" width="40" x="425" y="150" /><text dy=".3em" text-anchor="middle" x="445" y="175">7</text><rect class="list" height="50" width="40" x="465" y="150" /><text dy=".3em" text-anchor="middle" x="485" y="175">7</text><path class="arrow" d="M 230,175 C 248,175 248,175 267,175 C 286,175 286,175 305,175" fill="none" marker-end="url(#id44)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="3">
                        def augment_twice_bad(a_list, val):
                            a_list = a_list + [val, val]
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice_bad(nums, 7)
                        print(nums)         # [1, 2, 3]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id45" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" width="40" x="305" y="25" /><text dy=".3em" text-anchor="middle" x="325" y="50">1</text><rect class="list" height="50" width="40" x="345" y="25" /><text dy=".3em" text-anchor="middle" x="365" y="50">2</text><rect class="list" height="50" width="40" x="385" y="25" /><text dy=".3em" text-anchor="middle" x="405" y="50">3</text><path class="arrow" d="M 230,50 C 248,50 248,50 267,50 C 286,50 286,50 305,50" fill="none" marker-end="url(#id45)" /><rect class="frame" height="200" opacity="0.25" rx="20" ry="20" width="230" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="0.25" text-anchor="middle" x="140" y="125">augment_twice_bad</text><rect class="name" height="50" opacity="0.25" width="86" x="144" y="225" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="187" y="250">val</text><circle class="int value" cx="330" cy="250" r="25" /><text dy=".3em" text-anchor="middle" x="330" y="250">7</text><path class="arrow" d="M 230,250 C 248,250 248,250 267,250 C 286,250 286,250 305,250" fill="none" marker-end="url(#id45)" opacity="0.25" /><rect class="name" height="50" opacity="0.25" width="122" x="108" y="150" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="169" y="175">a_list</text><rect class="list" height="50" width="40" x="305" y="150" /><text dy=".3em" text-anchor="middle" x="325" y="175">1</text><rect class="list" height="50" width="40" x="345" y="150" /><text dy=".3em" text-anchor="middle" x="365" y="175">2</text><rect class="list" height="50" width="40" x="385" y="150" /><text dy=".3em" text-anchor="middle" x="405" y="175">3</text><rect class="list" height="50" width="40" x="425" y="150" /><text dy=".3em" text-anchor="middle" x="445" y="175">7</text><rect class="list" height="50" width="40" x="465" y="150" /><text dy=".3em" text-anchor="middle" x="485" y="175">7</text><path class="arrow" d="M 230,175 C 248,175 248,175 267,175 C 286,175 286,175 305,175" fill="none" marker-end="url(#id45)" opacity="0.25" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="3">
                        def augment_twice_bad(a_list, val):
                            a_list = a_list + [val, val]
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice_bad(nums, 7)
                        print(nums)         # [1, 2, 3]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id46" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" width="40" x="305" y="25" /><text dy=".3em" text-anchor="middle" x="325" y="50">1</text><rect class="list" height="50" width="40" x="345" y="25" /><text dy=".3em" text-anchor="middle" x="365" y="50">2</text><rect class="list" height="50" width="40" x="385" y="25" /><text dy=".3em" text-anchor="middle" x="405" y="50">3</text><path class="arrow" d="M 230,50 C 248,50 248,50 267,50 C 286,50 286,50 305,50" fill="none" marker-end="url(#id46)" /><circle class="int value" cx="330" cy="250" opacity="0.25" r="25" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="330" y="250">7</text><rect class="list" height="50" opacity="0.25" width="40" x="305" y="150" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="325" y="175">1</text><rect class="list" height="50" opacity="0.25" width="40" x="345" y="150" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="365" y="175">2</text><rect class="list" height="50" opacity="0.25" width="40" x="385" y="150" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="405" y="175">3</text><rect class="list" height="50" opacity="0.25" width="40" x="425" y="150" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="445" y="175">7</text><rect class="list" height="50" opacity="0.25" width="40" x="465" y="150" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="485" y="175">7</text></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="7">
                        def augment_twice_bad(a_list, val):
                            a_list = a_list + [val, val]
                            return      # not really necessary

                        nums = [1, 2, 3]
                        augment_twice_bad(nums, 7)
                        print(nums)         # [1, 2, 3]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id47" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" width="40" x="305" y="25" /><text dy=".3em" text-anchor="middle" x="325" y="50">1</text><rect class="list" height="50" width="40" x="345" y="25" /><text dy=".3em" text-anchor="middle" x="365" y="50">2</text><rect class="list" height="50" width="40" x="385" y="25" /><text dy=".3em" text-anchor="middle" x="405" y="50">3</text><path class="arrow" d="M 230,50 C 248,50 248,50 267,50 C 286,50 286,50 305,50" fill="none" marker-end="url(#id47)" /></svg>
            </div>
            </div>
            <!-- }}} -->
            """)

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
            fig = PyFig(size=(550,400), frame_num=frame)
            layout = PyLayout(y=25, name_right=230, val_gap=75)

            n_nums = auto_name(fig, layout, "nums")
            l_nums = fig.list(texts=["1", "2", "3"], pos=layout.val_for_name(n_nums), set=8, fade=1)
            fig.reference(n_nums, l_nums[0])

            the_frame = fig.frame(pos=layout.next_frame(), size=(230,200), text="augment_twice_bad", rise=2, set=7, fade=1)
            n_a_list = auto_name(fig, layout, "a_list", rise=2, set=5)
            fig.reference(n_a_list, l_nums[0])
            n_val = auto_name(fig, layout, "val", rise=2, set=6, fade=1)
            i_val = fig.int(pos=layout.val_for_name(n_val), text="7", rise=2, set=6, fade=1)
            fig.reference(n_val, i_val)

            n_a_list = fig.name(center=n_a_list.center, size=n_a_list.size, text="a_list", rise=5, set=6, fade=1)
            l_a_list = fig.list(texts=["1", "2", "3", "7", "7"], pos=layout.val_for_name(n_a_list), rise=4)
            fig.reference(n_a_list, l_a_list[0])

            n_return = fig.name(center=(the_frame.right, n_a_list.cy), size=(25,25), text="", rise=6, set=8)
            fig.reference(n_return, l_a_list[0])

            n_nums = fig.name(center=n_nums.center, size=n_nums.size, text="nums", rise=8)
            fig.reference(n_nums, l_a_list[0])

            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [5, 6, 1, 2, 2, 3, 6, 6, 7])

        self.assert_cog_output("""\
            <!-- Animation {{{ -->
            <div class="overlay">
            <pre class="python tophalf">
                        def augment_twice_good(a_list, val):
                            a_list = a_list + [val, val]
                            return a_list

                        nums = [1, 2, 3]
                        nums = augment_twice_good(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="5">
                        def augment_twice_good(a_list, val):
                            a_list = a_list + [val, val]
                            return a_list

                        nums = [1, 2, 3]
                        nums = augment_twice_good(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id48" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" width="40" x="305" y="25" /><text dy=".3em" text-anchor="middle" x="325" y="50">1</text><rect class="list" height="50" width="40" x="345" y="25" /><text dy=".3em" text-anchor="middle" x="365" y="50">2</text><rect class="list" height="50" width="40" x="385" y="25" /><text dy=".3em" text-anchor="middle" x="405" y="50">3</text><path class="arrow" d="M 230,50 C 248,50 248,50 267,50 C 286,50 286,50 305,50" fill="none" marker-end="url(#id48)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="6">
                        def augment_twice_good(a_list, val):
                            a_list = a_list + [val, val]
                            return a_list

                        nums = [1, 2, 3]
                        nums = augment_twice_good(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id49" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" width="40" x="305" y="25" /><text dy=".3em" text-anchor="middle" x="325" y="50">1</text><rect class="list" height="50" width="40" x="345" y="25" /><text dy=".3em" text-anchor="middle" x="365" y="50">2</text><rect class="list" height="50" width="40" x="385" y="25" /><text dy=".3em" text-anchor="middle" x="405" y="50">3</text><path class="arrow" d="M 230,50 C 248,50 248,50 267,50 C 286,50 286,50 305,50" fill="none" marker-end="url(#id49)" /><rect class="frame" height="200" rx="20" ry="20" width="230" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="140" y="125">augment_twice_bad</text><rect class="name" height="50" width="122" x="108" y="150" /><text dy=".3em" text-anchor="middle" x="169" y="175">a_list</text><path class="arrow" d="M 230,175 C 266,175 266,148 267,112 C 268,76 268,50 305,50" fill="none" marker-end="url(#id49)" /><rect class="name" height="50" width="86" x="144" y="225" /><text dy=".3em" text-anchor="middle" x="187" y="250">val</text><circle class="int value" cx="330" cy="250" r="25" /><text dy=".3em" text-anchor="middle" x="330" y="250">7</text><path class="arrow" d="M 230,250 C 248,250 248,250 267,250 C 286,250 286,250 305,250" fill="none" marker-end="url(#id49)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="1">
                        def augment_twice_good(a_list, val):
                            a_list = a_list + [val, val]
                            return a_list

                        nums = [1, 2, 3]
                        nums = augment_twice_good(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id50" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" width="40" x="305" y="25" /><text dy=".3em" text-anchor="middle" x="325" y="50">1</text><rect class="list" height="50" width="40" x="345" y="25" /><text dy=".3em" text-anchor="middle" x="365" y="50">2</text><rect class="list" height="50" width="40" x="385" y="25" /><text dy=".3em" text-anchor="middle" x="405" y="50">3</text><path class="arrow" d="M 230,50 C 248,50 248,50 267,50 C 286,50 286,50 305,50" fill="none" marker-end="url(#id50)" /><rect class="frame" height="200" rx="20" ry="20" width="230" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="140" y="125">augment_twice_bad</text><rect class="name" height="50" width="122" x="108" y="150" /><text dy=".3em" text-anchor="middle" x="169" y="175">a_list</text><path class="arrow" d="M 230,175 C 266,175 266,148 267,112 C 268,76 268,50 305,50" fill="none" marker-end="url(#id50)" /><rect class="name" height="50" width="86" x="144" y="225" /><text dy=".3em" text-anchor="middle" x="187" y="250">val</text><circle class="int value" cx="330" cy="250" r="25" /><text dy=".3em" text-anchor="middle" x="330" y="250">7</text><path class="arrow" d="M 230,250 C 248,250 248,250 267,250 C 286,250 286,250 305,250" fill="none" marker-end="url(#id50)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="2">
                        def augment_twice_good(a_list, val):
                            a_list = a_list + [val, val]
                            return a_list

                        nums = [1, 2, 3]
                        nums = augment_twice_good(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id51" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" width="40" x="305" y="25" /><text dy=".3em" text-anchor="middle" x="325" y="50">1</text><rect class="list" height="50" width="40" x="345" y="25" /><text dy=".3em" text-anchor="middle" x="365" y="50">2</text><rect class="list" height="50" width="40" x="385" y="25" /><text dy=".3em" text-anchor="middle" x="405" y="50">3</text><path class="arrow" d="M 230,50 C 248,50 248,50 267,50 C 286,50 286,50 305,50" fill="none" marker-end="url(#id51)" /><rect class="frame" height="200" rx="20" ry="20" width="230" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="140" y="125">augment_twice_bad</text><rect class="name" height="50" width="122" x="108" y="150" /><text dy=".3em" text-anchor="middle" x="169" y="175">a_list</text><path class="arrow" d="M 230,175 C 266,175 266,148 267,112 C 268,76 268,50 305,50" fill="none" marker-end="url(#id51)" /><rect class="name" height="50" width="86" x="144" y="225" /><text dy=".3em" text-anchor="middle" x="187" y="250">val</text><circle class="int value" cx="330" cy="250" r="25" /><text dy=".3em" text-anchor="middle" x="330" y="250">7</text><path class="arrow" d="M 230,250 C 248,250 248,250 267,250 C 286,250 286,250 305,250" fill="none" marker-end="url(#id51)" /><rect class="list" height="50" width="40" x="305" y="150" /><text dy=".3em" text-anchor="middle" x="325" y="175">1</text><rect class="list" height="50" width="40" x="345" y="150" /><text dy=".3em" text-anchor="middle" x="365" y="175">2</text><rect class="list" height="50" width="40" x="385" y="150" /><text dy=".3em" text-anchor="middle" x="405" y="175">3</text><rect class="list" height="50" width="40" x="425" y="150" /><text dy=".3em" text-anchor="middle" x="445" y="175">7</text><rect class="list" height="50" width="40" x="465" y="150" /><text dy=".3em" text-anchor="middle" x="485" y="175">7</text></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="2">
                        def augment_twice_good(a_list, val):
                            a_list = a_list + [val, val]
                            return a_list

                        nums = [1, 2, 3]
                        nums = augment_twice_good(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id52" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" width="40" x="305" y="25" /><text dy=".3em" text-anchor="middle" x="325" y="50">1</text><rect class="list" height="50" width="40" x="345" y="25" /><text dy=".3em" text-anchor="middle" x="365" y="50">2</text><rect class="list" height="50" width="40" x="385" y="25" /><text dy=".3em" text-anchor="middle" x="405" y="50">3</text><path class="arrow" d="M 230,50 C 248,50 248,50 267,50 C 286,50 286,50 305,50" fill="none" marker-end="url(#id52)" /><rect class="frame" height="200" rx="20" ry="20" width="230" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="140" y="125">augment_twice_bad</text><rect class="name" height="50" width="86" x="144" y="225" /><text dy=".3em" text-anchor="middle" x="187" y="250">val</text><circle class="int value" cx="330" cy="250" r="25" /><text dy=".3em" text-anchor="middle" x="330" y="250">7</text><path class="arrow" d="M 230,250 C 248,250 248,250 267,250 C 286,250 286,250 305,250" fill="none" marker-end="url(#id52)" /><rect class="name" height="50" width="122" x="108" y="150" /><text dy=".3em" text-anchor="middle" x="169" y="175">a_list</text><rect class="list" height="50" width="40" x="305" y="150" /><text dy=".3em" text-anchor="middle" x="325" y="175">1</text><rect class="list" height="50" width="40" x="345" y="150" /><text dy=".3em" text-anchor="middle" x="365" y="175">2</text><rect class="list" height="50" width="40" x="385" y="150" /><text dy=".3em" text-anchor="middle" x="405" y="175">3</text><rect class="list" height="50" width="40" x="425" y="150" /><text dy=".3em" text-anchor="middle" x="445" y="175">7</text><rect class="list" height="50" width="40" x="465" y="150" /><text dy=".3em" text-anchor="middle" x="485" y="175">7</text><path class="arrow" d="M 230,175 C 248,175 248,175 267,175 C 286,175 286,175 305,175" fill="none" marker-end="url(#id52)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="3">
                        def augment_twice_good(a_list, val):
                            a_list = a_list + [val, val]
                            return a_list

                        nums = [1, 2, 3]
                        nums = augment_twice_good(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id53" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" width="40" x="305" y="25" /><text dy=".3em" text-anchor="middle" x="325" y="50">1</text><rect class="list" height="50" width="40" x="345" y="25" /><text dy=".3em" text-anchor="middle" x="365" y="50">2</text><rect class="list" height="50" width="40" x="385" y="25" /><text dy=".3em" text-anchor="middle" x="405" y="50">3</text><path class="arrow" d="M 230,50 C 248,50 248,50 267,50 C 286,50 286,50 305,50" fill="none" marker-end="url(#id53)" /><rect class="frame" height="200" rx="20" ry="20" width="230" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="140" y="125">augment_twice_bad</text><rect class="name" height="50" opacity="0.25" width="86" x="144" y="225" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="187" y="250">val</text><circle class="int value" cx="330" cy="250" opacity="0.25" r="25" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="330" y="250">7</text><path class="arrow" d="M 230,250 C 248,250 248,250 267,250 C 286,250 286,250 305,250" fill="none" marker-end="url(#id53)" opacity="0.25" /><rect class="name" height="50" opacity="0.25" width="122" x="108" y="150" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="169" y="175">a_list</text><rect class="list" height="50" width="40" x="305" y="150" /><text dy=".3em" text-anchor="middle" x="325" y="175">1</text><rect class="list" height="50" width="40" x="345" y="150" /><text dy=".3em" text-anchor="middle" x="365" y="175">2</text><rect class="list" height="50" width="40" x="385" y="150" /><text dy=".3em" text-anchor="middle" x="405" y="175">3</text><rect class="list" height="50" width="40" x="425" y="150" /><text dy=".3em" text-anchor="middle" x="445" y="175">7</text><rect class="list" height="50" width="40" x="465" y="150" /><text dy=".3em" text-anchor="middle" x="485" y="175">7</text><path class="arrow" d="M 230,175 C 248,175 248,175 267,175 C 286,175 286,175 305,175" fill="none" marker-end="url(#id53)" opacity="0.25" /><rect class="name" height="25" width="25" x="243" y="163" /><path class="arrow" d="M 267,175 C 276,175 276,175 286,175 C 295,175 295,175 305,175" fill="none" marker-end="url(#id53)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="6">
                        def augment_twice_good(a_list, val):
                            a_list = a_list + [val, val]
                            return a_list

                        nums = [1, 2, 3]
                        nums = augment_twice_good(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id54" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" width="40" x="305" y="25" /><text dy=".3em" text-anchor="middle" x="325" y="50">1</text><rect class="list" height="50" width="40" x="345" y="25" /><text dy=".3em" text-anchor="middle" x="365" y="50">2</text><rect class="list" height="50" width="40" x="385" y="25" /><text dy=".3em" text-anchor="middle" x="405" y="50">3</text><path class="arrow" d="M 230,50 C 248,50 248,50 267,50 C 286,50 286,50 305,50" fill="none" marker-end="url(#id54)" /><rect class="frame" height="200" opacity="0.25" rx="20" ry="20" width="230" x="25" y="100" /><text class="framelabel" dy=".3em" opacity="0.25" text-anchor="middle" x="140" y="125">augment_twice_bad</text><rect class="list" height="50" width="40" x="305" y="150" /><text dy=".3em" text-anchor="middle" x="325" y="175">1</text><rect class="list" height="50" width="40" x="345" y="150" /><text dy=".3em" text-anchor="middle" x="365" y="175">2</text><rect class="list" height="50" width="40" x="385" y="150" /><text dy=".3em" text-anchor="middle" x="405" y="175">3</text><rect class="list" height="50" width="40" x="425" y="150" /><text dy=".3em" text-anchor="middle" x="445" y="175">7</text><rect class="list" height="50" width="40" x="465" y="150" /><text dy=".3em" text-anchor="middle" x="485" y="175">7</text><rect class="name" height="25" width="25" x="243" y="163" /><path class="arrow" d="M 267,175 C 276,175 276,175 286,175 C 295,175 295,175 305,175" fill="none" marker-end="url(#id54)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="6">
                        def augment_twice_good(a_list, val):
                            a_list = a_list + [val, val]
                            return a_list

                        nums = [1, 2, 3]
                        nums = augment_twice_good(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id55" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" opacity="0.25" width="40" x="305" y="25" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="325" y="50">1</text><rect class="list" height="50" opacity="0.25" width="40" x="345" y="25" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="365" y="50">2</text><rect class="list" height="50" opacity="0.25" width="40" x="385" y="25" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="405" y="50">3</text><path class="arrow" d="M 230,50 C 248,50 248,50 267,50 C 286,50 286,50 305,50" fill="none" marker-end="url(#id55)" opacity="0.25" /><rect class="list" height="50" width="40" x="305" y="150" /><text dy=".3em" text-anchor="middle" x="325" y="175">1</text><rect class="list" height="50" width="40" x="345" y="150" /><text dy=".3em" text-anchor="middle" x="365" y="175">2</text><rect class="list" height="50" width="40" x="385" y="150" /><text dy=".3em" text-anchor="middle" x="405" y="175">3</text><rect class="list" height="50" width="40" x="425" y="150" /><text dy=".3em" text-anchor="middle" x="445" y="175">7</text><rect class="list" height="50" width="40" x="465" y="150" /><text dy=".3em" text-anchor="middle" x="485" y="175">7</text><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><path class="arrow" d="M 230,50 C 266,50 266,76 267,112 C 268,148 268,175 305,175" fill="none" marker-end="url(#id55)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="7">
                        def augment_twice_good(a_list, val):
                            a_list = a_list + [val, val]
                            return a_list

                        nums = [1, 2, 3]
                        nums = augment_twice_good(nums, 7)
                        print(nums)         # [1, 2, 3, 7, 7]
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="550" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id56" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><rect class="list" height="50" width="40" x="305" y="150" /><text dy=".3em" text-anchor="middle" x="325" y="175">1</text><rect class="list" height="50" width="40" x="345" y="150" /><text dy=".3em" text-anchor="middle" x="365" y="175">2</text><rect class="list" height="50" width="40" x="385" y="150" /><text dy=".3em" text-anchor="middle" x="405" y="175">3</text><rect class="list" height="50" width="40" x="425" y="150" /><text dy=".3em" text-anchor="middle" x="445" y="175">7</text><rect class="list" height="50" width="40" x="465" y="150" /><text dy=".3em" text-anchor="middle" x="485" y="175">7</text><rect class="name" height="50" width="98" x="132" y="25" /><text dy=".3em" text-anchor="middle" x="181" y="50">nums</text><path class="arrow" d="M 230,50 C 266,50 266,76 267,112 C 268,148 268,175 305,175" fill="none" marker-end="url(#id56)" /></svg>
            </div>
            </div>
            <!-- }}} -->
            """)

    def test_any_name_can_refer_to_any_value_at_any_time(self):
        code = '''\
            x = 12
            x = "hello"
            x = [1, 2, 3]
            x[1] = "two"
            '''

        def figure(frame):
            fig = PyFig(size=(500,400), frame_num=frame)
            layout = PyLayout(y=25, name_right=200, val_gap=75)

            x0 = auto_name(fig, layout, "", set=0)
            x = auto_name(fig, layout, "x")
            x2 = auto_name(fig, layout, "", set=0)
            x3 = auto_name(fig, layout, "", set=0)

            i_12 = fig.int(pos=layout.val_for_name(x0), text="12", set=2, fade=10)
            fig.reference(x, i_12)
            s_hello = fig.string(pos=layout.val_for_name(x), text=repr("hello"), size=(130,50), rise=2, set=3, fade=10)
            fig.reference(x, s_hello)
            l_123 = fig.list(pos=layout.val_for_name(x2), texts="123", rise=3)
            fig.reference(x, l_123[0])
            l_1s3 = fig.list(pos=layout.val_for_name(x2), texts="1 3", rise=4)
            fig.reference(x, l_1s3[0])
            s_two = fig.string(center=(l_123[1].cx, x3.cy), text=repr("two"), size=(100, 50), rise=4)
            fig.connect(l_1s3[1].center, 90, s_two.north, 90, class_="arrow", start_marker=fig.DOT, rise=4)

            cog.outl(fig.tostring())

        pyfig_animation(code, figure, [])

        self.assert_cog_output("""\
            <!-- Animation {{{ -->
            <div class="overlay">
            <pre class="python tophalf">
                        x = 12
                        x = "hello"
                        x = [1, 2, 3]
                        x[1] = "two"
                        </pre>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="1">
                        x = 12
                        x = "hello"
                        x = [1, 2, 3]
                        x[1] = "two"
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id57" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker><marker id="id58" markerHeight="4" markerWidth="4" orient="auto" refX="2" refY="2" viewBox="0,0,4,4"><circle cx="2" cy="2" fill="black" r="2" /></marker></defs><rect class="name" height="50" width="62" x="138" y="100" /><text dy=".3em" text-anchor="middle" x="169" y="125">x</text><circle class="int value" cx="300" cy="50" r="25" /><text dy=".3em" text-anchor="middle" x="300" y="50">12</text><path class="arrow" d="M 200,125 C 226,125 230,112 237,87 C 244,62 248,50 275,50" fill="none" marker-end="url(#id57)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="2">
                        x = 12
                        x = "hello"
                        x = [1, 2, 3]
                        x[1] = "two"
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id59" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker><marker id="id60" markerHeight="4" markerWidth="4" orient="auto" refX="2" refY="2" viewBox="0,0,4,4"><circle cx="2" cy="2" fill="black" r="2" /></marker></defs><rect class="name" height="50" width="62" x="138" y="100" /><text dy=".3em" text-anchor="middle" x="169" y="125">x</text><circle class="int value" cx="300" cy="50" opacity="0.25" r="25" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="300" y="50">12</text><path class="arrow" d="M 200,125 C 226,125 230,112 237,87 C 244,62 248,50 275,50" fill="none" marker-end="url(#id59)" opacity="0.25" /><rect class="string value" height="50" rx="25" ry="25" width="130" x="275" y="100" /><text dy=".3em" text-anchor="middle" x="340" y="125">'hello'</text><path class="arrow" d="M 200,125 C 218,125 218,125 237,125 C 256,125 256,125 275,125" fill="none" marker-end="url(#id59)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="3">
                        x = 12
                        x = "hello"
                        x = [1, 2, 3]
                        x[1] = "two"
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id61" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker><marker id="id62" markerHeight="4" markerWidth="4" orient="auto" refX="2" refY="2" viewBox="0,0,4,4"><circle cx="2" cy="2" fill="black" r="2" /></marker></defs><rect class="name" height="50" width="62" x="138" y="100" /><text dy=".3em" text-anchor="middle" x="169" y="125">x</text><circle class="int value" cx="300" cy="50" opacity="0.25" r="25" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="300" y="50">12</text><path class="arrow" d="M 200,125 C 226,125 230,112 237,87 C 244,62 248,50 275,50" fill="none" marker-end="url(#id61)" opacity="0.25" /><rect class="string value" height="50" opacity="0.25" rx="25" ry="25" width="130" x="275" y="100" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="340" y="125">'hello'</text><path class="arrow" d="M 200,125 C 218,125 218,125 237,125 C 256,125 256,125 275,125" fill="none" marker-end="url(#id61)" opacity="0.25" /><rect class="list" height="50" width="40" x="275" y="175" /><text dy=".3em" text-anchor="middle" x="295" y="200">1</text><rect class="list" height="50" width="40" x="315" y="175" /><text dy=".3em" text-anchor="middle" x="335" y="200">2</text><rect class="list" height="50" width="40" x="355" y="175" /><text dy=".3em" text-anchor="middle" x="375" y="200">3</text><path class="arrow" d="M 200,125 C 226,125 230,137 237,162 C 244,187 248,200 275,200" fill="none" marker-end="url(#id61)" /></svg>
            </div>
            </div>
            <div class="overlay incremental">
            <pre class="python tophalf" select="4">
                        x = 12
                        x = "hello"
                        x = [1, 2, 3]
                        x[1] = "two"
                        </pre>
            <div class="opaque bottomhalf" style="text-align:center">
            <svg baseProfile="full" height="400" version="1.1" width="500" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id63" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker><marker id="id64" markerHeight="4" markerWidth="4" orient="auto" refX="2" refY="2" viewBox="0,0,4,4"><circle cx="2" cy="2" fill="black" r="2" /></marker></defs><rect class="name" height="50" width="62" x="138" y="100" /><text dy=".3em" text-anchor="middle" x="169" y="125">x</text><circle class="int value" cx="300" cy="50" opacity="0.25" r="25" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="300" y="50">12</text><path class="arrow" d="M 200,125 C 226,125 230,112 237,87 C 244,62 248,50 275,50" fill="none" marker-end="url(#id63)" opacity="0.25" /><rect class="string value" height="50" opacity="0.25" rx="25" ry="25" width="130" x="275" y="100" /><text dy=".3em" opacity="0.25" text-anchor="middle" x="340" y="125">'hello'</text><path class="arrow" d="M 200,125 C 218,125 218,125 237,125 C 256,125 256,125 275,125" fill="none" marker-end="url(#id63)" opacity="0.25" /><rect class="list" height="50" width="40" x="275" y="175" /><text dy=".3em" text-anchor="middle" x="295" y="200">1</text><rect class="list" height="50" width="40" x="315" y="175" /><text dy=".3em" text-anchor="middle" x="335" y="200">2</text><rect class="list" height="50" width="40" x="355" y="175" /><text dy=".3em" text-anchor="middle" x="375" y="200">3</text><path class="arrow" d="M 200,125 C 226,125 230,137 237,162 C 244,187 248,200 275,200" fill="none" marker-end="url(#id63)" /><rect class="list" height="50" width="40" x="275" y="175" /><text dy=".3em" text-anchor="middle" x="295" y="200">1</text><rect class="list" height="50" width="40" x="315" y="175" /><text dy=".3em" text-anchor="middle" x="335" y="200"> </text><rect class="list" height="50" width="40" x="355" y="175" /><text dy=".3em" text-anchor="middle" x="375" y="200">3</text><path class="arrow" d="M 200,125 C 226,125 230,137 237,162 C 244,187 248,200 275,200" fill="none" marker-end="url(#id63)" /><rect class="string value" height="50" rx="25" ry="25" width="100" x="285" y="250" /><text dy=".3em" text-anchor="middle" x="335" y="275">'two'</text><path class="arrow" d="M 335,200 C 335,212 335,212 335,225 C 335,237 335,237 335,250" fill="none" marker-end="url(#id63)" marker-start="url(#id64)" /></svg>
            </div>
            </div>
            <!-- }}} -->
            """)

    def test_names_have_no_type_values_have_no_scope(self):
        # Random figure!
        fig = PyFig(size=(400,600), scale=0.55)
        layout = PyLayout(y=25, name_right=200, val_gap=175)

        r = random.Random(14)   # seeded to make it pretty good.

        def rand_name():
            return "".join(r.choice(string.lowercase) for i in range(r.randint(3,7)))

        def lightly_shuffle(seq):
            """Reorder a list randomly, but don't move things too far."""
            numbered = list(enumerate(seq))
            def jitter(p):
                return p[0]+r.randint(-3,3)
            shuffled = [x for i,x in sorted(numbered, key=jitter)]
            return shuffled

        names = []
        for i in range(r.randint(2,3)):
            names.append(auto_name(fig, layout, rand_name()))

        for f in range(3):
            num_vars = r.randint(2,3)
            fig.frame(pos=layout.next_frame(), size=(200,50+75*num_vars), text="func_"+rand_name())
            for i in range(num_vars):
                names.append(auto_name(fig, layout, rand_name()))
            layout.end_frame()

        values = []
        for name in names:
            pos = layout.val_for_name(name)
            type = r.choice(['int']*2 + ['string']*4 + ['list']*8)
            if type == 'int':
                val = fig.int(pos=pos, text=str(r.randint(5,20)))
            elif type == 'string':
                s = rand_name()
                val = fig.string(pos=pos, text=repr(s), size=(70+10*len(s), 50))
            elif type == 'list':
                els = r.randint(4, 10)
                val = fig.list(pos=pos, texts=[str(r.randint(5,20)) for i in range(els)])
                val = val[0]
            values.append(val)

        # Mix things up
        shuffled = lightly_shuffle(names)
        for name, val in zip(shuffled, values):
            fig.reference(name, val)

        cog.outl(fig.tostring())

        self.assert_cog_output("""\
            <svg baseProfile="full" height="600" version="1.1" width="400" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><marker id="id65" markerHeight="10" markerWidth="10" orient="auto" refX="10" refY="5" viewBox="0,0,10,10"><path d="M 0,0 L 10,5 L 0,10 L 1,5 z" fill="black" stroke="none" /></marker></defs><g transform="scale(0.55)"><rect class="name" height="50" width="122" x="78" y="25" /><text dy=".3em" text-anchor="middle" x="139" y="50">qyhgtr</text><rect class="name" height="50" width="98" x="102" y="100" /><text dy=".3em" text-anchor="middle" x="151" y="125">rkud</text><rect class="frame" height="200" rx="20" ry="20" width="200" x="25" y="175" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="125" y="200">func_jguqdor</text><rect class="name" height="50" width="86" x="114" y="225" /><text dy=".3em" text-anchor="middle" x="157" y="250">qdi</text><rect class="name" height="50" width="86" x="114" y="300" /><text dy=".3em" text-anchor="middle" x="157" y="325">fzk</text><rect class="frame" height="275" rx="20" ry="20" width="200" x="25" y="400" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="125" y="425">func_pwrcp</text><rect class="name" height="50" width="122" x="78" y="450" /><text dy=".3em" text-anchor="middle" x="139" y="475">ecwnfl</text><rect class="name" height="50" width="98" x="102" y="525" /><text dy=".3em" text-anchor="middle" x="151" y="550">uncv</text><rect class="name" height="50" width="86" x="114" y="600" /><text dy=".3em" text-anchor="middle" x="157" y="625">hat</text><rect class="frame" height="200" rx="20" ry="20" width="200" x="25" y="700" /><text class="framelabel" dy=".3em" opacity="1" text-anchor="middle" x="125" y="725">func_cmrnl</text><rect class="name" height="50" width="110" x="90" y="750" /><text dy=".3em" text-anchor="middle" x="145" y="775">lpcmg</text><rect class="name" height="50" width="134" x="66" y="825" /><text dy=".3em" text-anchor="middle" x="133" y="850">ybdsoas</text><rect class="list" height="50" width="40" x="375" y="25" /><text dy=".3em" text-anchor="middle" x="395" y="50">10</text><rect class="list" height="50" width="40" x="415" y="25" /><text dy=".3em" text-anchor="middle" x="435" y="50">14</text><rect class="list" height="50" width="40" x="455" y="25" /><text dy=".3em" text-anchor="middle" x="475" y="50">20</text><rect class="list" height="50" width="40" x="495" y="25" /><text dy=".3em" text-anchor="middle" x="515" y="50">9</text><rect class="list" height="50" width="40" x="535" y="25" /><text dy=".3em" text-anchor="middle" x="555" y="50">9</text><rect class="list" height="50" width="40" x="575" y="25" /><text dy=".3em" text-anchor="middle" x="595" y="50">8</text><rect class="list" height="50" width="40" x="375" y="100" /><text dy=".3em" text-anchor="middle" x="395" y="125">9</text><rect class="list" height="50" width="40" x="415" y="100" /><text dy=".3em" text-anchor="middle" x="435" y="125">11</text><rect class="list" height="50" width="40" x="455" y="100" /><text dy=".3em" text-anchor="middle" x="475" y="125">5</text><rect class="list" height="50" width="40" x="495" y="100" /><text dy=".3em" text-anchor="middle" x="515" y="125">9</text><rect class="list" height="50" width="40" x="535" y="100" /><text dy=".3em" text-anchor="middle" x="555" y="125">20</text><rect class="list" height="50" width="40" x="575" y="100" /><text dy=".3em" text-anchor="middle" x="595" y="125">14</text><rect class="list" height="50" width="40" x="615" y="100" /><text dy=".3em" text-anchor="middle" x="635" y="125">9</text><rect class="list" height="50" width="40" x="375" y="225" /><text dy=".3em" text-anchor="middle" x="395" y="250">9</text><rect class="list" height="50" width="40" x="415" y="225" /><text dy=".3em" text-anchor="middle" x="435" y="250">5</text><rect class="list" height="50" width="40" x="455" y="225" /><text dy=".3em" text-anchor="middle" x="475" y="250">7</text><rect class="list" height="50" width="40" x="495" y="225" /><text dy=".3em" text-anchor="middle" x="515" y="250">8</text><rect class="list" height="50" width="40" x="535" y="225" /><text dy=".3em" text-anchor="middle" x="555" y="250">8</text><rect class="list" height="50" width="40" x="575" y="225" /><text dy=".3em" text-anchor="middle" x="595" y="250">18</text><rect class="string value" height="50" rx="25" ry="25" width="110" x="375" y="300" /><text dy=".3em" text-anchor="middle" x="430" y="325">'pxht'</text><rect class="string value" height="50" rx="25" ry="25" width="120" x="375" y="450" /><text dy=".3em" text-anchor="middle" x="435" y="475">'pytnv'</text><rect class="string value" height="50" rx="25" ry="25" width="110" x="375" y="525" /><text dy=".3em" text-anchor="middle" x="430" y="550">'youi'</text><rect class="list" height="50" width="40" x="375" y="600" /><text dy=".3em" text-anchor="middle" x="395" y="625">8</text><rect class="list" height="50" width="40" x="415" y="600" /><text dy=".3em" text-anchor="middle" x="435" y="625">19</text><rect class="list" height="50" width="40" x="455" y="600" /><text dy=".3em" text-anchor="middle" x="475" y="625">12</text><rect class="list" height="50" width="40" x="495" y="600" /><text dy=".3em" text-anchor="middle" x="515" y="625">10</text><rect class="list" height="50" width="40" x="535" y="600" /><text dy=".3em" text-anchor="middle" x="555" y="625">9</text><rect class="list" height="50" width="40" x="575" y="600" /><text dy=".3em" text-anchor="middle" x="595" y="625">6</text><rect class="list" height="50" width="40" x="615" y="600" /><text dy=".3em" text-anchor="middle" x="635" y="625">8</text><rect class="list" height="50" width="40" x="655" y="600" /><text dy=".3em" text-anchor="middle" x="675" y="625">16</text><circle class="int value" cx="400" cy="775" r="25" /><text dy=".3em" text-anchor="middle" x="400" y="775">9</text><rect class="list" height="50" width="40" x="375" y="825" /><text dy=".3em" text-anchor="middle" x="395" y="850">11</text><rect class="list" height="50" width="40" x="415" y="825" /><text dy=".3em" text-anchor="middle" x="435" y="850">17</text><rect class="list" height="50" width="40" x="455" y="825" /><text dy=".3em" text-anchor="middle" x="475" y="850">9</text><rect class="list" height="50" width="40" x="495" y="825" /><text dy=".3em" text-anchor="middle" x="515" y="850">10</text><rect class="list" height="50" width="40" x="535" y="825" /><text dy=".3em" text-anchor="middle" x="555" y="850">11</text><rect class="list" height="50" width="40" x="575" y="825" /><text dy=".3em" text-anchor="middle" x="595" y="850">7</text><rect class="list" height="50" width="40" x="615" y="825" /><text dy=".3em" text-anchor="middle" x="635" y="850">8</text><path class="arrow" d="M 200,50 C 243,50 243,50 287,50 C 331,50 331,50 375,50" fill="none" marker-end="url(#id65)" /><path class="arrow" d="M 200,250 C 253,250 261,234 287,187 C 313,140 321,125 375,125" fill="none" marker-end="url(#id65)" /><path class="arrow" d="M 200,475 C 271,475 277,433 287,362 C 297,291 303,250 375,250" fill="none" marker-end="url(#id65)" /><path class="arrow" d="M 200,125 C 266,125 273,159 287,225 C 301,290 308,325 375,325" fill="none" marker-end="url(#id65)" /><path class="arrow" d="M 200,325 C 257,325 266,346 287,400 C 308,453 317,475 375,475" fill="none" marker-end="url(#id65)" /><path class="arrow" d="M 200,550 C 243,550 243,550 287,550 C 331,550 331,550 375,550" fill="none" marker-end="url(#id65)" /><path class="arrow" d="M 200,775 C 257,775 266,753 287,700 C 308,646 317,625 375,625" fill="none" marker-end="url(#id65)" /><path class="arrow" d="M 200,625 C 257,625 266,646 287,700 C 308,753 317,775 375,775" fill="none" marker-end="url(#id65)" /><path class="arrow" d="M 200,850 C 243,850 243,850 287,850 C 331,850 331,850 375,850" fill="none" marker-end="url(#id65)" /></g></svg>
            """)
