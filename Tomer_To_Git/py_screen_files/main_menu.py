# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Tomer\PycharmProjects\Pyqt5_improved_framework\Tomer_To_Git\ui_screen_files\main_menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 738)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.upload_record = QtWidgets.QPushButton(self.centralwidget)
        self.upload_record.setEnabled(True)
        self.upload_record.setGeometry(QtCore.QRect(310, 140, 271, 81))
        font = QtGui.QFont()
        font.setFamily("Perpetua")
        font.setPointSize(16)
        self.upload_record.setFont(font)
        self.upload_record.setObjectName("upload_record")
        self.enter_profiles = QtWidgets.QPushButton(self.centralwidget)
        self.enter_profiles.setGeometry(QtCore.QRect(40, 20, 131, 101))
        font = QtGui.QFont()
        font.setFamily("Perpetua")
        font.setPointSize(16)
        self.enter_profiles.setFont(font)
        self.enter_profiles.setObjectName("enter_profiles")
        self.path_box = QtWidgets.QTextEdit(self.centralwidget)
        self.path_box.setGeometry(QtCore.QRect(250, 250, 391, 51))
        font = QtGui.QFont()
        font.setFamily("Perpetua")
        font.setPointSize(10)
        self.path_box.setFont(font)
        self.path_box.setObjectName("path_box")
        self.identify_btn = QtWidgets.QPushButton(self.centralwidget)
        self.identify_btn.setGeometry(QtCore.QRect(370, 540, 141, 61))
        font = QtGui.QFont()
        font.setFamily("Perpetua")
        font.setPointSize(16)
        self.identify_btn.setFont(font)
        self.identify_btn.setObjectName("identify_btn")
        self.radioButton_4 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_4.setGeometry(QtCore.QRect(410, 490, 89, 20))
        font = QtGui.QFont()
        font.setFamily("Perpetua")
        font.setPointSize(14)
        self.radioButton_4.setFont(font)
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setGeometry(QtCore.QRect(410, 460, 89, 20))
        font = QtGui.QFont()
        font.setFamily("Perpetua")
        font.setPointSize(14)
        self.radioButton_3.setFont(font)
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(410, 430, 89, 21))
        font = QtGui.QFont()
        font.setFamily("Perpetua")
        font.setPointSize(14)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_1 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_1.setGeometry(QtCore.QRect(410, 400, 89, 20))
        font = QtGui.QFont()
        font.setFamily("Perpetua")
        font.setPointSize(14)
        self.radioButton_1.setFont(font)
        self.radioButton_1.setObjectName("radioButton_1")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 300, 391, 111))
        font = QtGui.QFont()
        font.setFamily("Perpetua")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label.raise_()
        self.upload_record.raise_()
        self.enter_profiles.raise_()
        self.path_box.raise_()
        self.identify_btn.raise_()
        self.radioButton_4.raise_()
        self.radioButton_3.raise_()
        self.radioButton_2.raise_()
        self.radioButton_1.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.upload_record.setText(_translate("MainWindow", "Upload a new record"))
        self.enter_profiles.setText(_translate("MainWindow", "Profiles"))
        self.path_box.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Perpetua\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt;\">Here Will Be The Path</span></p></body></html>"))
        self.identify_btn.setText(_translate("MainWindow", "Identify"))
        self.radioButton_4.setText(_translate("MainWindow", "DB16"))
        self.radioButton_3.setText(_translate("MainWindow", "DB2"))
        self.radioButton_2.setText(_translate("MainWindow", "Bior4.4"))
        self.radioButton_1.setText(_translate("MainWindow", "Haar"))
        self.label.setText(_translate("MainWindow", "Please select a type of transformation to the\n"
"pre-processing stage:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())