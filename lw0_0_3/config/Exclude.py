import json
import os
import sys
import yaml


class Exclude:
    data: dict
    path: str

    def __init__(self):
        self.path = os.path.join(sys.path[-1], 'exclude.yaml')
        print(self.path)
        with open(self.path, "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)
        if self.data is None:
            self.data = {}
        for _, v in self.data.items():
            for key, value in v.items():
                if isinstance(value, list):
                    self.data[_][key] = tuple(value)
        # print("exclude:", self.data)
        print("exclude:", json.dumps(self.data, indent=2, ensure_ascii=False))

    pass


g_exclude = Exclude()
