#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Thu Jul 18 18:53:35 2019
"""

from boxx import *
from boxx import os
import argparse
import yacs

identity = lambda x:x

class _defaultArg():
    pass

class argument(argparse._AttributeHolder):
    def __init__(self, default=_defaultArg, type=_defaultArg, help=_defaultArg, metavar=_defaultArg):
        dic = dict(default=default, type=type, help=help, metavar=metavar)
        dic = dict(filter(lambda x:x[1] is not _defaultArg, dic.items()))
        self.__dict__.update(dic)

        
_action_dict = {
           None: argparse._StoreAction,
          'store': argparse._StoreAction,
          'store_const': argparse._StoreConstAction,
          'store_true': argparse._StoreTrueAction,
          'store_false': argparse._StoreFalseAction,
          'append': argparse._AppendAction,
          'append_const': argparse._AppendConstAction,
          'count': argparse._CountAction,
          'help': argparse._HelpAction,
          'version': argparse._VersionAction,
          'parsers': argparse._SubParsersAction
          }
def _pop_action_class(kwargs, default=None):
    action = kwargs.pop('action', default)
    return _action_dict[action]

if __name__ == "__main__":
#    _pop_action_class()
    arg = argument(1, int)
    pass
    
    
    
