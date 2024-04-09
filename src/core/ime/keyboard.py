from pynput import keyboard
from utils import keyutils
from core.ime.imectrl import ImeCtrl
import const.static as static
from core.state import State
from const.config import getHotKey
keyList = []
def win32KeyMapping(msg,data):
    global keyList
    if State.now_ime_state == State.IME_STATE_CLOSE:
        return

    if keyutils.is_on_press(msg):
        print(data.vkCode,chr(data.vkCode))
        if ImeCtrl.isWaitCountAndDump():
            if len(keyList) > 0:
                keyList.pop()
            return
        #如果是大小写切换键
        elif 20 == data.vkCode:
            if State.now_ime_state == State.IME_STATE_LOW:
                State.switch_stateByState(State.IME_STATE_HIGH)
            else:
                State.switch_stateByState(State.IME_STATE_LOW)
            return
        #如果是按下事件
        if len(keyList) > 0:
            return
        keyList.append(data.vkCode)
        #判断是否是字母
        if keyutils.is_letter(data.vkCode):
            ImeCtrl.append_input_word(chr(data.vkCode).lower())
            if kc!=None:
                if len(keyList) > 0:
                    keyList.pop()
                kc.suppress_event()
        #如果没有输入字母就不走下面的流程
        elif len(ImeCtrl.input_word) == 0:
            return
        #如果是数字键
        elif keyutils.is_number(data.vkCode):
            if len(ImeCtrl.show_words)>=data.vkCode-48:
                ImeCtrl.pre_output = ImeCtrl.show_words[data.vkCode-49]
                ImeCtrl.output()
                ImeCtrl.clear()
                if kc!=None:
                    if len(keyList) > 0:
                        keyList.pop()
                    kc.suppress_event()
                
        #如果是退格键
        elif keyutils.get_vk(keyboard.Key.backspace) == data.vkCode:
            ImeCtrl.pop_input_word()
            if kc!=None:
                if len(keyList) > 0:
                    keyList.pop()
                kc.suppress_event()
        #如果是退出键
        elif keyutils.get_vk(keyboard.Key.esc) == data.vkCode:
            ImeCtrl.clear()
            if kc!=None:
                if len(keyList) > 0:
                    keyList.pop()
                kc.suppress_event()
            
        #如果是回车键
        elif keyutils.get_vk(keyboard.Key.enter) == data.vkCode:
            ImeCtrl.output()
            ImeCtrl.clear()
            if kc!=None:
                if len(keyList) > 0:
                    keyList.pop()
                kc.suppress_event()
        #如果是空格键
        elif keyutils.get_vk(keyboard.Key.space) == data.vkCode:
            ImeCtrl.output_input()
            ImeCtrl.clear()
            if kc!=None:
                if len(keyList) > 0:
                    keyList.pop()
                kc.suppress_event()

        #如果是上键
        elif keyutils.get_vk(keyboard.Key.up) == data.vkCode:
            ImeCtrl.move_up()
            if kc!=None:
                if len(keyList) > 0:
                    keyList.pop()
                kc.suppress_event()
        #如果是下键
        elif keyutils.get_vk(keyboard.Key.down) == data.vkCode:
            ImeCtrl.move_down()
            if kc!=None:
                if len(keyList) > 0:
                    keyList.pop()
                kc.suppress_event()
    else:
        for i in range(len(keyList)):
            if keyList[i] == data.vkCode:
                keyList.pop(i)
                break



kc = None
def onStart():
    global kc
    kc = keyboard.Listener(win32_event_filter=win32KeyMapping)
    kc.start()
    
    #特殊键
    #从文件中读取热键配置
    #如果没有配置文件就使用默认配置

    hotkeySwitchIME = getHotKey('hotkey-imeSwitch')
    hotkeySwitchState = getHotKey('hotkey-imeStateSwitch')
    globalListener = keyboard.GlobalHotKeys({
        hotkeySwitchIME: ImeCtrl.switch_ime,
        hotkeySwitchState: ImeCtrl.switch_state
    })
    globalListener.start()


