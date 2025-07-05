import win32gui
import win32process
import psutil
import keyboard
import win32con
import win32api
from pynput import mouse
from win10toast import ToastNotifier
from datetime import datetime
import time
import threading

class WindowManager:
    def __init__(self):
        # 初始化参数
        self.scale_step = 0.1
        self.move_step = 10
        self.shift_vertical_move = True
        self.ctrl_vertical_scale = True
        self.double_click_timeout = 0.5
        self.notification_duration = 2
        self.anti_shake_duration = 0.5  # 减少防抖时间，提高响应速度
        self.listening_enabled = True
        self.last_esc_switch_time = 0
        self.toaster = ToastNotifier()
        
        # 双击检测状态
        self.key_press_timestamps = {
            'shift': 0,
            'ctrl': 0,
            'esc': 0
        }
        self.key_first_press = {
            'shift': True,
            'ctrl': True,
            'esc': True
        }
        
        # 热键配置
        self.hotkey_config = [
            ('alt+7', self.move_window_to_corner, ('top_left',)),
            ('alt+8', self.move_window_to_corner, ('top_center',)),
            ('alt+9', self.move_window_to_corner, ('top_right',)),
            ('alt+4', self.move_window_to_corner, ('middle_left',)),
            ('alt+5', self.move_window_to_corner, ('center',)),
            ('alt+6', self.move_window_to_corner, ('middle_right',)),
            ('alt+1', self.move_window_to_corner, ('bottom_left',)),
            ('alt+2', self.move_window_to_corner, ('bottom_center',)),
            ('alt+3', self.move_window_to_corner, ('bottom_right',)),
            ('alt+left', self.move_window_horizontally, 'left'),
            ('alt+right', self.move_window_horizontally, 'right'),
            ('alt+up', self.move_window_vertically, 'up'),
            ('alt+down', self.move_window_vertically, 'down'),
        ]
        
        # 鼠标监听器
        self.mouse_listener = None
        self.registered_hotkeys = []
        self.lock = threading.Lock()  # 添加线程锁
        self._is_processing = False  # 防止重复处理
        
        # 注册Windows消息处理函数
        self._register_windows_hook()

    def _register_windows_hook(self):
        """注册Windows消息钩子，处理窗口消息"""
        # 这里可以添加更完善的Windows消息处理
        pass

    def get_screen_size(self):
        """获取屏幕分辨率"""
        return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

    def get_window_info(self, hwnd=None):
        """获取当前窗口信息，增加错误处理"""
        hwnd = hwnd or win32gui.GetForegroundWindow()
        if not hwnd:
            return None
        
        try:
            title = win32gui.GetWindowText(hwnd)
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]
            process = psutil.Process(pid)
            path = process.exe()
        except Exception as e:
            print(f"获取窗口信息失败: {str(e)}")
            return None
        
        return {
            "hwnd": hwnd,
            "title": title,
            "width": right - left,
            "height": bottom - top,
            "left": left,
            "top": top,
            "path": path
        }

    def move_window(self, hwnd, x, y):
        """移动窗口"""
        try:
            win32gui.SetWindowPos(hwnd, None, x, y, 0, 0, win32con.SWP_NOSIZE)
        except Exception as e:
            print(f"移动窗口失败: {str(e)}")

    def scale_window(self, hwnd, scale_factor, maintain_position=True):
        """缩放窗口（支持保持位置）"""
        info = self.get_window_info(hwnd)
        if not info:
            return
        
        screen_width, screen_height = self.get_screen_size()
        new_width = max(100, int(info["width"] * (1 + scale_factor)))
        new_height = max(60, int(info["height"] * (1 + scale_factor)))
        
        new_width = min(new_width, screen_width)
        new_height = min(new_height, screen_height)
        
        if maintain_position:
            x = (screen_width - new_width) // 2
            y = (screen_height - new_height) // 2
        else:
            x, y = info["left"], info["top"]
        
        try:
            win32gui.SetWindowPos(hwnd, None, x, y, new_width, new_height, win32con.SWP_NOZORDER)
        except Exception as e:
            print(f"缩放窗口失败: {str(e)}")

    def scale_dimension(self, hwnd, is_vertical, scale_factor):
        """按维度缩放（宽度或高度）"""
        info = self.get_window_info(hwnd)
        if not info:
            return
        
        screen_width, screen_height = self.get_screen_size()
        try:
            if is_vertical:
                new_height = max(60, int(info["height"] * (1 + scale_factor)))
                new_height = min(new_height, screen_height)
                y = (screen_height - new_height) // 2
                win32gui.SetWindowPos(hwnd, None, info["left"], y, info["width"], new_height, win32con.SWP_NOZORDER)
            else:
                new_width = max(100, int(info["width"] * (1 + scale_factor)))
                new_width = min(new_width, screen_width)
                x = (screen_width - new_width) // 2
                win32gui.SetWindowPos(hwnd, None, x, info["top"], new_width, info["height"], win32con.SWP_NOZORDER)
        except Exception as e:
            print(f"按维度缩放窗口失败: {str(e)}")

    def move_window_to_corner(self, position):
        """将窗口移动到指定屏幕位置"""
        info = self.get_window_info()
        if not info:
            return
        
        screen_width, screen_height = self.get_screen_size()
        x, y = 0, 0
        
        if position == 'top_left':
            x, y = 0, 0
        elif position == 'top_center':
            x = (screen_width - info["width"]) // 2
            y = 0
        elif position == 'top_right':
            x = screen_width - info["width"]
            y = 0
        elif position == 'middle_left':
            x = 0
            y = (screen_height - info["height"]) // 2
        elif position == 'center':
            x = (screen_width - info["width"]) // 2
            y = (screen_height - info["height"]) // 2
        elif position == 'middle_right':
            x = screen_width - info["width"]
            y = (screen_height - info["height"]) // 2
        elif position == 'bottom_left':
            x = 0
            y = screen_height - info["height"]
        elif position == 'bottom_center':
            x = (screen_width - info["width"]) // 2
            y = screen_height - info["height"]
        elif position == 'bottom_right':
            x = screen_width - info["width"]
            y = screen_height - info["height"]
        
        self.move_window(info["hwnd"], x, y)
        self.log_action(f"移动到{position}", info)

    def move_window_horizontally(self, direction):
        """水平移动窗口（左/右边缘）"""
        info = self.get_window_info()
        if not info:
            return
        
        screen_width = self.get_screen_size()[0]
        x = 0 if direction == 'left' else screen_width - info["width"]
        self.move_window(info["hwnd"], x, info["top"])
        self.log_action(f"水平移动到{direction}", info)

    def move_window_vertically(self, direction):
        """垂直移动窗口（上/下边缘）"""
        info = self.get_window_info()
        if not info:
            return
        
        screen_height = self.get_screen_size()[1]
        y = 0 if direction == 'up' else screen_height - info["height"]
        self.move_window(info["hwnd"], info["left"], y)
        self.log_action(f"垂直移动到{direction}", info)

    def log_action(self, action, info=None):
        """记录操作日志，增加默认值处理"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info = info or {}
        left = info.get("left", "?")
        top = info.get("top", "?")
        width = info.get("width", "?")
        height = info.get("height", "?")
        print(f"{timestamp} {action} - 位置({left}, {top}), 大小({width}x{height})")

    def show_notification(self, title, message):
        """显示通知"""
        try:
            self.toaster.show_toast(title, message, duration=self.notification_duration, threaded=True)
        except Exception as e:
            print(f"显示通知失败: {str(e)}")

    def handle_key_double_press(self, key):
        """处理按键双击"""
        with self.lock:
            if self._is_processing:
                return
            self._is_processing = True
            
            try:
                if key == 'shift':
                    self.shift_vertical_move = not self.shift_vertical_move
                    self.show_notification("Shift模式切换", "垂直移动" if self.shift_vertical_move else "水平移动")
                elif key == 'ctrl':
                    self.ctrl_vertical_scale = not self.ctrl_vertical_scale
                    self.show_notification("Ctrl模式切换", "高度缩放" if self.ctrl_vertical_scale else "宽度缩放")
            finally:
                self._is_processing = False

    def on_key_press(self, key_name):
        """按键按下处理，增加防抖"""
        with self.lock:
            if self._is_processing:
                return
            self._is_processing = True
            
            try:
                current_time = time.time()
                
                # 防抖处理
                if key_name == 'esc' and current_time - self.key_press_timestamps[key_name] < 0.3:
                    return
                    
                key_state = self.key_first_press[key_name]
                
                if key_state:
                    self.key_press_timestamps[key_name] = current_time
                    self.key_first_press[key_name] = False
                else:
                    if current_time - self.key_press_timestamps[key_name] < self.double_click_timeout:
                        self.handle_key_double_press(key_name)
                        self.reset_key_state(key_name)
            finally:
                self._is_processing = False

    def on_key_release(self, key_name):
        """按键释放处理"""
        with self.lock:
            self.reset_key_state(key_name)

    def reset_key_state(self, key_name):
        """重置按键状态"""
        self.key_first_press[key_name] = True
        self.key_press_timestamps[key_name] = 0

    def on_mouse_scroll(self, x, y, dx, dy):
        """鼠标滚轮处理"""
        if not self.listening_enabled:
            return
        
        info = self.get_window_info()
        if not info:
            return
        
        scale_factor = self.scale_step if dy > 0 else -self.scale_step
        
        if keyboard.is_pressed('alt'):
            self.scale_window(info["hwnd"], scale_factor)
            self.log_action("等比例缩放", info)
        elif keyboard.is_pressed('shift'):
            delta = dy * self.move_step
            if self.shift_vertical_move:
                self.move_window(info["hwnd"], info["left"], info["top"] - delta)
                self.log_action("垂直移动", info)
            else:
                self.move_window(info["hwnd"], info["left"] - delta, info["top"])
                self.log_action("水平移动", info)
        elif keyboard.is_pressed('ctrl'):
            if self.ctrl_vertical_scale:
                self.scale_dimension(info["hwnd"], True, scale_factor)
                self.log_action("高度缩放", info)
            else:
                self.scale_dimension(info["hwnd"], False, scale_factor)
                self.log_action("宽度缩放", info)

    def on_mouse_click(self, x, y, button, pressed):
        """鼠标点击处理"""
        if not pressed:
            return
        
        if button == mouse.Button.middle:
            if keyboard.is_pressed('shift'):
                self.handle_key_double_press('shift')
            elif keyboard.is_pressed('ctrl'):
                self.handle_key_double_press('ctrl')

    def toggle_listening(self):
        """切换监听状态，增加线程保护"""
        with self.lock:
            if self._is_processing:
                return
            self._is_processing = True
            
            try:
                current_time = time.time()
                if current_time - self.last_esc_switch_time < self.anti_shake_duration:
                    return
                
                self.listening_enabled = not self.listening_enabled
                message = "按键监听已启用 ✔" if self.listening_enabled else "按键监听已禁用 ❌"
                
                info = self.get_window_info()
                self.log_action(message, info)
                self.show_notification("监听状态", message)
                
                self.manage_listeners()
                self.last_esc_switch_time = current_time
            finally:
                self._is_processing = False

    def manage_listeners(self):
        """管理监听组件"""
        with self.lock:
            if self._is_processing:
                return
            self._is_processing = True
            
            try:
                if self.listening_enabled:
                    self.register_hotkeys()
                    if not self.mouse_listener or not self.mouse_listener.is_alive():
                        self.mouse_listener = mouse.Listener(
                            on_click=self.on_mouse_click,
                            on_scroll=self.on_mouse_scroll
                        )
                        self.mouse_listener.start()
                else:
                    self.unregister_hotkeys()
                    if self.mouse_listener and self.mouse_listener.is_alive():
                        self.mouse_listener.stop()
            finally:
                self._is_processing = False

    def register_hotkeys(self):
        """注册热键"""
        with self.lock:
            self.unregister_hotkeys()  # 先注销旧热键
            for hotkey, func, args in self.hotkey_config:
                try:
                    keyboard.add_hotkey(hotkey, func, args=args)
                    self.registered_hotkeys.append(hotkey)
                except Exception as e:
                    print(f"注册热键失败: {hotkey}, 错误: {str(e)}")

    def unregister_hotkeys(self):
        """注销热键"""
        with self.lock:
            for hotkey in self.registered_hotkeys:
                keyboard.remove_hotkey(hotkey)
            self.registered_hotkeys.clear()

    def start(self):
        """启动管理器"""
        # 注册Esc键处理
        keyboard.on_press_key('esc', lambda _: self.on_key_press('esc'))
        keyboard.on_release_key('esc', lambda _: self.on_key_release('esc'))
        keyboard.add_hotkey('esc', self.toggle_listening)  # 双击Esc触发切换
        
        print("窗口管理器已启动，按Alt+数字键快速定位窗口，按Esc双击切换监听状态")
        keyboard.wait()

if __name__ == "__main__":
    manager = WindowManager()
    manager.start()