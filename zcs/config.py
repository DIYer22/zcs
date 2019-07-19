#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Fri Jul 19 13:30:51 2019
"""

import argparse
import yacs.config as yacs
import copy
from functools import wraps

identity = lambda x:x

class _defaultArg():
    pass


class argument(argparse._AttributeHolder):
    def __init__(self, default=_defaultArg, type=_defaultArg, help=_defaultArg, metavar=_defaultArg):
        dic = dict(default=default, type=type, help=help, metavar=metavar)
        dic = dict(filter(lambda x:x[1] is not _defaultArg, dic.items()))
        self.__dict__.update(dic)


class CfgNode(yacs.CfgNode):
    __allow_cover__ = True
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
        if isinstance(value, argument):  # if argument 
            arg = value
        elif isinstance(value, CfgNode):
            value.__dict__['__parser__'].prog = parser.prog+ '.' + name
            arg = argument(default=value, type=identity, 
                            help='CfgNode')
        else:  # if only value is same as yacs
            arg = argument(default=value, 
                            help='default is "%s", without argument'%value)
        # allow replace in parser
        if self.__allow_cover__ and argk in action_dic:
            action_dic.pop(argk)
        kwargs = {
                # set default type
                'type': identity if isinstance(value, str) else self._decode_cfg_value
                }
        kwargs.update(arg.__dict__)
        parser.add_argument(argk, **kwargs)
        value = arg.__dict__.get('default', None)
        self[name] = value
        
    def merge_from_other_cfg(self, cfg_other):
        """Merge `cfg_other` into this CfgNode."""
        _merge_a_into_b(cfg_other, self, self, [])

    def merge_from_list(self, cfg_list):
        """Merge config (keys, values) in a list (e.g., from command line) into
        this CfgNode. For example, `cfg_list = ['FOO.BAR', 0.5]`.
        """
        yacs._assert_with_logging(
            len(cfg_list) % 2 == 0,
            "Override list has odd length: {}; it must be a list of pairs".format(
                cfg_list
            ),
        )
        root = self
        for full_key, v in zip(cfg_list[0::2], cfg_list[1::2]):
            if root.key_is_deprecated(full_key):
                continue
            if root.key_is_renamed(full_key):
                root.raise_key_rename_error(full_key)
            key_list = full_key.split(".")
            d = self
            for subkey in key_list[:-1]:
                yacs._assert_with_logging(
                    subkey in d, "Non-existent key: {}".format(full_key)
                )
                d = d[subkey]
            subkey = key_list[-1]
            yacs._assert_with_logging(subkey in d, "Non-existent key: {}".format(full_key))
            value = _parser_action(d, subkey, v)
            d[subkey] = value


def _parser_action(node, k, v):
    argk = k if k.startswith('--') else ('--' + k)
    parser, action_dic = node._get_parser_actions()
    action = action_dic[argk]
    v = parser._get_values(action, [v])
    return v

def _merge_a_into_b(a, b, root, key_list):
    """Merge config dictionary a into config dictionary b, clobbering the
    options in b whenever they are also specified in a.
    """
    yacs._assert_with_logging(
        isinstance(a, yacs.CfgNode),
        "`a` (cur type {}) must be an instance of {}".format(type(a), yacs.CfgNode),
    )
    yacs._assert_with_logging(
        isinstance(b, CfgNode),
        "`b` (cur type {}) must be an instance of {}".format(type(b), CfgNode),
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
        v = copy.deepcopy(v_)
        # Recursively merge dicts
        if isinstance(v, dict):
            if not isinstance(v, yacs.CfgNode):
                v = yacs.CfgNode(v)
            try:
                _merge_a_into_b(v, b[k], root, key_list + [k])
            except BaseException:
                raise
        elif isinstance(v, str):
            v = _parser_action(b, k, v)
        b[k] = v

parser = argparse.ArgumentParser(prog='Z Config System Parser')
parser.add_argument(
    'config',
    default="",
    metavar="FILE",
    help="path to config file",
)
parser.add_argument(
    "opts",
    help="Modify config options using the command-line",
    default=[],
    nargs=argparse.REMAINDER,
)

def parse_args(parser=parser):
    args = parser.parse_args()
    return args

def merge_by_args(cfg, args=None):
    if args is None:
        args = parse_args()
    if args.config:
        cfg.merge_from_file(args.config)
    cfg.merge_from_list(args.opts)
    
if __name__ == "__main__":
    pass
    
    
    
