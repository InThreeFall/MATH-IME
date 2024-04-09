from __future__ import unicode_literals, absolute_import
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime,create_engine
from sqlalchemy.orm import sessionmaker
from const import static
from const.config import isFirst,setFirst
ModelBase = declarative_base() #<-元类
class CorpusTable(ModelBase):
    """
    CorpusTable\n
    词库表\n
    description:使用sqlalchemy创建词库表\n
    """
    __tablename__ = "corpus"
    id = Column(Integer, primary_key=True)
    show_word_low = Column(String(255)) #utf-8或者url 在输入法显示的文字
    show_word_high = Column(String(255)) #utf-8或者url 在输入法显示的文字
    true_word_low = Column(String(255)) #打印出来的文字
    true_word_high = Column(String(255)) #打印出来的文字
    ime_type = Column(String(255)) #输入法类型
    pinyin = Column(String(255))

class Word():
    """
    Word\n
    单词类\n
    description:词库表的实体类\n

    """
    def __init__(self,id, show_word_low,show_word_high, true_word_low,true_word_high, pinyin,ime_type):
        self.id = id
        self.show_word_low = show_word_low
        self.show_word_high = show_word_high
        self.true_word_low = true_word_low
        self.true_word_high = true_word_high
        self.pinyin = pinyin
        self.ime_type = ime_type

class Corpus():
    """
    Corpus\n
    词库的通信类\n
    description:词库的通信类，提供增删改查的方法\n
    warning:命名错误，应该是CorpusDao\n
    """
    def __init__(self):
        # 创建数据库引擎
        
        self.engine = create_engine(static.CORPUS_PATH, echo=True)
        # 创建数据表
        ModelBase.metadata.create_all(self.engine)
        # 创建一个会话
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def in_start(self):
        if not isFirst():
            return
    
        #读取csv文件
        with open(static.PRE_DATA_PATH, 'r', encoding='utf-8') as f:
            #去掉第一行
            for line in f:
                print(line)
                line = line.strip()
                if not line:
                    continue
                show_word_low,show_word_high, pinyin, true_word_low,true_word_high, ime_type = line.split(',')
                corpus = CorpusTable(show_word_low = show_word_low,
                                     show_word_high = show_word_high,
                                        true_word_low = true_word_low,
                                        true_word_high = true_word_high,
                                      pinyin = pinyin,
                                      ime_type = ime_type)
                if self.checkIsExist(Word(0, show_word_low,show_word_high, true_word_low,true_word_high, pinyin, ime_type)): 
                    continue
                self.session.add(corpus)
            self.session.commit()
        #设置不是第一次运行
        setFirst(False)

    def checkIsExist(self, word: Word):
        corpus = self.session.query(CorpusTable).filter(CorpusTable.id == word.id).first()
                                    
        if corpus:
            return True
        return False
    
    def checkIsExistByShowWord(self, show_word_low):
        corpus = self.session.query(CorpusTable).filter(CorpusTable.show_word_low == show_word_low).first()
        if corpus:
            return True
        return False

    def add(self, word: Word):
        corpus = CorpusTable(show_word_low = word.show_word_low,show_word_high = word.show_word_high,
                                        true_word_low = word.true_word_low,
                                        true_word_high = word.true_word_high,
                                      pinyin = word.pinyin,
                                      ime_type = word.ime_type)

        self.session.add(corpus)
        self.session.commit()

    def delete(self, id):
        corpus = self.session.query(CorpusTable).filter(CorpusTable.id == id).first()
        self.session.delete(corpus)
        self.session.commit()

    def update(self, word: Word):
        corpus = self.session.query(CorpusTable).filter(CorpusTable.id == word.id).first()
        self.session.delete(corpus)
        corpus.show_word_low = word.show_word_low
        corpus.show_word_high = word.show_word_high
        corpus.true_word_low = word.true_word_low
        corpus.true_word_high = word.true_word_high
        corpus.pinyin = word.pinyin
        corpus.ime_type = word.ime_type
        #更新
        self.session.add(corpus)
        self.session.commit()

    def query(self, id):
        corpus = self.session.query(CorpusTable).filter(CorpusTable.id == id).first()
        return Word(corpus.id, corpus.show_word_low,corpus.show_word_high, corpus.true_word_low,corpus.true_word_high, corpus.pinyin)
    
    def query_all(self):
        corpus_list = self.session.query(CorpusTable).all()
        word_list = []
        for corpus in corpus_list:
            word_list.append(Word(corpus.id, corpus.show_word_low,corpus.show_word_high, corpus.true_word_low,corpus.true_word_high, corpus.pinyin,corpus.ime_type))
        return word_list
    
    def query_by_type(self, ime_type):
        corpus_list = self.session.query(CorpusTable).filter(CorpusTable.ime_type == ime_type).all()
        word_list = []
        for corpus in corpus_list:
            word_list.append(Word(corpus.id, corpus.show_word_low,corpus.show_word_high, corpus.true_word_low,corpus.true_word_high, corpus.pinyin,corpus.ime_type))
        return word_list

    def query_typeList(self):
        corpus_list = self.session.query(CorpusTable.ime_type).distinct().all()
        type_list = []
        for corpus in corpus_list:
            type_list.append(corpus.ime_type)
        return type_list
    def close(self):
        self.session.close()
    



