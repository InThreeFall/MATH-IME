from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from const import static
from core.state import State
class TrayIcon(QtWidgets.QSystemTrayIcon):
    """
    TrayIcon\n托盘图标类
    """
    def __init__(self,MainWindow,parent=None,showDialog=None):
        """
        init\n初始化

        Args:
            MainWindow:MainWindow
            parent:parent
            showDialog:showDialog
        """
        super(TrayIcon, self).__init__(parent)
        self.ui = MainWindow
        self.showDialog = showDialog
        self.__createMenu()
    
    def __createMenu(self):
        """create menu\n创建菜单"""
        self.menu = QtWidgets.QMenu()
        self.showAction0 = QtWidgets.QAction("状态：", self, triggered=self.update_state)
        self.showAction1 = QtWidgets.QAction("大写/小写/关闭", self, triggered=self.switch_state)
        self.showAction2 = QtWidgets.QAction("切换输入法", self,triggered=self.switch_ime)
        self.showAction3 = QtWidgets.QAction("编辑词库", self,triggered=self.setting)
        self.showAction4 = QtWidgets.QAction("关于", self,triggered=self.about)
        self.editConfigAction = QtWidgets.QAction("编辑配置", self,triggered=self.editConfig)
        self.quitAction = QtWidgets.QAction("退出", self, triggered=self.quit)

        self.menu.addAction(self.showAction0)
        self.menu.addAction(self.showAction1)
        self.menu.addAction(self.showAction2)
        self.menu.addAction(self.showAction3)
        self.menu.addAction(self.showAction4)
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)
 
        #设置图标
        self.setIcon(QtGui.QIcon(static.ICON_PATH))
        self.icon = self.MessageIcon()

        #设置定时器
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_state)
        self.timer.start(1000)

    def update_state(self):
        """update state\n更新状态"""
        self.showAction0.setText("状态:"+State.now_ime+" "+State.now_ime_state)

    def switch_state(self):
        """switch state\n切换状态"""
        State.switch_state()
        self.update_state()

    def editConfig(self):
        """edit config\n编辑配置"""
        import os
        os.system("notepad "+static.CONFIG_PATH)

    def switch_ime(self):
        """switch ime\n切换输入法"""
        State.switch_ime()
        self.update_state()

    def setting(self):
        """setting\n设置"""
        self.showDialog()

    def about(self):
        """about\n关于"""
        import os
        os.system("notepad "+static.ABOUT_PATH)

    def quit(self):
        """quit\n退出"""
        QtWidgets.qApp.quit()
 

