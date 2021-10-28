import subprocess
from PyQt5.QtCore import QProcess

class killProcess():
    def terminal(self):
        self.bash_top_all = QProcess()
        self.bash_top_all.start('xterm top')

    def stopPwout(self):
        pid = subprocess.getoutput('pidof pw')
        if pid == '' or pid == None:
            pass
        else:
            subprocess.call('kill {}'.format(pid), shell=True)

    def stopGipaw(self):
        pid = subprocess.getoutput('pidof gipaw')
        if pid == '' or pid == None:
            pass
        else:
            subprocess.call('kill {}'.format(pid), shell=True)