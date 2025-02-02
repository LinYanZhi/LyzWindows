import json
import os
import sys
import yaml

import re


class NickName:
    data: dict
    path: str

    def __init__(self):
        self.path = os.path.join(sys.path[-1], 'nickname.yaml')
        print(self.path)
        with open(self.path, "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)
        if self.data is None:
            self.data = {}
        tmp_dict = {}
        for _, v in self.data.items():
            tmp_dict[v['process_path']] = v['nick_name']
        self.data = tmp_dict
        # print("nickname:", self.data)
        print("nickname:", json.dumps(self.data, indent=2, ensure_ascii=False))

    # def __find_matches_by_regex(self, pattern, default: str = ''):
    #     # 编译正则表达式
    #     print("pattern:", pattern)
    #     regex = re.compile(pattern)
    #
    #     # 查找匹配的键和值
    #     matched_items = {key: value for key, value in self.data.items() if regex.search(key)}
    #
    #     return matched_items if matched_items else default

    # def get_by_re(self, process_path: str, default: str = ''):
    #     ret = default
    #     for k, v in self.data.items():
    #         print("pattern:", v)
    #         pattern = re.compile(k)
    #         if bool(pattern.fullmatch(process_path)):
    #             return v
    #     return ret

    pass


g_nickname = NickName()
