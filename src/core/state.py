#状态
#目前的输入法 默认为希腊
from core.ime.corpusdata import Corpus
class State:
    """
    State\n
    状态类\n
    description:状态类，用于存储当前的输入法和状态\n
    warning:未来可能会改为单例模式而非静态类，因为静态类会比词库Dao优先初始化\n
    """
    IME_STATE_LOW = "小写"
    IME_STATE_HIGH = "大写"
    IME_STATE_CLOSE = "关闭"

    #从数据库中获得list
    corpus = Corpus()
    now_ime_list = corpus.query_typeList()
    if len(now_ime_list) == 0:
        now_ime_list = ["希腊"]
    now_ime = now_ime_list[0]

    now_ime_state = "关闭"
    now_ime_state_list = ["小写","大写","关闭"]

    @staticmethod
    def switch_ime():
        li = State.now_ime_list
        index = li.index(State.now_ime)
        length = len(li)
        index = (index+1)%length
        State.now_ime = li[index]

    @staticmethod
    def switch_state():
        li = State.now_ime_state_list
        index = li.index(State.now_ime_state)
        length = len(li)
        index = (index+1)%length
        State.now_ime_state = li[index]

    @staticmethod
    def switch_stateByState(state):
        State.now_ime_state = state

    @staticmethod
    def switch_imeByIme(ime):
        State.now_ime = ime

    @staticmethod
    def update_ime_list():
        State.now_ime_list = State.corpus.query_typeList()
        if len(State.now_ime_list) == 0:
            State.now_ime_list = ["希腊"]
        State.now_ime = State.now_ime_list[0]