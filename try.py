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
import yacs_local as yacs
import argparse_local as argparse




parser = argparse.ArgumentParser(prog='PROG', allow_abbrev=True)
parser.add_argument('--a', type=float, default=None)
ac = parser.add_argument('--foobar', action='store_true')
ac = parser.add_argument('--c', type=eval, default={})
#ac = parser.add_argument('--d', default=None, choices=['rock', 'paper', 'scissors'])
args = parser.parse_args(['--foobar', '--c', '[1 , 4]'])

print(args)

CN = yacs.CfgNode

cfg = CN()

cfg.TASK = 'rotor_demo'
cfg.OUTPUT = '/tmp'

cfg.MODEL = CN()
# conv-strategy "none"|"one"|"distance"|"each"
cfg.MODEL.FEATURE_ALIGN = "none"

cfg.MODEL.OUTPUT_STRIDE = 4

cfg.MODEL.WEIGHT = None



cfg.AFFINITY = CN()
# Ds for aff
cfg.AFFINITY.DS = [1,2,4,8]
# direct code
cfg.AFFINITY.DIRECT_CODE = ''
# min_gap for getBiassByMinSize
cfg.AFFINITY.MIN_GAP = -1
# max_len for getBiassByMinSize
cfg.AFFINITY.MAX_LEN = -1

cfg.AFFINITY.INVERT_BIAS = -1
print(cfg)



yamlp = 'a.yaml'
#cfg.merge_from_file(yamlp)

cfg.merge_from_list(['AFFINITY.DIRECT_CODE', '1'])

import yaml

yamlstr = openread(yamlp)
ya = yaml.safe_load(yamlstr)
print(ya)
if __name__ == "__main__":
    pass
    
    
    
