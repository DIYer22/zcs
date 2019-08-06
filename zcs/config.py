#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Fri Jul 19 13:30:51 2019
"""
import os
import copy
import yaml
from functools import wraps
import argparse
import yacs.config as yacs

def identity(x):
    return x

_None_ = {None}

class argument(argparse._AttributeHolder):
    """Same API with "parser.add_argument", but remove name and flags, ex. "--opt"
    
    Usage:    
        >>> cfg.FOO = argument(default=None, type=int, help="FOO is a int type, default is None")
    """
    def __init__(
            self, 
            default=_None_, 
            type=_None_, 
            help=_None_, 
            metavar=_None_,
            action=_None_,
            nargs=_None_,
            const=_None_,
            choices=_None_,
            required=_None_,
            dest=_None_,
        ):
        if default is None and type is not _None_:
            # when default is None
            # make sure ATTR could set back to None by args.opts
            from .type import try_return_None
            type = try_return_None(type)
        dic = dict(default=default, type=type, help=help, metavar=metavar,
            action=action, nargs=nargs, const=const, choices=choices,
            required=required, dest=dest, )
        dic = dict(filter(lambda x:x[1] is not _None_, dic.items()))
        self.__dict__.update(dic)


class CfgNode(yacs.CfgNode):
    __allow_cover__ = True
    @wraps(yacs.CfgNode.__init__)
    def __init__(self, *l, **kv):
        super(CfgNode, self).__init__(*l, **kv)
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
                            help='default is "%s", without argument' % str(value))
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

    @classmethod
    def _load_cfg_py_source(cls, filename):
        """Load a config from a Python source file."""
        module = yacs._load_module_from_file("yacs.config.override", filename)
        yacs._assert_with_logging(
            hasattr(module, "cfg"),
            "Python module from file {} must have 'cfg' attr".format(filename),
        )
        VALID_ATTR_TYPES = {dict, CfgNode, yacs.CfgNode}
        yacs._assert_with_logging(
            type(module.cfg) in VALID_ATTR_TYPES,
            "Imported module 'cfg' attr must be in {} but is {} instead".format(
                VALID_ATTR_TYPES, type(module.cfg)
            ),
        )
        return cls(module.cfg)
    
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
            key_list = full_key.replace(">",".").split(".")
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
    
    def merge_from_list_or_str(self, cfg_list_str):
        cfg_list = cfg_list_str
        if isinstance(cfg_list_str, str):
            cfg_list = cfg_list_str.strip().split()
        return self.merge_from_list(cfg_list)
    
    def dump(self, fname=None, **kwargs):
        """Dump to a string."""
        def convert_to_dict(cfg_node, key_list):
            if not isinstance(cfg_node, CfgNode):
                yacs._assert_with_logging(
                    _valid_type(cfg_node),
                    "Key {} with value {} is not a valid type; valid types: {}".format(
                        ".".join(key_list), type(cfg_node), _VALID_TYPES
                    ),
                )
                return cfg_node
            else:
                cfg_dict = dict(cfg_node)
                for k, v in cfg_dict.items():
                    cfg_dict[k] = convert_to_dict(v, key_list + [k])
                return cfg_dict

        self_as_dict = convert_to_dict(self, [])
        yaml_str = yaml.safe_dump(self_as_dict, **kwargs)
        if fname is not None:
            dir_name = os.path.dirname(fname)
            if not os.path.isdir(dir_name):
                os.makedirs(dir_name)
            with open(fname, 'w') as f:
                f.write(fname)
        return yaml_str
    
    __placeholder__ = "[__placeholder_for_CfgNode_base__]"
    
    def clone_as_base(self):
        base = self.clone()
        def trun_value_to_None_(cfg):
            for k,v in cfg.items():
                if isinstance(v, yacs.CfgNode):
                    trun_value_to_None_(v)
                else:
                    cfg[k] = self.__placeholder__
        trun_value_to_None_(base)
        return base
    
    def update_default_from_base(self, base):
        def copy_base_where_v_is_None_(child, base):
            for k,v in child.items():
                if isinstance(v, str) and v == self.__placeholder__:
                    child[k] = base[k]
                if isinstance(v, yacs.CfgNode):
                    copy_base_where_v_is_None_(child[k], base[k])
        copy_base_where_v_is_None_(self, base)
        return self
        
        
        
_VALID_TYPES = copy.deepcopy(yacs._VALID_TYPES)
_VALID_TYPES.add(type(None))
def _valid_type(value, allow_cfg_node=False):
    return (type(value) in _VALID_TYPES) or (allow_cfg_node and isinstance(value, CfgNode))

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
            _merge_a_into_b(v, b[k], root, key_list + [k])
            continue
        if isinstance(v, str):
            v = _parser_action(b, k, v)
        b[k] = v

parser = argparse.ArgumentParser(prog='Z Config System Parser')
parser.add_argument(
    '--config',
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
    
    
    
