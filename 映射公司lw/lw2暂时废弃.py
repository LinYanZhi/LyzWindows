import win32gui
import win32api
import win32con
import win32process
import psutil
import time

# pip install win32gui win32api win32con win32process psutil

# 缩放比例步长
SCALE_STEP = 0.1

# 持续时间
DURATION = 0.1  # 越短越平滑 但是次数多了会有卡顿
# 次数
STEPS = 10  # 次数越多越平滑 但是慢

# 封装一个窗口控制类
class WindowControl:
    # 基本属性
    handle = None
    left = 0
    top = 0
    width = 0
    height = 0
    title = ''
    pid = 0
    exe_path = ''

    def __init__(self, handle):
        self.handle = handle

    # 自赋值
    def __auto_assign(self):
        self.left, self.top, self.right, self.bottom = win32gui.GetWindowRect(self.handle)
        self.width = self.right - self.left
        self.height = self.bottom - self.top
        self.title = win32gui.GetWindowText(self.handle)
        self.pid = win32process.GetWindowThreadProcessId(self.handle)[1]
        try:
            process = psutil.Process(self.pid)
            self.exe_path = process.exe()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            self.exe_path = None
        return

    # (坐标)移动该窗口
    def __move(self, left: int, top: int):
        self.__auto_assign()
        win32gui.MoveWindow(self.handle, int(left), int(top), self.width, self.height, True)

    # (坐标)丝滑移动该窗口
    def __move_silky(self, target=None, target_left=None, target_top=None, duration=DURATION, steps=STEPS):
        """
        丝滑移动窗口到目标位置
        
        参数:
        target: 位置关键词，如'center', 'left_top'等
        target_left: 目标位置的左坐标(如果提供了target则忽略)
        target_top: 目标位置的上坐标(如果提供了target则忽略)
        duration: 移动持续时间(秒)
        steps: 移动步数
        """
        
        # 如果提供了target参数，则计算目标坐标
        if target:
            screen_size = get_screen_size()
            if target == 'center':
                target_left = (screen_size[0] - self.width) // 2
                target_top = (screen_size[1] - self.height) // 2
            elif target == 'left_top':
                target_left = 0
                target_top = 0
            elif target == 'right_top':
                target_left = screen_size[0] - self.width
                target_top = 0
            elif target == 'left_bottom':
                target_left = 0
                target_top = screen_size[1] - self.height
            elif target == 'right_bottom':
                target_left = screen_size[0] - self.width
                target_top = screen_size[1] - self.height
            elif target == 'left_center':
                target_left = 0
                target_top = (screen_size[1] - self.height) // 2
            elif target == 'right_center':
                target_left = screen_size[0] - self.width
                target_top = (screen_size[1] - self.height) // 2
            elif target == 'top_center':
                target_left = (screen_size[0] - self.width) // 2
                target_top = 0
            elif target == 'bottom_center':
                target_left = (screen_size[0] - self.width) // 2
                target_top = screen_size[1] - self.height
        
        # 确保目标坐标有效
        if target_left is None or target_top is None:
            raise ValueError("必须提供target或target_left和target_top参数")
        
        # 计算每一步需要移动的距离
        step_left = (target_left - self.left) / steps
        step_top = (target_top - self.top) / steps
        
        # 计算每一步的时间间隔
        step_time = duration / steps
        
        # 逐步移动窗口
        original_left, original_top = self.left, self.top
        for i in range(steps):
            new_left = original_left + step_left * (i + 1)
            new_top = original_top + step_top * (i + 1)
            self.__move(new_left, new_top)
            time.sleep(step_time)
        
        # 确保最终位置准确
        self.__move(target_left, target_top)

    # 移动窗口到... 获取坐标(left, top)
    def _get_target_xy(self, key: str = '', model='center'):
        # 获取当前电脑屏幕大小
        screen_size = get_screen_size()

        # 移动窗口到屏幕左上角
        if key == '7' or model == 'left_top':
            return 0, 0
        # 移动窗口到屏幕上半部分
        elif key == '8' or model == 'top_center':
            return (screen_size[0] - self.width) // 2, 0
         # 移动窗口到屏幕右上角
        elif key == '9' or model == 'right_top':
            return screen_size[0] - self.width, 0

        # 移动窗口到屏幕左半部分
        elif key == '4' or model == 'left_center':
            return 0, (screen_size[1] - self.height) // 2
        # 移动窗口到屏幕中心
        if key == '5' or model == 'center':
            return (screen_size[0] - self.width) // 2, (screen_size[1] - self.height) // 2
        # 移动窗口到屏幕右半部分
        elif key == '6' or model == 'right_center':
            return screen_size[0] - self.width, (screen_size[1] - self.height) // 2

        # 移动窗口到屏幕左下角
        elif key == '1' or model == 'left_bottom':
            return 0, screen_size[1] - self.height
        # 移动窗口到屏幕下半部分
        elif key == '2' or model == 'bottom_center':
            return (screen_size[0] - self.width) // 2, screen_size[1] - self.height
        # 移动窗口到屏幕右下角
        elif key == '3' or model == 'right_bottom':
            return screen_size[0] - self.width, screen_size[1] - self.height

        # 移动到左对齐
        elif key == 'left':
            return 0, self.top
        # 移动到右对齐
        elif key == 'right':
            return screen_size[0] - self.width, self.top
        # 移动到上对齐
        elif key == 'top':
            return self.left, 0
        # 移动到下对齐
        elif key == 'bottom':
            return self.left, screen_size[1] - self.height

        else:
            return self.left, self.top

    # ============================ 移动窗口位置 ============================

    # 移动
    def move(self, key: str = '', model='center'):
        left, top = self._get_target_xy(key, model)
        self.__move(left, top)

    # 丝滑移动
    def move_silky(self, key: str = '', model='center'):
        left, top = self.__get_target_xy(key, model)
        self.__move_silky(target_left=left, target_top=top)

    # ============================ 改变窗口大小 ============================
    
    # (坐标)改变该窗口的大小：变大后窗口的正中心不变
    def __resize(self, width: int, height: int):
        self.__auto_assign()
        # win32gui.MoveWindow(self.handle, self.left, self.top, width, height, True)
        # 原本的窗口正中心
        center_x = self.left + self.width // 2
        center_y = self.top + self.height // 2
        # 计算新的窗口位置
        new_left = center_x - width // 2
        new_top = center_y - height // 2
        # 改变窗口大小
        win32gui.SetWindowPos(self.handle, None, new_left, new_top, width, height, win32con.SWP_NOZORDER)

    # 以窗口正中心为基准 改变窗口大小：改变创建之后，窗口的正中心位置不变
    def __resize_center(self, scale_factor = SCALE_STEP):
        left, top, right, bottom = win32gui.GetWindowRect(self.handle)
        width = right - left
        height = bottom - top
        new_width = int(width * (1 + scale_factor))
        new_height = int(height * (1 + scale_factor))

        # 获取屏幕分辨率
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)

        # 确保窗口不会超出屏幕边界
        new_width = min(new_width, screen_width)
        new_height = min(new_height, screen_height)

        # 重新计算窗口位置以保持居中
        new_left = (screen_width - new_width) // 2
        new_top = (screen_height - new_height) // 2

        win32gui.SetWindowPos(self.handle, None, new_left, new_top, new_width, new_height, win32con.SWP_NOZORDER)

    # 丝滑改变窗口大小 拆分成多个步骤 窗口变大后 窗口正中心位置不变
    def resize_silky(self, scale_factor = SCALE_STEP, duration=DURATION, steps=STEPS):
        # 获取当前窗口大小
        left, top, right, bottom = win32gui.GetWindowRect(self.handle)
        width = right - left
        height = bottom - top
        # 计算新的窗口大小
        new_width = int(width * (1 + scale_factor))
        new_height = int(height * (1 + scale_factor))
        # 计算每一步需要改变的大小
        step_width = (new_width - width) / steps
        step_height = (new_height - height) / steps
        # 计算每一步的时间间隔
        step_time = duration / steps
        # 逐步改变窗口大小
        for i in range(steps):
            width += step_width
            height += step_height
            self.__resize(int(width), int(height))
            time.sleep(step_time)
        # 确保最终大小准确
        self.__resize(new_width, new_height)

    # 窗口变大
    def window_big(self, scale_factor = SCALE_STEP):
        self.resize_silky(scale_factor)
    
    # 窗口变小
    def window_small(self, scale_factor = SCALE_STEP):
        self.resize_silky(-scale_factor)

    pass


# 获取当前激活的窗口：
def get_active_window():
    return win32gui.GetForegroundWindow()


# 获取当前电脑尺寸(如果电脑有缩放比 则获取实际的宽高px)
def get_screen_size():
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)


if __name__ == '__main__':
    # 获取到当前电脑屏幕大小
    screen_size = get_screen_size()
    print(f'当前电脑屏幕大小为：{screen_size}')

    time.sleep(1)
    # 获取当前激活窗口
    window = get_active_window()
    # 实例化窗口控制类
    window_control = WindowControl(window)

    

    



    

