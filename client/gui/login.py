# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Vern\Desktop\New folder\loginnew.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import source,sqlite3
from start import MainWindow


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1147, 777)
        Form.setAutoFillBackground(False)
        Form.setStyleSheet("*{\n"
"    font-family:century gothic;\n"
"    font-size:24px;\n"
"}\n"
"\n"
"#Form{\n"
"    border-image:url(:/newPrefix/Q7XTON.jpg)  0 0 0 0 stretch stretch;\n"
"    \n"
"}\n"
"\n"
"QFrame\n"
"{\n"
"    background:white;\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"QToolButton{\n"
"    background:white;    \n"
"    border-radius:15px;\n"
"}\n"
"\n"
"QLabel{\n"
"    color:Black;\n"
"    \n"
"\n"
"}\n"
"\n"
"QPushButton{\n"
"    background:gray;\n"
"    border-radius:15px;\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"    color:white;\n"
"    border-radius:15px;\n"
"    background:#333;\n"
"}\n"
"\n"
"QLineEdit{\n"
"    background:transparent;\n"
"    border:none;\n"
"    color:#717072;\n"
"    border-bottom:1px solid #717072;\n"
"}\n"
"")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(300, 70, 561, 601))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.Label = QtWidgets.QLabel(self.frame)
        self.Label.setGeometry(QtCore.QRect(140, 40, 271, 111))
        self.Label.setObjectName("Label")
        self.login_btn = QtWidgets.QPushButton(self.frame)
        self.login_btn.setGeometry(QtCore.QRect(100, 480, 381, 61))
        self.login_btn.setObjectName("login_btn")
        self.uname_lineEdit = QtWidgets.QLineEdit(self.frame)
        self.uname_lineEdit.setGeometry(QtCore.QRect(120, 240, 401, 41))
        self.uname_lineEdit.setText("")
        self.uname_lineEdit.setObjectName("uname_lineEdit")
        self.pass_lineEdit = QtWidgets.QLineEdit(self.frame)
        self.pass_lineEdit.setGeometry(QtCore.QRect(120, 360, 411, 31))
        self.pass_lineEdit.setText("")
        self.pass_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_lineEdit.setObjectName("pass_lineEdit")
        self.Usernamelogo = QtWidgets.QToolButton(self.frame)
        self.Usernamelogo.setGeometry(QtCore.QRect(40, 230, 81, 71))
        self.Usernamelogo.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/male.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Usernamelogo.setIcon(icon)
        self.Usernamelogo.setIconSize(QtCore.QSize(48, 48))
        self.Usernamelogo.setObjectName("Usernamelogo")
        self.Passwordlogo = QtWidgets.QToolButton(self.frame)
        self.Passwordlogo.setGeometry(QtCore.QRect(40, 350, 71, 41))
        self.Passwordlogo.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/lock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Passwordlogo.setIcon(icon1)
        self.Passwordlogo.setIconSize(QtCore.QSize(64, 64))
        self.Passwordlogo.setObjectName("Passwordlogo")
        self.u_name_label = QtWidgets.QLabel(self.frame)
        self.u_name_label.setGeometry(QtCore.QRect(120, 200, 231, 41))
        self.u_name_label.setObjectName("u_name_label")
        self.pass_label = QtWidgets.QLabel(self.frame)
        self.pass_label.setGeometry(QtCore.QRect(120, 320, 181, 41))
        self.pass_label.setObjectName("pass_label")
        
        self.login_btn.clicked.connect(self.loginCheck) 

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Label.setText(_translate("Form", "Digital Crime Analyzer"))
        self.login_btn.setText(_translate("Form", "LOGIN"))
        self.uname_lineEdit.setPlaceholderText(_translate("Form", "Username"))
        self.pass_lineEdit.setPlaceholderText(_translate("Form", "Password"))
        self.u_name_label.setText(_translate("Form", "Username"))
        self.pass_label.setText(_translate("Form", "Password"))
    
    
    def loginCheck(self):
        username = self.uname_lineEdit.text()
        password = self.pass_lineEdit.text()
        connection = sqlite3.connect("login.db")
        result = connection.execute("SELECT * FROM USER WHERE USERNAME = ? AND PASSWORD = ?",(username,password))
        if (len(result.fetchall())>0):
            print("User Found! ")
            Form.hide()
            self.startWindowShow()
        else:
            print ("User Not Found!")
            self.showMessageBox('Warning',"Wrong Username/Password")
            self.uname_lineEdit.clear()
            self.pass_lineEdit.clear()
    
    
    def startWindowShow(self):
        self.theclass= MainWindow()
        self.theclass.show()
    
    def showMessageBox(self,title,message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
