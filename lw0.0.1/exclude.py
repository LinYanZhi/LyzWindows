import os

exclude_content = """\
# 行首是'#'视为注释
# 每行是一个排除项
Program Manager
Microsoft Text Input Application
InputTip.exe
com.ayangweb.EcoPaste-siw
"""


# 如果这两个文件不存在则创建
def init(dir, exclude_name):
    # 排除项文件
    exclude_path = os.path.join(dir, exclude_name)
    if not os.path.exists(exclude_path):
        print(f"{exclude_path} 文件不存在，创建之。")
        with open(exclude_path, 'w', encoding='utf8') as f:
            f.write(exclude_content)

    # 读取
    exclude_list = read(exclude_path)

    # 结束
    return exclude_list


# 获取
def read(exclude_path):
    # 排除项
    with open(exclude_path, 'r', encoding='utf8') as f:
        exclude_list = f.readlines()

    # 排除注释和无关字符
    exclude_list = [i.strip() for i in exclude_list if i.strip() and not i.strip().startswith('#')]

    # 结束
    return exclude_list
