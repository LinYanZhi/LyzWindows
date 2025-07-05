import json
import os

default_config = {
    "width": 288,
    "height": 292,
    "x": 659,
    "y": 535,
    "bg_color": "#1e1f22",
    "border_color": "#2b2d30",
    "corner_color": "lightgreen",
    "is_topmost": True,
    "topmost_border_color": "#444447",
    "menu_bg_color": "white",
    "menu_fg_color": "black"
}


# width                宽度
# height               高度
# x                    x坐标
# y                    y坐标
# bg_color             背景颜色
# border_color         边框颜色
# corner_color         角落颜色
# is_topmost           是否置顶
# topmost_border_color 置顶边框颜色
# menu_bg_color        菜单背景颜色
# menu_fg_color        菜单前景颜色


# 负责配置文件的所有操作：
class Config:
    config_file_path: str
    config: dict

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.load_config()
        return

    def load_config(self):
        # 判断配置文件是否存在
        if os.path.exists(self.config_file_path):
            # 如果存在，则打开配置文件
            with open(self.config_file_path, 'r') as f:
                # 将配置文件中的内容加载到self.config中
                self.config = json.load(f)
        else:
            # 如果配置文件不存在，则使用默认配置
            self.config = default_config
            # 保存默认配置
            self.save_config()
        # 如果配置项不全，则补上
        for key in default_config:
            if key not in self.config:
                self.config[key] = default_config[key]
        return

    def save_config(self):
        with open(self.config_file_path, 'w') as f:
            json.dump(self.config, f, indent=4)
        return

    # 重载[]
    def __getitem__(self, item):
        return self.config[item]

    # 重载[] =
    def __setitem__(self, key, value):
        self.config[key] = value
        # self.save_config()
        return

    pass


if __name__ == "__main__":
    config = Config("config.json")
    print(config.config)
