#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Sun Jul 21 10:19:38 2019
"""
from zcs.config import CfgNode as CN

# 　zcs 具有和 yacs 一样的接口和用法
from zcs import argument

cfg = CN()

cfg.LR = 1e-3
# 完全兼容 yacs 形式的自动识别 type

cfg.OUTPUT = argument(default=None, type=str, help="Output dir")
# 使 argument 来配置 default, type, help.
# argument 用法和 parser.add_argument 一样

cfg.MODEL = CN()  # 新建节点

cfg.MODEL.LAYERS = argument(101, int, "How many layers of model")
# 等价于 parser.add_argument(default=101, type=int, help="...")

# 支持 choices 等多种 parser.add_argument 的接口
cfg.MODEL.BACKBONE = argument(
    default="resnet",
    choices=["resnet", "shufflenet", "senet"],
    help="Backbone of the model",
)

if __name__ == "__main__":
    print(cfg)
