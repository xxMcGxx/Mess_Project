import sys
from PyQt5 import QtWidgets
import client_gui_conv

# Вариант 1. Объект формы - атрибут класса главного окна
class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = client_gui_conv.Ui_MainClientWindow()
        self.ui.setupUi(self)
        self.ui.btnQuit.clicked.connect(QtWidgets.qApp.quit)

# Вариант 2. Главное окно дополнительно наследуется от класса формы
class MyWindow_2(QtWidgets.QWidget, client_gui_conv.Ui_MainClientWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui.setupUi(self)
        self.ui.btnQuit.clicked.connect(QtWidgets.qApp.quit)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())