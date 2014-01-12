# -*- coding: utf8 -*-
"""Miscellaneous helpers for SvgFig □→♡ """

def poparg(kwargs, **argdef):
    """
    Get an argument, with a default, from a dict of **kwargs.

    Use it like this::

        def fn(**kwargs):
            foo = poparg(kwargs, foo=17)

    Now `foo` is the value of the foo argument to fn, with a default of 17. The
    keyword argument can be any keyword you like, its name will be the key
    plucked from `kwargs`.

    `kwargs` has the argument removed, so that it can be passed on to
    another function.

    Arguments:
        kwargs (dict): the keyword arguments to the calling function.

    Returns:
        The value of the argument, defaulted to the value passed to the
        keyword argument.

    """
    assert len(argdef) == 1
    name, value = argdef.popitem()
    return kwargs.pop(name, value)


def defarg(kwargs, **argdef):
    """Default an argument in `kwargs` based on a keyword argument.

    Use it like this::

        def fn(**kwargs):
            defarg(kwargs, foo=17)

    If `kwargs` had a key of "foo", it's unchanged, but if it didn't, then
    it's had "foo" defined as 17 in it.

    """
    assert len(argdef) == 1
    name, value = argdef.popitem()
    kwargs.setdefault(name, value)


def add_class(add, class_):
    """Add to a CSS class attribute.

    The string `add` will be added to the classes already in `class_`, with
    a space if needed.  `class_` can be None::

        >>> add_class("foo", None)
        'foo'
        >>> add_class("foo", "bar")
        'bar foo'

    Returns the amended class string.

    """
    if class_:
        class_ += " "
    else:
        class_ = ""
    return class_ + add
