# -*- coding: utf-8 -*-
import subprocess
subprocess.run('sudo apt install xterm', shell=True)
subprocess.run('sudo apt-get install python3-pip python3-dev python3-pyqt5',shell=True)
from PyQt5 import QtCore, QtGui, QtWidgets



class Ui_Dialog(object):
        
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(415, 88)
        Dialog.setMinimumSize(QtCore.QSize(415, 88))
        Dialog.setMaximumSize(QtCore.QSize(415, 88))
        icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap("{}/spyn.png".format(self.dir_images)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.btn_install = QtWidgets.QPushButton(Dialog)
        self.btn_install.setGeometry(QtCore.QRect(310, 50, 90, 31))
        self.btn_install.setObjectName("btn_install")
        self.btn_install.clicked.connect(self.install)
        self.ln_dir = QtWidgets.QLineEdit(Dialog)
        self.ln_dir.setGeometry(QtCore.QRect(10, 10, 351, 31))
        self.ln_dir.setObjectName("ln_dir")
        self.btn_findir = QtWidgets.QPushButton(Dialog)
        self.btn_findir.setGeometry(QtCore.QRect(360, 10, 31, 31))
        self.btn_findir.setObjectName("btn_findir")
        self.btn_findir.clicked.connect(self.dirinstall)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Install spyn"))
        self.btn_install.setText(_translate("Dialog", "Install"))
        self.ln_dir.setText(_translate("Dialog", "Please, choose a directory for installation"))
        self.btn_findir.setText(_translate("Dialog", "..."))

    def install(self):  
        get_direct = self.ln_dir.text() #get text of qline
        spyn_direct = '{}/spyn'.format(get_direct) #var for create file with dir 
        subprocess.run('tar -xzvf spyn.tar.gz -C {}'.format(get_direct),shell=True) #unpack targz file        
        Ui_Dialog.writeSpyndir(self) #function to create a python file into spyn directory with directory installed
        QtWidgets.qApp.quit() #close app        
        subprocess.run("xterm -e 'cd {} && python3 install_spyn.py && exit; bash'".format(spyn_direct), shell=True)
        Ui_Dialog.desktopEntry(self) #function to create a entry and resolving permissions         
        subprocess.run("xterm -e 'sh {}/permissionDE.sh && exit; bash'".format(spyn_direct), shell=True)

    def dirinstall(self):
        global dir_install
        dir_install = QtWidgets.QFileDialog.getExistingDirectory(None, 'Directory for install','') #dialog to get dir
        self.ln_dir.setText('{}'.format(dir_install)) #show dir choosed 
        return dir_install

    def writeSpyndir(self):        
        get_direct = self.ln_dir.text() #get text of qline
        spyn_direct = '{}/spyn'.format(get_direct) #var for create file with dir
        text = ("class Spyndir():\n"
                "   def __init__(self):\n"
                "       self.spyndir = '{}'\n".format(spyn_direct))
        
        fdir = open('{}/spyndir.py'.format(spyn_direct),'w') #create file into spyns dir with directory
        fdir.write("{}".format(text))
        fdir.close()

        fspynsh = open('{}/spyn.sh'.format(spyn_direct), 'w') #create file into spyns dir with initialize shell
        fspynsh.write('#!/bin/bash\ncd {} && python3 spyn_main.py'.format(spyn_direct))
        fspynsh.close()
    
    def desktopEntry(self):
        get_direct = self.ln_dir.text() #get text of qline
        spyn_direct = '{}/spyn'.format(get_direct) #var for create file with dir
        #creating a desktop entry
        entry = (   "[Desktop Entry]\n"
                    "Name=Spyn\n"
                    "GenericName=Spyn\n"
                    "Comment=GUI for Chemical calculations\n"
                    "Exec={}/spyn.sh\n"
                    "Terminal=false\n"
                    "Type=Application\n"
                    "Icon={}/fig/spyn.png\n"
                    "StartupNotify=false\n"
                    "Categories=Network;\n"
                    "".format(spyn_direct,spyn_direct))
        fde = open('{}/spyn.desktop'.format(spyn_direct),'w')
        fde.write(entry)
        fde.close()

        #resolving permission things and moving entry to applications sistem
        fdesh = open('{}/permissionDE.sh'.format(spyn_direct), 'w')
        fdesh.write("#!/bin/bash\n"
                    "echo 'Permission for create a Spyn icon'\n"
                    "sudo chmod a+xrw {}/spyn.desktop\n"
                    "sudo chmod +x {}/spyn.sh\n"
                    "sudo cp {}/spyn.desktop /usr/share/applications/spyn.desktop\n".format(spyn_direct,spyn_direct,spyn_direct)
                     )
        fdesh.close()

      

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
