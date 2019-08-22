#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Tue Aug  6 20:36:47 2019
"""

from boxx import *
from boxx import pathjoin, tmpboxx, impt

import unittest

with impt(".."):
    from zcs.config import CfgNode

    CN = CfgNode
    from zcs import argument


class TestCfgNode(unittest.TestCase):
    def setUp(self):
        self.cfg = cfg = CN()

        cfg.DATA = CN()
        # cfg.DATA is config for first dataset
        # but also the default base of other cfg.DATA2/3 and cfg.TSET cfg.VAL
        cfg.DATA.DIR = argument(None, str, "Dataset dir")

        cfg.DATA.SIZE = argument(
            512, int, help="The format of dataset directory struct"
        )

        cfg.DATA.NUM_CLASS = argument(
            2, int, "Number of classes to predict (including background)."
        )

        cfg.DATA.IMG_MEAN = (104.00698793, 116.66876762, 122.67891434)

        cfg.DATA2 = cfg.DATA.clone_as_base()

        cfg.DATA2.DIR = "dir2"

        cfg.DATA3 = cfg.DATA.clone_as_base(exclude=["DIR"])

    def testBase(self):
        cfg = self.cfg.clone()
        cfg.merge_from_list_or_str(
            "DATA.DIR dir1 DATA.NUM_CLASS 10 DATA.SIZE 1024 DATA2.SIZE 256"
        )
        cfg.DATA2.update_placeholder_from_base(cfg.DATA)

        self.assertTrue(cfg.DATA2.DIR == "dir2")
        self.assertTrue(cfg.DATA2.IMG_MEAN == cfg.DATA.IMG_MEAN)
        self.assertTrue(cfg.DATA.SIZE == 1024)
        self.assertTrue(cfg.DATA2.SIZE == 256)
        self.assertTrue(cfg.DATA.NUM_CLASS == cfg.DATA2.NUM_CLASS == 10)

        cfg.DATA3.update_placeholder_from_base(cfg.DATA2)
        self.assertTrue(cfg.DATA3.DIR == None)

    def testDump(self):
        import yaml

        cfg = self.cfg.clone()
        yamlp = pathjoin(tmpboxx(), "test.yaml")
        cfg.dump(yamlp)
        cfg_dict = yaml.load(open(yamlp))
        cfgd = CfgNode(cfg_dict)
        self.assertTrue(str(cfg.dump()) == str(cfgd.dump()))

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
    pass
