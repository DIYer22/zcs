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

## 使用方法





