#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Wed Jul 17 20:10:27 2019
"""

from boxx import *
from boxx import os
import argparse
import yacs.config as yacs
#import yacs_local as yacs
import argparse_local as argparse
import copy
from zcs.config import CfgNode, argument, identity


parser = argparse.ArgumentParser(prog='PROG', allow_abbrev=True)
parser.add_argument('aA', type=float, default=None)
#parser.add_argument('d', type=float, default=None)
#parser.add_argument('dd', type=float, default=None)
ac = parser.add_argument('--foobar', action='store_true')
ac = parser.add_argument('--c', type=eval, default={})
parser._option_string_actions.pop('--c')
ac = parser.add_argument('--c', type=eval, default={})
#ac = parser.add_argument('--d', default=None, choices=['rock', 'paper', 'scissors'])
if len(sys.argv)>=2:
    args = parser.parse_args()
else:
    args = parser.parse_args(['1','--foobar', '--c', '[1 , 4]'])

pad = parser.__dict__
print(args)


_VALID_TYPES = copy.deepcopy(yacs._VALID_TYPES)
_VALID_TYPES.add(type(None))
def _valid_type(value):
    return (type(value) in _VALID_TYPES)


CN = CfgNode
cfg = CN()
cfg.TASK = 'rotor_demo'
cfg.NODE = CN()
cfg.TEST = argument(2)
cfg.TEST = (2)
#cfg.TEST = argument(2)


yamlp = 'a.yaml'
#cfg.merge_from_file(yamlp)

cfg.merge_from_list([ 'TEST', 'a10'])

import yaml

print([cfg.TEST])


yamlstr = openread(yamlp)
ya = yaml.safe_load(yamlstr)
#print(ya)
if __name__ == "__main__":
    pass
    
    
    
