# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Z Configuration System: a flexible powerful configuration system 
which takes advantage of both argparse and yacs
"""
from .__info__ import __version__

from .config import CfgNode, argument, identity
from .config import parser, parse_args, merge_by_args

from .type import str2bool, ints, str2index, fstring, try_return_None, str_or_None
