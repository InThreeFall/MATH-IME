from PyQt5.QtWidgets import QLineEdit,QLabel,QMessageBox, QWidget
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QDialog, QMenu
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

from core.state import State
from core.ime.corpusdata import Corpus,Word

class EditWindow(QWidget):
    """
    EditWindow class\n
    This class is used to create a window for editing the configuration of the input method.\n
    编辑窗口类\n
    用于创建一个窗口，用于编辑输入法的配置
    """
    #初始化
    def __init__(self):
        """
        Initialize the window\n
        初始化窗口
        """
        super().__init__()
        self.__connectSql()
        self.__setWindowUi()
        self.__createComboBox(True)
        self.__createButton()
        self.__createTable(True)
        self.__layout()

    #总窗口UI设置
    def __setWindowUi(self):
        """set the window UI\n设置窗口UI"""
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus)
        self.setWindowTitle("编辑")
        self.resize(1200, 600)

    #创建控件
    def __createTable(self,is_first = False):
        """create table\n创建表格"""
        data = self.__getDataForTable()
        if is_first:
            self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setRowCount(len(data))
        self.table.setHorizontalHeaderLabels(["显示-大写", "显示-小写", "拼音","输出-大写", "输出-小写","ID","类别"])
        for i in range(len(data)):
            for j in range(len(data[i])):
                item = QTableWidgetItem(data[i][j])
                item.setTextAlignment(Qt.AlignCenter)  # 设置内容水平居中对齐
                self.table.setItem(i, j, item)
                if j == 5:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table.setColumnHidden(j, True)
                elif j == 6:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table.setColumnHidden(j, True)
                    # 调整列宽以填充空白
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置表格水平对齐方式为居中
        self.table.horizontalHeaderItem(0).setTextAlignment(1)
        # 设置表格大小策略
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #设置表格为不可编辑
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        #设置表格右键弹出菜单
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.onRightClickForTable)

    def __createComboBox(self,is_first = False):
        """create combobox\n创建下拉框"""
        if is_first:
            self.combobox = QComboBox()
        type_list = self.__getTypeList()
        for i in range(len(type_list)):
            self.combobox.addItem(type_list[i])
        self.combobox.currentIndexChanged.connect(self.onChooseType)

    def __createButton(self):
        """create button\n创建按钮"""
        add_button = QPushButton("添加新语言")
        add_button.clicked.connect(self.onAddType)
        self.add_button = add_button
        edit_button = QPushButton("编辑")
        edit_button.clicked.connect(self.onClickEditButton)
        self.edit_button = edit_button
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.onCancel)
        self.cancel_button = cancel_button

    # 以下为槽函数
    def onAddType(self):
       """click the 'add new type' button\n点击'添加新语言'按钮"""
       self.__openNewTypeDialog()   

    def onClickEditButton(self):
        """click the 'edit' button\n点击'编辑'按钮"""
        if self.__isEditState():#之前已经是编辑状态，点击后应该保存
            self.__setEditButtonEditStyle()
            self.__saveData()
        else:
            self.__setEditButtonSaveStyle()

    def onCancel(self):
        """click the 'cancel' button\n点击'取消'按钮"""
        self.__createTable()
        self.__setEditButtonEditStyle()
        self.hide()

    def onChooseType(self):
        """choose the type\n选择类型"""
        self.__createTable()

    #布局
    def __layout(self):
        """layout\n布局"""
        layout = QVBoxLayout()
        layout.addWidget(self.combobox)
        layout.addWidget(self.add_button)
        layout.addWidget(self.table)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.edit_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    #获取数据
    def __connectSql(self):
        """connect to the database\n连接数据库"""
        self.corpus = Corpus()

    def __getCorpusList(self):
        """
        Get the corpus list\n
        获取词库列表
        """
        corpus_list = self.corpus.query_by_type(self.combobox.currentText())
        if corpus_list is None:
            corpus_list = []
        return corpus_list
    
    def __getDataForTable(self):
        """
        Get the data for the table\n
        获取将要填充表格的数据
        """
        corpus_list = self.__getCorpusList()
        data = []
        dataItem = []
        for i in range(len(corpus_list)):
            dataItem.append(corpus_list[i].show_word_high)
            dataItem.append(corpus_list[i].show_word_low)
            dataItem.append(corpus_list[i].pinyin)
            dataItem.append(corpus_list[i].true_word_high)
            dataItem.append(corpus_list[i].true_word_low)
            dataItem.append(str(corpus_list[i].id))
            dataItem.append(corpus_list[i].ime_type)
            data.append(dataItem)
            dataItem = []
        return data
    
    def __getTypeList(self):
        """Get the type list\n获取类型列表"""
        self.type_list = self.corpus.query_typeList()
        if self.type_list is None:
            self.type_list = []
        return self.type_list
    
    #控件交互
    def __isEditState(self):
        """check if the state is 'edit'\n检查是否为编辑状态"""
        return self.edit_button.text() == "保存" #如果按钮文字为"保存"则处于是编辑状态
    
    def __setEditButtonSaveStyle(self):
        """set the button to 'save' style\n设置按钮为'保存'样式"""
        self.edit_button.setText("保存")
        self.table.setEditTriggers(QTableWidget.DoubleClicked)
        self.table.setStyleSheet("background-color: rgb(240, 240, 240);")
    
    def __setEditButtonEditStyle(self):
        """set the button to 'edit' style\n设置按钮为'编辑'样式"""
        self.edit_button.setText("编辑")
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("background-color: rgb(255, 255, 255);")

    def __createMenuByRightClick(self,row_num,pos):
        """create the menu by right click\n右键触发的创建菜单"""
        menu = QMenu()
        menu.addAction("删除", lambda: self.onDeleteInMenu(row_num,menu))
        menu.addAction("插入", lambda: self.onInsertInMenu(row_num,menu))
        menu.exec_(pos)

    def __getDataByTableRowNum(self,row_num):
        """get the data by the row number\n通过行号获取数据"""
        return self.__turnTable2WordList()[row_num]

    def onRightClickForTable(self):
        """right click on the table\n表格右键"""
        if not self.__isEditState():#如果不是编辑状态则不允许右键操作 
            return
        #获取当前行
        row_num = self.table.currentRow()
        #获取鼠标位置
        pos = QCursor.pos()
        #创建菜单
        self.__createMenuByRightClick(row_num,pos)

    delete_list = []
    def __deleteTableRow(self,row_num):
        """delete the row of the table\n删除表格行"""
        if self.delete_list is None:
            self.delete_list = []
        self.delete_list.append(self.__getDataByTableRowNum(row_num))
        self.table.removeRow(row_num)

    #与数据库交互
    def __turnTable2WordList(self):
        """turn the table data to the word list\n将表格数据转换为词条列表"""
        table_data = []
        for i in range(self.table.rowCount()):
            data = []
            for j in range(self.table.columnCount()):
                if self.table.item(i, j) is not None:
                    data.append(self.table.item(i, j).text())
            table_data.append(data)
        return table_data
    
    def onDeleteInMenu(self,row_num,menu):
        """delete the row\n删除行"""
        self.__deleteTableRow(row_num)
        menu.close()
    
    def onInsertInMenu(self,row_num,menu):
        """insert the row\n插入行"""
        data = ["","","","","","",self.combobox.currentText()]
        self.table.insertRow(row_num+1)
        for i in range(len(data)):
            item = QTableWidgetItem(data[i])
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_num+1, i, item)
        menu.close()

    def __addData2Sql(self):
        """add the data to the database\n添加数据到数据库"""
        table_data = self.__turnTable2WordList()
        for data in table_data:
            if data[1]=="" or data[0]=="" or data[3]=="" or data[4]=="" or data[2]=="":
                #弹窗提示
                QMessageBox.information(self, "提示", "请填写完整,如果该字母没有对于的大写，请将小写复制到大写处\n"+
                                        "出错行数："+str(table_data.index(data)+1))
                continue
            word = Word(data[5], data[1], data[0], data[4], data[3], data[2], data[6])
            if self.corpus.checkIsExist(word):
                self.corpus.update(word)
            else:
                self.corpus.add(word)

    def __deleteData2Sql(self):
        """delete the data from the database\n从数据库删除数据"""
        if self.delete_list is None:
            self.delete_list = []
        for data in self.delete_list:
            word = Word(data[5], data[1], data[0], data[4], data[3], data[2], data[6])
            self.corpus.delete(word.id)
        self.delete_list = []

    def __saveData(self):
        """save the data\n保存数据"""
        self.__addData2Sql()
        self.__deleteData2Sql()

        self.__createTable()
        self.__createComboBox()

    #与外部交互
    def __openNewTypeDialog(self):
        """open the 'new type' dialog\n打开'创建新类型'对话框"""
        newdialog = NewTypeDialog(self.updateType)
        newdialog.exec_()

    def updateType(self):
        """update the type this method is for NewTypeDialog \n更新类型 给外部调用"""
        self.__createComboBox()
        self.__createTable()

