from core.gui.tray import TrayIcon
from PyQt5 import QtWidgets, QtGui, QtCore
from core.gui.status import StatusBarWin
from core.gui.input import InputWin
from core.gui.editconfig import EditWindow

def onStart(args):
    """
    Start the GUI\n
    启动GUI

    Args:
        args (list): Get it By 'sys.argv()'\n
                        通过'sys.argv()'获取    

    """
    app = QtWidgets.QApplication(args)
    MainWindow = QtWidgets.QMainWindow()
    statusBarWin = StatusBarWin()
    statusBarWin.show()
    inputWin = InputWin()
    inputWin.show()
    editWin = EditWindow()
    tray = TrayIcon(MainWindow,showDialog=editWin.show)
    tray.show()
    app.exec_()