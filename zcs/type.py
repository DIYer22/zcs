#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Fri Jul 19 21:25:18 2019
"""
import sys
import argparse


def str2bool(s):
    if isinstance(s, str):
        if s.lower() in ("yes", "true", "t", "y", "1"):
            return True
        elif s.lower() in ("no", "false", "f", "n", "0"):
            return False
    if s in (None, True, False, 1, 0):
        return bool(s)
    raise argparse.ArgumentTypeError('Boolean value expected. But got "%s"' % s)


def ints(s):
    """Return a list of int in the string"""
    import re

    return list(map(int, re.findall(r"-?\d+\d*", s)))


def str2index(s):
    """
    return a index or slice
    """
    if ":" in s:  # is slice

        class GetSlice:
            @classmethod
            def __getitem__(self, slicee):
                return slicee

        return eval("GetSlice()[%s]" % s.replace("[", "").replace("]", ""))
    else:
        return ints(s)


def fstring(eval_locals=None):
    """Treate the string as fstring

    Usage:
        >>> agument(type=fstring())
    """
    if eval_locals is None:
        eval_locals = sys._getframe(1).f_locals

    def _fstring(s):
        code = 'f"""%s"""' % s
        return eval(code, eval_locals)

    return _fstring


def try_return_None(type_fun):
    """If a string s == "None", return None
    else return type_fun(s)
    """

    def _type(s):
        if s.strip() in ("None",):
            return None
        else:
            return type_fun(s)

    return _type


str_or_None = try_return_None(str)


if __name__ == "__main__":
    aa = 55
    typee = fstring(dict(aa=3))
    s = typee("aa={aa}")
    assert s == "aa=3", s

    l = list(range(6))

    s = ":2"
    assert l[str2index(s)] == [0, 1]
    s = "[4:]"
    assert l[str2index(s)] == [4, 5]
    s = ":4:2"
    assert l[str2index(s)] == [0, 2]
    s = "4, 2"
    assert str2index(s) == [4, 2]

    pass
