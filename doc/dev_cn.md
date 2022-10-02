# dev draft in Chinese


需求:
- 支持 args
- 能够继承配置
- 需要科学的 help
    - 支持和 argparse 相似的 type 和 help
- 各种变量需求
    - 支持 None
- 能被 dump 为 yaml
    - 同时能 dump pikels


## 竞品
- hydra:
    - https://hydra.cc/
    - https://github.com/ashleve/lightning-hydra-template
- hpman: https://github.com/megvii-research/hpman
- omegaconf: https://github.com/omry/omegaconf
    - hydra 前身
    - 对 yaml 做了大量定制
    - 优点:
        - cli: arg=value
        - 支持关系路径, 并动态解析, nested 路径
- https://github.com/google/gin-config

vs mmdet
优点
- 

缺点
- 不支持通过更改 args 快速实验
- mmdet 继承关系是定制的, 不是 python 原生, 对编辑器不友好
- 不支持


vs yacs
- 支持 None
- 支持


vs argparse



