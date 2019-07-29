# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 00:06:10 2019

@author: yl
"""
import os
import argparse
from defaults import cfg

parser = argparse.ArgumentParser()
parser.add_argument(
    '--config',
    default="configs/resnet_50.py",
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
    
    # 复制一份 cfg
    cfg = cfg.clone()  
    # 融合 args.config 指定的的配置文件
    cfg.merge_from_file(args.config)  
    # 融合来自命令行的成对配置
    cfg.merge_from_list(args.opts)    
    # dump 每次实验参数, 方便复现
    cfg.dump(os.path.join(cfg.OUTPUT, 'dump.yaml'))
    
    print(cfg)