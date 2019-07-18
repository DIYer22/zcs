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
#import argparse_local as argparse

from argument import argument, identity


from argument import argument as _argument


parser = argparse.ArgumentParser(prog='PROG', allow_abbrev=True)
parser.add_argument('--aA', type=float, default=None)
parser.add_argument('d', type=float, default=None)
parser.add_argument('dd', type=float, default=None)
ac = parser.add_argument('--foobar', action='store_true')
ac = parser.add_argument('--c', type=eval, default={})
parser._option_string_actions.pop('--c')
ac = parser.add_argument('--c', type=eval, default={})
#ac = parser.add_argument('--d', default=None, choices=['rock', 'paper', 'scissors'])
if len(sys.argv)>=2:
    args = parser.parse_args()
else:
    args = parser.parse_args(['--foobar', '2', '4', '--c', '[1 , 4]'])

pad = parser.__dict__
print(args)

import copy
_VALID_TYPES = copy.deepcopy(yacs._VALID_TYPES)
_VALID_TYPES.add(type(None))
def _valid_type(value):
    return (type(value) in _VALID_TYPES)

CN = yacs.CfgNode
from functools import wraps
class ZcfgNode(yacs.CfgNode):
    __allow_replace__ = True
#    __allow_replace__ = False
    @wraps(yacs.CfgNode.__init__)
    def __init__(self, *l, **kv):
        super(type(self), self).__init__(*l, **kv)
        parser = argparse.ArgumentParser(prog='cfg')
        self.__dict__['__parser__'] = parser
        self.__dict__['__action_dic__'] = parser._option_string_actions
    
    def _get_parser_actions(self):
        return self.__dict__['__parser__'], self.__dict__['__action_dic__']
    
    def __setattr__(self, name, value):
        if self.is_frozen():
            raise AttributeError(
                "Attempted to set {} to {}, but CfgNode is immutable".format(
                    name, value
                )
            )

        yacs._assert_with_logging(
            name not in self.__dict__,
            "Invalid attempt to modify internal CfgNode state: {}".format(name),
        )
        
        parser, action_dic = self._get_parser_actions()
        argk = name if name.startswith('--') else ('--' + name)
        if isinstance(value, _argument):
            arg = value
        elif isinstance(value, ZcfgNode):
            value.__dict__['__parser__'].prog = parser.prog+ '.' + name
            arg = _argument(default=value, type=identity, 
                            help='ZcfgNode')
        else:
            typef = identity if isinstance(value, str) else yacs._decode_cfg_value
            arg = _argument(default=value, type=typef, 
                            help='default is "%s", without argument'%value)
        if self.__allow_replace__ and argk in action_dic:
            action_dic.pop(argk)
        action = parser.add_argument(argk, **arg.__dict__)
        value = arg.__dict__.get('default', None)
        self[name] = value
    def merge_from_other_cfg(self, cfg_other):
        """Merge `cfg_other` into this CfgNode."""
        _merge_a_into_b(cfg_other, self, self, [])


def _merge_a_into_b(a, b, root, key_list):
    """Merge config dictionary a into config dictionary b, clobbering the
    options in b whenever they are also specified in a.
    """
    yacs._assert_with_logging(
        isinstance(a, yacs.CfgNode),
        "`a` (cur type {}) must be an instance of {}".format(type(a), yacs.CfgNode),
    )
    yacs._assert_with_logging(
        isinstance(b, ZcfgNode),
        "`b` (cur type {}) must be an instance of {}".format(type(b), ZcfgNode),
    )

    for k, v_ in a.items():
        full_key = ".".join(key_list + [k])
        # a must specify keys that are in b
        if k not in b:
            if root.key_is_deprecated(full_key):
                continue
            elif root.key_is_renamed(full_key):
                root.raise_key_rename_error(full_key)
            else:
                raise KeyError("Non-existent config key: {}".format(full_key))
        v = v_
        # Recursively merge dicts
        if isinstance(v, yacs.CfgNode):
            try:
                _merge_a_into_b(v, b[k], root, key_list + [k])
            except BaseException:
                raise
        else:
            v = copy.deepcopy(v_)
            if isinstance(v, str):
                argk = k if k.startswith('--') else ('--' + k)
                parser, action_dic = b._get_parser_actions()
                v = action_dic.type(argk)
            b[k] = v


CN = ZcfgNode
cfg = CN()

cfg.TASK = 'rotor_demo'
cfg.OUTPUT = '/tmp'
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



cfg.TEST = argument(2)
cfg.TEST = argument(2)

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
    
    
    
