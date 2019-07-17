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
parser.add_argument('--foobar', action='store_true')
parser.add_argument('--a', type=float, default=None)
ac = parser.add_argument('--c', type=eval, default={})
args = parser.parse_args(['--foobar', '--c', '[1 , 4]'])

print(args)




if __name__ == "__main__":
    pass
    
    
    
