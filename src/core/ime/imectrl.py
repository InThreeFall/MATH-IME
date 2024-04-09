from core.state import State
from pynput import keyboard
from core.ime.corpusdata import Word,Corpus
from core.ime.searchalgorithm import IME

class WaitWord:
    """
    WaitWord\n等待词类
    description:等待词类，用于存储搜索到的词和分数，目前与Word类相同，并没使用score属性,计划删除
    """
    def __init__(self,word:Word,score:int):
        self.word = word
        self.score = score

class ImeCtrl:
    """
    ImeCtrl\n输入法控制类
    description:输入法控制类，用于控制输入法的各种操作，目前是静态类，计划改为单例模式
    """
    IME_STATE_LOW = "小写"
    IME_STATE_HIGH = "大写"
    IME_STATE_CLOSE = "关闭"

    input_word = '' #字符串
    wait_words = [] #word类的列表
    show_words = [] #word类的列表
    pre_output:Word = None #word
    corpus = Corpus()
    showCandidatePage = 0
    corpusList = corpus.query_by_type(State.now_ime)
    ime_search = IME(corpusList)
    __on_wait_count = 0

    @staticmethod
    def setWaitCount(count:int):
        ImeCtrl.__on_wait_count = count
    
    @staticmethod
    def isWaitCountAndDump():
        if ImeCtrl.__on_wait_count == 0:
            return False
        else:
            ImeCtrl.__on_wait_count -= 1
            return True

    @staticmethod
    def switch_ime():
        State.switch_ime()
        ImeCtrl.corpusList = ImeCtrl.corpus.query_by_type(State.now_ime)
        ImeCtrl.ime_search = IME(ImeCtrl.corpusList)
        ImeCtrl.clear()

    @staticmethod
    def switch_state():
        State.switch_state()
        ImeCtrl.ime_search = IME(ImeCtrl.corpusList)
        ImeCtrl.clear()
    @staticmethod
    def switch_stateByState(state):
        State.switch_stateByState(state)
        ImeCtrl.ime_search = IME(ImeCtrl.corpusList)
        ImeCtrl.clear()

    @staticmethod
    def updateIME():
        State.switch_ime()
        ImeCtrl.corpusList = ImeCtrl.corpus.query_by_type(State.now_ime)
        ImeCtrl.ime_search = IME(ImeCtrl.corpusList)
        ImeCtrl.clear()

    @staticmethod
    def clear():
        ImeCtrl.input_word = ''
        ImeCtrl.wait_words = []
        ImeCtrl.pre_output = ''
        ImeCtrl.show_words = []
    
    @staticmethod
    def append_input_word(word):
        ImeCtrl.input_word += word
        ImeCtrl.turninput2wait()

    @staticmethod
    def pop_input_word():
        ImeCtrl.input_word = ImeCtrl.input_word[:-1]
        if len(ImeCtrl.input_word) == 0:
            ImeCtrl.clear()
        ImeCtrl.turninput2wait()

    @staticmethod
    def turninput2wait():
        wait_words = ImeCtrl.ime_search.getScoresByX(ImeCtrl.input_word)
        for (score,word) in wait_words:
            ImeCtrl.wait_words.append(WaitWord(word,score))
        
        #show_words是前5个
        if len(ImeCtrl.wait_words) > 5:
            ImeCtrl.show_words = ImeCtrl.wait_words[:5]
        else:
            ImeCtrl.show_words = ImeCtrl.wait_words
        if len(ImeCtrl.wait_words) == 0:
            ImeCtrl.pre_output = ''
        else:
            ImeCtrl.pre_output = ImeCtrl.wait_words[0]

    @staticmethod
    def output():
        if ImeCtrl.pre_output == None:
            return
        ctrl = keyboard.Controller()
        if State.now_ime_state == ImeCtrl.IME_STATE_LOW:
            ImeCtrl.setWaitCount(len(ImeCtrl.pre_output.word.true_word_low))
            ctrl.type(ImeCtrl.pre_output.word.true_word_low)
        elif State.now_ime_state == ImeCtrl.IME_STATE_HIGH:
            ImeCtrl.setWaitCount(len(ImeCtrl.pre_output.word.true_word_high))
            ctrl.type(ImeCtrl.pre_output.word.true_word_high)
        ImeCtrl.clear()

    @staticmethod
    def output_input():
        ImeCtrl.setWaitCount(len(ImeCtrl.input_word))
        ctrl = keyboard.Controller()
        ctrl.type(ImeCtrl.input_word)
        ImeCtrl.clear()

    @staticmethod
    def move_up():
        #点击向上的箭头时，如果pre_output是第一个词，则不做任何操作
        #否则，将pre_output设置为前一个词，如果当前页是第一页，则不做任何操作
        #否则，当pre_output是show_words的第一个词时，将当前页设置为前一页
        if len(ImeCtrl.wait_words) == 0:
            return
        if ImeCtrl.pre_output == ImeCtrl.wait_words[0]:
            return
        for i in range(len(ImeCtrl.wait_words)):
            if ImeCtrl.pre_output == ImeCtrl.wait_words[i]:
                ImeCtrl.pre_output = ImeCtrl.wait_words[i-1]
                break
        if ImeCtrl.pre_output in ImeCtrl.show_words:
            return
        if ImeCtrl.showCandidatePage == 0:
            return
        ImeCtrl.showCandidatePage -= 1
        ImeCtrl.show_words = ImeCtrl.wait_words[ImeCtrl.showCandidatePage*5:ImeCtrl.showCandidatePage*5+5]


    @staticmethod
    def move_down():
        #点击向下的箭头时，如果pre_output是最后一个词，则不做任何操作
        #否则，将pre_output设置为后一个词，如果当前页是最后一页，则不做任何操作
        #否则，当pre_output是show_words的最后一个词时，将当前页设置为后一页
        if len(ImeCtrl.wait_words) == 0:
            return
        if ImeCtrl.pre_output == ImeCtrl.wait_words[-1]:
            return
        for i in range(len(ImeCtrl.wait_words)):
            if ImeCtrl.pre_output == ImeCtrl.wait_words[i]:
                ImeCtrl.pre_output = ImeCtrl.wait_words[i+1]
                break
        if ImeCtrl.pre_output in ImeCtrl.show_words:
            return
        if ImeCtrl.showCandidatePage == len(ImeCtrl.wait_words)//5:
            return
        ImeCtrl.showCandidatePage += 1
        ImeCtrl.show_words = ImeCtrl.wait_words[ImeCtrl.showCandidatePage*5:ImeCtrl.showCandidatePage*5+5]
        
