#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Wed Jul 17 20:10:27 2019
"""

from boxx import *
from boxx import os, impt, sys, openread, g

with impt(".."):
    from zcs.config import CfgNode, argument

# import argparse
import yacs.config as yacs

# import yacs_local as yacs
import argparse_local as argparse
import yaml


def get_parser():
    parser = argparse.ArgumentParser(prog="PROG", allow_abbrev=True)
    parser.add_argument("a", type=float, default=None)
    ac = parser.add_argument("--foobar", action="store_true")
    ac = parser.add_argument("--c", type=eval, default={})
    parser._option_string_actions.pop("--c")
    ac = parser.add_argument("--c", type=eval, default={})
    # ac = parser.add_argument('--d', default=None, choices=['rock', 'paper', 'scissors'])
    if len(sys.argv) >= 2:
        args = parser.parse_args()
    else:
        args = parser.parse_args(["1", "--foobar", "--c", "[1 , 4]"])

    pad = parser.__dict__
    g()
    return args
    print(args)


CN = CfgNode
cfg = CN()
cfg.TASK = "task"
cfg.NODE = CN()
cfg.NODE.ATTR1 = argument(None, eval)
cfg.TEST = argument(2)
cfg.TEST = argument(None, str, choices=["1", "b", "c"])
cfg.TEST = argument(None, str, choices=[None, "1", "b", "c"])
# cfg.TEST = '9'

yamlp = "a.yaml"
cfg.merge_from_file(yamlp)
cfg.merge_from_list(["TEST", "None", "NODE.ATTR1", "9+1"])

print(cfg)


def load_yaml(yamlp):
    yamlstr = openread(yamlp)
    ya = yaml.safe_load(yamlstr)
    return ya
    print(ya)


s = cfg.dump()
print("\n\ndump:")
print(s)

if __name__ == "__main__":
    pass
