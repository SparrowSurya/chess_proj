import json
from os import path
from typing import Any

from const import COLOR_C1, COLOR_C2, COLOR_H1, COLOR_H2

ROOT_PATH = path.split(__file__)[0]

FILE = f"{ROOT_PATH}\\data\\config.json"
UFILE = f"{ROOT_PATH}\\data\\uconfig.json"


with open(FILE, 'r') as f:
    _Config = json.loads(f.read())

with open(UFILE, 'r') as f:
    _uConfig = json.loads(f.read())

IMG_DIR = _uConfig['img_dir']


class cfg(dict):
    __file = FILE

    def __init__(self):
        super().__init__({key:_Config[key] for key in _Config.keys()})
    
    def __str__(self):
        return json.dumps(self, sort_keys=False, indent=4, separators=(',', ': '))
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in self.keys:
            self[__name] = __value
    
    def config(self, __key: str, __value: Any) -> None:
        """updates both file and gui"""
        if __key not in _Config.keys():
            return False

        self[__key] = __value
        with open(self.__file, 'w') as f:
            new_cfg = {key: val for key, val in self.items()}
            data = json.dumps(new_cfg, sort_keys=False, indent=4, separators=(',', ': '))
            f.write(data)
        return True
    
    def color_type(self, r: int, c: int) -> str:
        """Returns cell colour type based on its location."""
        return COLOR_C1 if (r+c)%2 else COLOR_C2
    
    def highlight_type(self, r: int, c: int) -> str:
        """Returns cell hightlight colour type based on its location."""
        return COLOR_H1 if (r+c)%2 else COLOR_H2

