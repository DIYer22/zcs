# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
Z Configuration System: a flexible powerful configuration system 
which takes advantage of both argparse and yacs
'''
__version__ = "0.1.9"
__short_description__ = "Z Configuration System: a flexible powerful configuration system which takes advantage of both argparse and yacs"
__license__ = "MIT"
__author__ = "DIYer22"
__author_email__ = "ylxx@live.com"
__maintainer__ = "DIYer22"
__maintainer_email__ = "ylxx@live.com"
__github_username__ = "DIYer22"
__github_url__ = "https://github.com/DIYer22/zcs"
__support__ = "https://github.com/DIYer22/zcs/issues"


from .config import CfgNode, argument, identity
from .config import parser, parse_args, merge_by_args

from .type import str2bool, ints, fstring, try_return_None


