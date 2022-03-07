# TODO list in Chinese

## TODO
 - [ ] if default is str, do type(default)
 - [ ] when dump, save types that not support by yaml(e.g. slice) as string
 - [ ] DEBUG: `clone()` in Windows and WSL will raise Exception
 - [ ] README: English Version
 - [ ] test code
 - [ ] dump to yaml or zcs.pkl and suport vis pkl
 - [ ] `--help`
 - [ ] try test other Action
 - [ ] for no default cfg, cfg.merge_from_list_or_str("port 2 camera.0.ip xxx")
    - now: `{"port": "2", AssertionError: Non-existent key: camera.0.ip}`
    - target: `{"port": "2", "camera":{0:{"ip":"xxx"}}}`
## Done

 - [x] add `CfgNode.clone_as_base()` and `CfgNode.update_placeholder_from_base(base)`
 - [x] README: Chinese Version
 - [x] example
 - [x] add `types.py`: `str2bool`, `fstring`
 - [x] `setup.py` and upload to `PyPI`
