from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QCursor
from core.state import State
class StatusBarWin(QMainWindow):
    """
    StatusBarWin\n状态栏窗口类
    """
    def __init__(self):
        super().__init__()
        self.m_flag = False
        self.__setWindowUi()
        self.__createLabel()
        self.show()

    def __setWindowUi(self):
        """set window ui\n设置窗口ui"""
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint|Qt.SplashScreen ) #窗口置顶，无边框
        screen_geometry = QApplication.desktop().screenGeometry()#获取屏幕大小
        status_width = 120  #设置窗口大小
        status_height = 50
        self.setGeometry(screen_geometry.width() - status_width - 10,  
                         screen_geometry.height() - status_height - 10,
                           status_width, status_height)
        self.setStyleSheet("background-color: rgba(135,206,250, 50%);")# 设置窗口浅蓝色背景，透明度为50%

    def __createLabel(self):
        """create label\n创建标签"""
        text_label = QLabel('状态提示', self)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setGeometry(10, 10, 100, 30)
        text_label.setStyleSheet("QLabel { color : white; }")
        
        #设置定时器，每隔一段时间更新状态，连接插槽
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.__updateState)
        self.timer.start(300)

    def __updateState(self):
        text = State.now_ime + State.now_ime_state
        self.findChild(QLabel).setText(text)

    #重写鼠标事件实现窗口拖动
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  #更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
            QMouseEvent.accept()
            
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))

