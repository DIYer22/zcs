# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 00:06:10 2019

@author: yl
"""
import os
import argparse
from defaults import cfg

parser = argparse.ArgumentParser(prog='')
parser.add_argument(
    '--config',
    default="",
    metavar="FILE",
    help="Path to config file",
)
parser.add_argument(
    "opts",
    help="Modify config options using the command-line",
    default=[],
    nargs=argparse.REMAINDER,
)

if __name__ == "__main__":
    args = parser.parse_args()
    
    cfg = cfg.clone()
    cfg.merge_from_file(args.config)
    cfg.merge_from_list(args.opts)    
    print(cfg)
    
    cfg.dump(os.path.join(cfg.OUTPUT, 'dump.yaml'))

