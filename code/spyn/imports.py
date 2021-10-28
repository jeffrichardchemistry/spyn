from PyQt5 import QtWidgets
from direct import Dirs

class importAll(Dirs):

    def importGiaoout(self):
        try:
            dir_giao, _ = QtWidgets.QFileDialog.getOpenFileName(self,'Open a GIAO output','')
            
            fgiao = open(dir_giao,'r')
            fgiaor = fgiao.read()
            fgiao.close()

            fgiaow = open('{}giaout.out'.format(self.tmp_dir),'w')
            fgiaow.write(fgiaor)
            fgiaow.close()
            
        except FileNotFoundError:
            pass        
    
    def importGipawout(self):
        try:
            dir_gipout, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open a Gipaw-QE output','')
            fgip = open(dir_gipout, 'r')
            fgipread = fgip.read()
            fgip.close()
            
            fgipw = open('{}gipawout.out'.format(self.tmp_dir), 'w')
            fgipw.write(fgipread)
            fgipw.close()
        except FileNotFoundError:
            pass

    def importConfs(self):
        try:
            dir_conf, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open molecule file', '',
                                                                '(*.mol *.sdf) ;;')
            fallconfs = open('{}'.format(dir_conf), 'r')
            fallconfs_read = fallconfs.read()
            fallconfs.close()

            fallconfs2 = open('{}output.sdf'.format(self.tmp_dir), 'w')
            fallconfs2.write(fallconfs_read)
            fallconfs2.close()

        except FileNotFoundError:
            pass

    def importPWscfout(self):
        try:
            dir_pwout, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open a PWscf-QE output','')
            fpwscfout = open(dir_pwout, 'r')
            fpwscfoutr = fpwscfout.read()
            fpwscfout.close()

            fpw = open('{}pwgrep'.format(self.tmp_dir), 'w')
            fpw.write(fpwscfoutr)
            fpw.close()

        except FileNotFoundError:
            pass
        
