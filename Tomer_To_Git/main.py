from PyQt5 import QtWidgets
from Tomer_To_Git.py_screen_files.main_menu import Ui_MainWindow
from Tomer_To_Git.Definitions.screen_definition import InstallerDefinition
import sys


# main is the starter of the program

if __name__ == '__main__':
    ins = InstallerDefinition(True, False)
    app = QtWidgets.QApplication(sys.argv)
    ins.open_window(Ui_MainWindow)
    sys.exit(app.exec_())

