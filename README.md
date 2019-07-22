English version README is coming soon
# zcs 中文说明

**`zcs`** is short of "<strong>Z</strong>  <strong>C</strong>onfiguration <strong>S</strong>ystem": 结合了 `argparse` and `yacs` 的优点而打造出的**灵活, 强大**的配置管理系统

## 竞品对比

| configuration system | 缺点 | 优点 |
| :-- | -- | -- |
| `argparse` | 不支持配置文件, 不支持层级结构, 难以有效的 dump 和复现实验参数 | `add_argument` 强大的 default, type 和 help 参数易于使用 |
| `yacs` | 类型系统只支持仅有的几种类型, 不支持 `None`, 且类型 check 令人困惑 | 1. 灵活易用的层级配置; 2. 方便的 dump 和 load, 能有效的对实验参数进行记录与复现 |


为此, 我将 `argparse` 和 `yacs` 整合在一起, 打造出了集两者优点于一身的 **`zcs`** :
1. 具有和 `argparse.add_argument` 一样的定义 argument 的接口, 支持 NoneType, 自定义 Type, 易于使用
1. 和 `yacs` 具有同样的层级配置管理能力, 及方便的 dump 和 load, 能有效的对实验参数进行记录与复现
1. 用法完全兼容 `yacs` 和 `argparse`, 学习成本低



## Example
使用 `zcs` 科学管理 config 的一个样例, 样例的代码在 [zcs/example](./example)

**文件结构:**   
```bash
example/
├── configs  # 可选配置文件
│   ├── resnet_50.py
│   └── senet_152.yaml
├── defaults.py  # config 的模版
└── main.py
```
1. 首先得定义一个 config 的模版: **defaults.py**   

```python
from zcs.config import CfgNode as CN
#　zcs 具有和 yacs 一样的接口和用法
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
        default='resnet', 
        choices=['resnet', 'shufflenet', 'senet'],
        help="Backbone of the model",
        )
```

2. 接下来需要对每个实验写一个配置文件:  

```yaml
# configs/senet_152.yaml
OUTPUT: 'outputs/senet_152'
MODEL:
    BACKBONE: 'senet'
    LAYERS: 152
```

当然, 配置文件也可以是 python 文件, 这样会更加灵活和智能:   
```python
# configs/resnet_50.py
from zcs.config import CfgNode as CN

cfg = CN()
cfg.OUTPUT = 'outputs/resnet_50'
cfg.MODEL = CN()
cfg.MODEL.LAYERS = 50
```

3. 在 **main.py** 内融合各层次的配置, 并生成最终的 cfg

```python
import os
import argparse
from defaults import cfg

parser = argparse.ArgumentParser()
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
    
    # 复制一份 cfg
    cfg = cfg.clone()  
    # 融合 args.config 指定的的配置文件
    cfg.merge_from_file(args.config)  
    # 融合来自命令行的成对配置
    cfg.merge_from_list(args.opts)    
    # dump 每次实验参数, 方便复现
    cfg.dump(os.path.join(cfg.OUTPUT, 'dump.yaml'))
    
    print(cfg)
```


4. 比如, 现在要做一个基于 senet_152 学习率调大到 0.05 的实验  

```bash
$ python main.py --config configs/senet_152.yaml LR 0.005 OUTPUT outputs/senet_152_lr0.005

LR: 0.005
MODEL:
  BACKBONE: senet
  LAYERS: 152
OUTPUT: outputs/senet_152_lr0.005

```
