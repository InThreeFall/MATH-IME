import win32con # type: ignore
import pynput

def is_letter(key):
    return 65 <= key <= 90 or 97 <= key <= 122
def is_on_press(msg):
    if msg == win32con.WM_KEYDOWN:
        return True
    elif msg == win32con.WM_KEYUP:
        return False
    else:
        return None
def get_vk(key):
    if isinstance(key, pynput.keyboard.Key):
        return key.value.vk
    elif isinstance(key, pynput.keyboard._win32.KeyCode):
        return key.vk
    else:
        return None
#判断是否是数字键
def is_number(key):
    return 48<=key<=57