class NewTypeDialog(QDialog):
    """
    NewTypeDialog class\n
    This class is used to create a dialog for adding a new type.\n
    新类型对话框类,用于创建一个对话框，用于添加新类型
    """
    def __setWindowUi(self):
        """set the window UI\n设置窗口UI"""
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus|Qt.SplashScreen)
        self.setWindowTitle("添加")
    def __setCallback(self,updateTypeCallback):
        """set the callback function\n设置回调函数"""
        self.updateTypeCallback = updateTypeCallback
    def __createInput(self):
        """create the input\n创建输入框"""
        self.label0 = QLabel("类型名称:")
        self.imeType = QLineEdit()
        self.label1 = QLabel("下面请填写一个示范词条")
        self.label2 = QLabel("显示-大写:")
        self.show_word_high = QLineEdit()
        self.label3 = QLabel("显示-小写:")
        self.show_word_low = QLineEdit()
        self.label4 = QLabel("拼音:")
        self.pinyin = QLineEdit()
        self.label5 = QLabel("输出-大写:")
        self.true_word_high = QLineEdit()
        self.label6 = QLabel("输出-小写:")
        self.true_word_low = QLineEdit()
    def __createButton(self):
        #创建按钮
        self.makeSureBt = QPushButton("确定")
        self.makeSureBt.clicked.connect(self.onMakeSureBtClick)
        self.cancelBt = QPushButton("取消")
        self.cancelBt.clicked.connect(self.onCancelBtClick)
    # 布局
    def __layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.label0)
        layout.addWidget(self.imeType)
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(self.show_word_high)
        layout.addWidget(self.label3)
        layout.addWidget(self.show_word_low)
        layout.addWidget(self.label4)
        layout.addWidget(self.pinyin)
        layout.addWidget(self.label5)
        layout.addWidget(self.true_word_high)
        layout.addWidget(self.label6)
        layout.addWidget(self.true_word_low)
        layout.addWidget(self.makeSureBt)
        layout.addWidget(self.cancelBt)
        self.setLayout(layout)
    def __init__(self,updateTypeCallback):
        """
        Initialize the dialog\n
        初始化对话框

        Args:
            updateTypeCallback: The callback function for updating the type\n
            updateTypeCallback: 更新类型的回调函数
        """
        super().__init__()
        self.__setWindowUi()
        self.__setCallback(updateTypeCallback)
        self.__createInput()
        self.__createButton()
        self.__layout()

    def __saveData(self):
        """save the data\n保存数据"""
        word = Word(None,
                     self.show_word_low.text(), 
                     self.show_word_high.text(), 
                     self.true_word_low.text(), 
                     self.true_word_high.text(),
                        self.pinyin.text(), 
                       self.imeType.text())
        corpus = Corpus()
        corpus.add(word)
        #提示添加成功
        QMessageBox.information(self, "提示", "添加成功")
        self.updateTypeCallback()
        State.update_ime_list()
        self.close()

    def onMakeSureBtClick(self):
        """click the 'make sure' button\n点击'确定'按钮"""
        self.__saveData()

    def onCancelBtClick(self):
        """click the 'cancel' button\n点击'取消'按钮"""
        self.close()
