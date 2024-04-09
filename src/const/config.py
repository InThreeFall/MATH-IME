import const.static as static
import json
def isFirst():
    """
    Description: Check if the program is running for the first time\n
    检查程序是否第一次运行

    Returns:
        bool: True if the program is running for the first time, False otherwise\n
        如果程序第一次运行则返回True，否则返回False
    """
    with open(static.CONFIG_PATH, 'r') as f:
        config = json.load(f)
        return config['isFirstRun']
    
def setFirst(isFirstRun):
    """
    Description: Set the program to run for the first time\n
    设置程序是否是第一次运行

    Args:
         bool: True or False\n
    """
    with open(static.CONFIG_PATH, 'r') as f:
        config = json.load(f)
        config['isFirstRun'] = isFirstRun
    with open(static.CONFIG_PATH, 'w') as f:
        json.dump(config, f)

def getHotKey(key):
    """
    Description: Get the hotkey for the specified function from the config file\n
    从配置文件中获取指定功能的热键

    Args:
        key (str):such as "hotkey-imeSwitch" or "hotkey-imeStateSwitch" \n
        例如："hotkey-imeSwitch" 或 "hotkey-imeStateSwitch"
    Returns:
        str : The hotkey from "pynput" library format\n
        从 "pynput" 库格式的热键
    """
    with open(static.CONFIG_PATH, 'r') as f:
        config = json.load(f)
        return config[key]
