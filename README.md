# zcs 中文说明

**`zcs`** is short of "<strong>Z</strong>  <strong>C</strong>onfiguration <strong>S</strong>ystem": 结合了 `argparse` and `yacs` 的优点而打造出的**灵活, 强大**的配置文件管理系统

## 竞品对比

| configuration system | 缺点 | 优点 |
| :-- | -- | -- |
| `argparse` | 不支持配置文件, 不支持层级结构, 不支持合并 | 
| `yacs` | 不支持 `None`, 类型系统令人困惑 |


为此, 我将 `argparse` 和 `yacs` 整合在一起, 打造出了集两者优点于一身的 **`zcs`** :
1. `argparse.add_argument` 一样的定义 argument 的接口, 易于使用
1. 支持 NoneType, 自定义 Type
1. 和 `yacs` 具有同样的管理能力





