#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Sun Jul 21 10:19:38 2019
"""
from zcs import CfgNode as CN
from zcs import argument 

cfg = CN()
# 
cfg.LR = 1e-3
cfg.OUTPUT = argument(default=None, type=str, help="output dir")
cfg.MODEL = CN()
cfg.MODEL.BACKBONE = argument(
        default='resnet', 
        choices=['resnet', 'shufflenet', 'senet'],
        help="backbone of the model",
        )
cfg.MODEL.LAYERS = 101


if __name__ == "__main__":
    print(cfg)
    
    
