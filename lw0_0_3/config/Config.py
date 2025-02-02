import json
import os.path

import yaml
import sys


class Config:
    data: dict
    path: str

    def __init__(self):
        self.path = os.path.join(sys.path[-1], 'config.yaml')
        print(self.path)
        with open(self.path, "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)
        # print("config:", self.data)
        print("config:", json.dumps(self.data, indent=2, ensure_ascii=False))
        return

    def update(self):
        with open(self.path, "w", encoding="utf-8") as f:
            yaml.dump(self.data, f, allow_unicode=True)
        return

    pass


g_config = Config()
