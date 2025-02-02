# 仿照Rust写的结果类
# 这个很重要!!!
# 我希望程序的所有错误在控制之内
# 所以我需要这个类来封装结果
class R:
    # 构造
    def __init__(self, success: bool = True, message: str = "", data: any = None):
        self.success = success
        self.message = message
        self.data = data
        return

    # 错误输出
    def is_error(self):
        if not self.success:
            print(f"Error: {self.message}")
        return self

    # 正确输出
    def is_ok(self):
        if self.success:
            print(f"Ok: {self.message}")
        return self

    # 输出
    def __str__(self):
        return f"R(success={self.success}, message={self.message}, data={self.data})"

    # 输出
    def __repr__(self):
        return self.__str__()

    # 判断真假
    def __bool__(self):
        return self.success

    # 判断相等
    def __eq__(self, other):
        return self.success == other.success and self.message == other.message and self.data == other.data

    # 判断不等
    def __ne__(self, other):
        return not self.__eq__(other)

    # and
    def __and__(self, other):
        return R(self.success and other.success, self.message + " and " + other.message, self.data and other.data)

    # or
    def __or__(self, other):
        return R(self.success or other.success, self.message + " or " + other.message, self.data or other.data)
