from core.ime.corpusdata import Corpus
import core.ime.keyboard as keyboardmanager
def onStart():
    """
    数据库初始化
    """
    corpus = Corpus()
    corpus.in_start()

    """
    键盘管理开启
    """
    keyboardmanager.onStart()
