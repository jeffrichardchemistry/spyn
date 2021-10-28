import subprocess
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidget, QMessageBox
from direct import Dirs

class energy(Dirs):
    def __init__(self):
        self.tables = QTableWidget()
        Dirs.__init__(self)

    def runTables(self):
        try:
            energy_txt, combobox = energy.calcEnergy(self)
            if combobox == 'MMFF94' or combobox == 'MMFF94s':
                get_dict = energy.get_minimos(self)
                self.tables.clear()
                num_min = int(self.apy_ui.ln_confs.text())
                self.tables.resize(315, 400)
                self.tables.setWindowTitle('Lower Energy Conformers')
                self.tables.setColumnCount(2)
                self.tables.setRowCount(num_min + 1)
                self.tables.setItem(0, 0, QtWidgets.QTableWidgetItem("Label"))
                self.tables.setItem(0, 1, QtWidgets.QTableWidgetItem("Energy (kcal/mol)"))
                self.tables.setColumnWidth(0, 150)
                self.tables.setColumnWidth(1, 150)
            else:
                get_dict = energy.get_minimos(self)
                self.tables.clear()
                num_min = int(self.apy_ui.ln_confs.text())
                self.tables.resize(315, 400)
                self.tables.setWindowTitle('Lower Energy Conformers')
                self.tables.setColumnCount(2)
                self.tables.setRowCount(num_min + 1)
                self.tables.setItem(0, 0, QtWidgets.QTableWidgetItem("Label"))
                self.tables.setItem(0, 1, QtWidgets.QTableWidgetItem("Energy (kj/mol)"))
                self.tables.setColumnWidth(0, 150)
                self.tables.setColumnWidth(1, 150)
            try:
                cntkeyvalue=0
                for keydict,valuedict in get_dict.items():
                    cntkeyvalue += 1
                    self.tables.setItem(cntkeyvalue, 0, QtWidgets.QTableWidgetItem(keydict))
                    self.tables.setItem(cntkeyvalue, 1, QtWidgets.QTableWidgetItem(str(valuedict)))
                self.tables.show()


            except AttributeError:
                #self.apy_ui.txt_energy_show.setText("The energy wasn't calculated, do it first.")
                csGA_QMBox = QMessageBox()
                csGA_QMBox.setIcon(QMessageBox.Critical)
                csGA_QMBox.setWindowTitle('Error')
                csGA_QMBox.setText("The energy wasn't calculated, do it first.")
                csGA_QMBox.exec()

        except ValueError:
            csGA_QMBox = QMessageBox()
            csGA_QMBox.setIcon(QMessageBox.Critical)
            csGA_QMBox.setWindowTitle('Error')
            csGA_QMBox.setText('Type the number of lower energy conformers')
            csGA_QMBox.exec()



    def get_minimos(self):
        try:
            file = '{}elowconf.log'.format(self.tmp_dir)
            with open('{}'.format(file), 'r') as j:
                file = j.readlines()
            #print(file)

            num_min = int(self.apy_ui.ln_confs.text())
            lst1 = []
            cnt = 0
            for i in file:
                for j in i.split():
                    cnt = cnt + 1
                    lst1.append(j)
            # print('lst1 = {}'.format(lst1))
            lst2 = []
            for k in lst1:
                lst2.append(k.split())
            # print('lst2 = {}'.format(lst2))

            lst_cnt = []
            cnt = 4
            for cntador in range(0, int(len(lst2) / 6)):
                cnt = cnt + 6
                lst_cnt.append(cnt)
            del lst_cnt[-1]
            # print('lst_cnt = {}'.format(lst_cnt,'\n'))

            get_energys = []
            get_energys.append(float(lst2[4][0]))
            for jk in lst_cnt:
                a = lst2[jk]
                for p in a:
                    get_energys.append(float(p))
            # print('Energias = {}'.format(get_energys))

            ordem_energ = [zz for zz in get_energys]
            ordem_energ.sort()
            # print('Minimos de energias ordenados = {}'.format(ordem_energ))

            confs_mins = ordem_energ[:num_min]
            #print('confs_mins = {}'.format(confs_mins))

            get_conf_final = []
            dict1={}
            # print(list(enumerate(get_energys)))
            for indx, energyy in enumerate(get_energys):
                # print(indx,energy)
                for v in confs_mins:
                    if energyy == v:
                        get_conf_final.append('Confomero {} = {} kj/mol'.format((indx + 1), energyy))
                        dict1['Confomero {}'.format(indx + 1)] = energyy
            return dict1

        except FileNotFoundError:
            energy_QMBox = QMessageBox()
            energy_QMBox.setWindowTitle('Error')
            energy_QMBox.setText("The energy wasn't calculated, do it first.")
            energy_QMBox.setIcon(QMessageBox.Critical)
            energy_QMBox.exec()

        except IndexError:
            energy_QMBox = QMessageBox()
            energy_QMBox.setWindowTitle('Error')
            energy_QMBox.setText("The energy wasn't calculated, do it first.")
            energy_QMBox.setIcon(QMessageBox.Critical)
            energy_QMBox.exec()


    def calcEnergy(self):
        #global get_combobox
        get_combobox = self.apy_ui.cbox_energyfield.currentText()

        if get_combobox == 'UFF':
            #global energy_UFF
            energy_UFF = subprocess.getoutput(
                'obenergy -ff UFF -v {} '
                '| grep -a "TOTAL EN" |'
                ' while read -r line ;'
                ' do i=$((i+1));'
                ' echo "Conformer $i:'
                '$line" ; done'.format(self.diroutput_cs))
            self.apy_ui.txt_energy_show.setText(energy_UFF)
            wfile = open('{}elowconf.log'.format(self.tmp_dir), 'w')
            wfile.write(energy_UFF)
            wfile.close()
            return energy_UFF, get_combobox


        elif get_combobox == 'MMFF94':
            global energy_MMFF94
            energy_MMFF94 = subprocess.getoutput(
                'obenergy -ff MMFF94 -v {} '
                '| grep -a "TOTAL EN" |'
                ' while read -r line ;'
                ' do i=$((i+1));'
                ' echo "Conformer $i:'
                '$line" ; done'.format(self.diroutput_cs))
            self.apy_ui.txt_energy_show.setText(energy_MMFF94)
            wfile = open('{}elowconf.log'.format(self.tmp_dir), 'w')
            wfile.write(energy_MMFF94)
            wfile.close()

            return energy_MMFF94, get_combobox

        elif get_combobox == 'MMFF94s':
            #global energy_MMFF94s
            energy_MMFF94s = subprocess.getoutput(
                'obenergy -ff MMFF94s -v {} '
                '| grep -a "TOTAL EN" |'
                ' while read -r line ;'
                ' do i=$((i+1));'
                ' echo "Conformer $i:'
                '$line" ; done'.format(self.diroutput_cs))
            self.apy_ui.txt_energy_show.setText(energy_MMFF94s)
            wfile = open('{}elowconf.log'.format(self.tmp_dir), 'w')
            wfile.write(energy_MMFF94s)
            wfile.close()

            return energy_MMFF94s, get_combobox

        elif get_combobox == 'Ghemical':
            #global energy_Ghemical
            energy_Ghemical = subprocess.getoutput(
                'obenergy -ff Ghemical -v {} '
                '| grep -a "TOTAL EN" |'
                ' while read -r line ;'
                ' do i=$((i+1));'
                ' echo "Conformer $i:'
                '$line" ; done'.format(self.diroutput_cs))
            self.apy_ui.txt_energy_show.setText(energy_Ghemical)
            wfile = open('{}elowconf.log'.format(self.tmp_dir), 'w')
            wfile.write(energy_Ghemical)
            wfile.close()

            return energy_Ghemical, get_combobox

        elif get_combobox == 'GAFF':
            #global energy_GAFF
            energy_GAFF = subprocess.getoutput(
                'obenergy -ff GAFF -v {} '
                '| grep -a "TOTAL EN" |'
                ' while read -r line ;'
                ' do i=$((i+1));'
                ' echo "Conformer $i:'
                '$line" ; done'.format(self.diroutput_cs))
            self.apy_ui.txt_energy_show.setText(energy_GAFF)
            wfile = open('{}elowconf.log'.format(self.tmp_dir), 'w')
            wfile.write(energy_GAFF)
            wfile.close()

            return energy_GAFF, get_combobox


    def export_energy_GA(self):
        get_energytxt, get_combobox = energy.calcEnergy(self)

        get_export_dir, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Energy', '/home')
        if get_export_dir == '' or get_export_dir is None:
            pass
        else:
            if get_combobox == 'UFF':
                with open('{}'.format(get_export_dir), 'w') as exportUFF:
                    exportUFF.write(get_energytxt)

            elif get_combobox == 'MMFF94':
                with open('{}'.format(get_export_dir), 'w') as exportMMFF94:
                    exportMMFF94.write(get_energytxt)

            elif get_combobox == 'MMFF94s':
                with open('{}'.format(get_export_dir), 'w') as exportMMFF94s:
                    exportMMFF94s.write(get_energytxt)

            elif get_combobox == 'Ghemical':
                with open('{}'.format(get_export_dir), 'w') as exportGhemical:
                    exportGhemical.write(get_energytxt)

            elif get_combobox == 'GAFF':
                with open('{}'.format(get_export_dir), 'w') as exportGAFF:
                    exportGAFF.write(get_energytxt)
