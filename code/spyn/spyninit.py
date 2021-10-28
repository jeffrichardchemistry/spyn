import sys
import time
from direct import Dirs
from spyn_main import spyn_main
from stylesprogbar import layoutsProgbar
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Initialize(Dirs):
    def __init__(self):
        Dirs.__init__(self)

    def splash(self):
        style1, style2, style3, style4, style5, style6, style7 = layoutsProgbar.stylesProgbar(self)            
        splash_pix = QPixmap('{}/logo5.png'.format(self.dir_images))
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        splash.setEnabled(False)    

        progressBar_splash = QProgressBar(splash)
        progressBar_splash.setMaximum(10)
        progressBar_splash.setGeometry(40, splash_pix.height() - 20, splash_pix.width() - 85, 17) #(Movimento em x, Movimento em Y, Largura da progbar, Altura da progbar)        
        progressBar_splash.setStyleSheet(style6)
        splash.show()

        for i in range(1, 11):
            progressBar_splash.setValue(i)
            t = time.time()
            while time.time() < t + 0.1:
                app.processEvents()
                
        #time.sleep(5) 
        splash.finish(gui)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = spyn_main()
    spl = Initialize()
    spl.splash()
    gui.show()

    sys.exit(app.exec_())