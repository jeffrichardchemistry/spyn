from PyQt5 import QtWidgets
import subprocess
from direct import Dirs
#from csGA import csGA

class get_dir():
    def __init__(self, open_file='a'):      #É necessario criar um construtor, pois os outros arquivos puxam variaveis daqui quando a gente seta la
        self.open_file = open_file

    def open_from_menu(self):
        global menu_open_file
        menu_open_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open molecule file', '',
                                                            ' All (*.mol *.mol2 *.cml *.com *.xyz *.mold *.molden *.cif *.sdf) ;;'
                                                            ' mol (*.mol);;.mol2 (*.mol2) ;;.cml (*.cml);;.com (*.com);;.xyz(*.xyz);;.cif (*.cif);;.sdf (*.sdf);;.mold (*.mold);;.molden(*.molden);;')

        if menu_open_file == '' or menu_open_file is None:
            self.apy_ui.lbl_show_dir_cs.setText('File wrong or empty')
        else:            
            self.apy_ui.lbl_show_dir_cs.setText('File dir:  {}'.format(menu_open_file))
            self.apy_ui.lbl_show_dir_cs_2.setText('File dir:  {}'.format(menu_open_file))
            subprocess.run('nohup jmol -ILi {} &'.format(menu_open_file), shell=True)

        return menu_open_file


    def getopenAll(self):
        self.open_file = menu_open_file     #função para pegar o diretório
        return self.open_file

