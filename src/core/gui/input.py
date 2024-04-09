from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QCursor
from core.ime.imectrl import ImeCtrl
from core.state import State

class InputWin(QMainWindow):
    """
    Input tip window\n
    输入提示窗口
    """
    def __init__(self):
        super().__init__()
        self.__setWindowsUi()
        self.__createTipLabel()
        self.__createButton()
        self.__layout()
        self.pre_hidden = True

    def __setWindowsUi(self):
        """Set the window style\n设置窗口样式"""
        self.setFixedSize(500, 120)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus|Qt.SplashScreen)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setStyleSheet("background-color: rgba(255, 255, 255, 200); border-radius: 10px;")  # 设置背景色和圆角
        
    def __createTipLabel(self):
        """Create the tip label\n创建提示标签"""
        self.tipLabel = QLabel("候选词", self)
        font = self.tipLabel.font()
        font.setBold(True)
        font.setPointSize(16)
        self.tipLabel.setFont(font)
        self.tipLabel.setAlignment(Qt.AlignCenter)

    def __createButton(self):
        """Create button widget\n创建按钮部件"""
        #创建按钮部件
        self.button_layout = QHBoxLayout()
        #设背景颜色
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setAlignment(Qt.AlignCenter)
        self.button_layout.setSpacing(0)
        #创建按钮
        self.button_list = []
        self.tipLabel_list = []
        self.item_layout_list = []
        self.item_widget_list = []
        for i in range(5):
            #添加数字提示label
            #创建子布局
            item_widget = QWidget()
            #设置布局内为中央对齐
            item_layout = QHBoxLayout()
            #设置为中央对齐
            item_widget.setLayout(item_layout)
            label = QLabel(str(i+1), self)
            label.setFixedWidth(20)
            label.setAlignment(Qt.AlignCenter)
            font = label.font()
            font.setBold(True)
            font.setPointSize(16)
            label.setFont(font)
            self.tipLabel_list.append(label)
            item_layout.addWidget(label)
            #添加按钮
            btn = QPushButton("", self)
            btn.setFixedHeight(60)
            ##设置外边距为0
            btn.setContentsMargins(0, 0, 0, 0)
            #设按钮高度与窗口高度一致
            #设置字体大小
            font = btn.font()
            font.setPointSize(16)
            font.setBold(True)
            btn.setFont(font)
            self.button_list.append(btn)
            item_layout.addWidget(btn)
            #设置item_widget 背景颜色为白色
            self.item_widget_list.append(item_widget)
            self.button_layout.addWidget(item_widget)
            self.item_layout_list.append(item_layout)
        
        #设置按钮均分窗口的宽,高度与窗口高度一致
        for i in range(5):
            self.button_layout.setStretch(i, 1)
    
        #设置定时器，每隔一段时间更新状态
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.__updateState)
        self.timer.start(100)
        self.pos = QCursor.pos()
        self.__hidden()


    def __layout(self):
        """Set the layout\n设置布局"""
        #创建中心部件
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        #设置外边距为0
        self.main_widget.setContentsMargins(0, 0, 0, 0)
        #创建中心布局
        self.main_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()

        self.top_layout.addWidget(self.tipLabel)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.button_layout)
        self.main_widget.setLayout(self.main_layout)

    def __updateState(self):
        """Update the state\n更新窗口状态"""
        if self.__isSwitchHidden():
            self.__hidden()
        else:
            self.__show()
            self.__setTipText()
            self.__updateButton()
            self.__followMouse()


    def __followMouse(self):
        """Follow the mouse\n跟随鼠标"""
        self.move(self.pos.x()-250, self.pos.y()+20)  # 位置稍微往下偏移，避免阻碍视线
        self.show()

    def __isSwitchHidden(self):
        """Determine whether to switch hidden\n判断是否切换隐藏"""
        if State.now_ime_state == State.IME_STATE_CLOSE:
            return True
        if len(ImeCtrl.input_word) <= 0:
            return True
        return False

    def __hidden(self):
        """Hidden the window\n隐藏窗口"""
        self.hide()
        self.pre_hidden = True

    def __show(self):
        """show the window\n显示窗口"""
        self.show()
        if self.pre_hidden:
            self.pos = QCursor.pos()
        self.pre_hidden = False
    
    def __setButtonPreStyle(self, btn, widget,tipLabel):
        """Set the button style\n设置按钮样式"""
        btn.setStyleSheet("background-color:#a6d8ff;color: #353535;border:none;padding-bottom:27px;")
        widget.setStyleSheet("background-color:#a6d8ff;color: #636363;border:none;margin-left:5px")
        tipLabel.setStyleSheet("background-color:#a6d8ff;color: #636363;border:none;")

    def __setButtonNormalStyle(self, btn, widget,tipLabel):
        """Set the button style\n设置按钮样式"""
        btn.setStyleSheet("background-color:#f3f3f3;color: #353535;border:none;padding-bottom:27px;")
        widget.setStyleSheet("background-color:#f3f3f3;color: #636363;border:none;margin-left:5px")
        tipLabel.setStyleSheet("background-color:#f5f5f5;color: #636363;border:none;")

    def __setTipText(self):
        """Set the tip text\n设置提示文本"""
        self.tipLabel.setText(ImeCtrl.input_word)
    
    def __updateButton(self):
        """Update the button\n更新按钮"""
        for i in range(5):
            btn = self.button_list[i]
            #显示当前页的候选词
            if i < len(ImeCtrl.show_words):
                if State.now_ime_state == State.IME_STATE_LOW:
                    btn.setText(ImeCtrl.show_words[i].word.show_word_low)
                elif State.now_ime_state == State.IME_STATE_HIGH:
                    btn.setText(ImeCtrl.show_words[i].word.show_word_high)
                #如果是选中的词，背景颜色变化
                if ImeCtrl.pre_output == ImeCtrl.show_words[i]:
                    self.__setButtonPreStyle(btn,self.item_widget_list[i],self.tipLabel_list[i])
                else:
                    self.__setButtonNormalStyle(btn,self.item_widget_list[i],self.tipLabel_list[i])

