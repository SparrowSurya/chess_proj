import json
from os import path
from typing import Any

from const import *


ROOT_PATH = path.split(__file__)[0]

FILE = f"{ROOT_PATH}\\data\\config.json"
UFILE = f"{ROOT_PATH}\\data\\uconfig.json"


with open(FILE, 'r') as f:
    _Config = json.loads(f.read())

with open(UFILE, 'r') as f:
    _uConfig = json.loads(f.read())


IMG_DIR = _uConfig['img_dir']


class cfg():
    __Config = _Config
    __file = FILE
    __cfg = {key: _Config[key] for key in _Config.keys()}

    def __init__(self):
        pass
    
    def __str__(self):
        return json.dumps(self.__cfg, sort_keys=False, indent=4, separators=(',', ': '))

    @property
    def file(self):
        return self.__file
    
    @property
    def keys(self):
        return self.__cfg.keys()

    def __getitem__(self, __key: str):
        return self.__cfg[__key]
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in self.keys:
            self.__cfg[__name] = __value
    
    def config(self, __key: str, __value: Any) -> None:
        """updates both file and gui"""
        if __key not in _Config.keys():
            return False

        self.__cfg[__key] = __value
        with open(self.__file, 'w') as f:
            new_cfg = {key: self.__cfg[key] for key in self.__Config.items()}
            data = json.dumps(new_cfg, sort_keys=False, indent=4, separators=(',', ': '))
            f.write(data)
        return True