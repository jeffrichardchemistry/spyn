from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from math import e
from direct import Dirs

class boltzd(Dirs):
    def variables(self):
        get_temp = self.apy_ui.txt_tempboltz.text()
        temp_k = float(get_temp)

        get_nconf_boltz = self.apy_ui.txt_nconfboltz.text()
        get_nconf_boltz_int = int(get_nconf_boltz)
        get_nconf_boltzAutomatic = int(self.apy_ui.ln_automaticboltz.text())

        return temp_k, get_nconf_boltz_int, get_nconf_boltzAutomatic

    def onpressed(self):
        if self.apy_ui.cbox_unityboltz.currentText() == 'kj/mol':
            unity_manual = 'Energy kJ/mol'
        else:
            unity_manual = 'Energy kcal/mol'
        try:
            temp_k, get_nconf_boltz_int,get_nconf_boltzAutomatic = boltzd.variables(self)

            self.apy_ui.tables.clear()
            self.apy_ui.tables.setRowCount(get_nconf_boltz_int + 1)
            self.apy_ui.tables.setColumnCount(2)
            self.apy_ui.tables.setItem(0, 0, QtWidgets.QTableWidgetItem(unity_manual))
            self.apy_ui.tables.setItem(0, 1, QtWidgets.QTableWidgetItem("%Ci"))
            self.apy_ui.tables.setColumnWidth(0, 210)
            self.apy_ui.tables.setColumnWidth(1, 210)
        except ValueError:
            pass

    def calcboltzAutomatic(self):
        try:
            if self.apy_ui.cbox_unityboltz.currentText() == 'kj/mol':
                k = 0.0083144621
            else:
                k = 0.0019872041

            temp_k, get_nconf_boltz_int,get_nconf_boltzAutomatic = boltzd.variables(self)
            beta = 1 / (temp_k * k)
            denom = 0
            list_get_energy = []
            for j in range(1, get_nconf_boltzAutomatic + 1):
                item1 = self.apy_ui.tables.item(j, 1)       #Pegando as energias digitadas na tabela
                itemget = item1.text()                      #transformando o objeto em texto(o numero na tabela é um objeto nao iteravel)
                list_get_energy.append(float(itemget))      #Armazenando na lista os valores

                denom = denom + e ** (-beta * list_get_energy[j - 1])   #Calculando o denominador
                #print('Energys = ', list_get_energy)

            Ci = []
            for jj in range(1, get_nconf_boltzAutomatic + 1):
                calc_boltz = (e ** (-beta * list_get_energy[jj - 1]) * 100 / denom)     #Calculando tudo
                Ci.append(calc_boltz)

                #self.apy_ui.tables.setItem(jj, 2, QtWidgets.QTableWidgetItem('{:6f}'.format(calc_boltz)))      #Devolvendo o valor para a coluna %Ci
            return Ci

        except ValueError:
            pass

        except AttributeError:
            pass

    def boltzAutomatic(self):
        try:
            if self.apy_ui.cbox_unityboltz.currentText() == 'kj/mol': #pegando a combo box
                unity_boltz = 'Energy (kJ/mol)'
            else:
                unity_boltz = 'Energy (kcal/mol)'

            get_lnautomatic = int(self.apy_ui.ln_automaticboltz.text()) #pegando a linha
            dict_min = boltzd.dictAutogeneration(self)  #rodando a função pra pegar o dicionario com as energias
            dict_sorted = {}
            #print(dict_min)
            for item in sorted(dict_min, key=dict_min.get):
                dict_sorted['{}'.format(item)] = dict_min[item]
            #print(dict_sorted)
            self.apy_ui.tables.clear()
            self.apy_ui.tables.setRowCount(get_lnautomatic + 1)
            self.apy_ui.tables.setColumnCount(3)
            self.apy_ui.tables.setItem(0, 0, QtWidgets.QTableWidgetItem("Conformers"))
            self.apy_ui.tables.setItem(0, 1, QtWidgets.QTableWidgetItem(unity_boltz))
            self.apy_ui.tables.setItem(0, 2, QtWidgets.QTableWidgetItem("%Ci"))
            self.apy_ui.tables.setColumnWidth(0, 140)
            self.apy_ui.tables.setColumnWidth(1, 140)
            self.apy_ui.tables.setColumnWidth(2, 140)

            cnt = 0
            for key,value in dict_sorted.items(): #percorrendo os dicionarios e pegando as chaves e valores
                cnt += 1
                self.apy_ui.tables.setItem(cnt, 0, QtWidgets.QTableWidgetItem(key)) #adicionando as chaves na tabela
                self.apy_ui.tables.setItem(cnt, 1, QtWidgets.QTableWidgetItem(str(value))) #add os valores na tabela
            Ci_lst = boltzd.calcboltzAutomatic(self) #pegando os resultados do calculo do boltzmann

            cnt2 = 0
            for percent in Ci_lst:
                cnt2 += 1
                self.apy_ui.tables.setItem(cnt2,2, QtWidgets.QTableWidgetItem('{:6f}'.format(percent))) #add na tabela as porcentagens

        except AttributeError:
            boltz_qmbox = QMessageBox()
            boltz_qmbox.setWindowTitle('Error')
            boltz_qmbox.setText('It is necessary that the conformations be generated and the energy calculated')
            boltz_qmbox.setIcon(QMessageBox.Critical)
            boltz_qmbox.exec()

        except TypeError:
            boltz_qmbox = QMessageBox()
            boltz_qmbox.setWindowTitle('Error')
            boltz_qmbox.setText('The amount of conformations generated is smaller than the requested')
            boltz_qmbox.setIcon(QMessageBox.Critical)
            boltz_qmbox.exec()

        except IndexError:
            boltz_qmbox = QMessageBox()
            boltz_qmbox.setWindowTitle('Error')
            boltz_qmbox.setText('It is necessary that the conformations be generated and the energy calculated')
            boltz_qmbox.setIcon(QMessageBox.Critical)
            boltz_qmbox.exec()

        except ValueError:
            boltz_qmbox = QMessageBox()
            boltz_qmbox.setWindowTitle('Error')
            boltz_qmbox.setText('Type a integer value')
            boltz_qmbox.setIcon(QMessageBox.Critical)
            boltz_qmbox.exec()


    def calcboltz(self):
        try:
            if self.apy_ui.cbox_unityboltz.currentText() == 'kj/mol':
                k = 0.0083144621
            else:
                k = 0.0019872041

            temp_k, get_nconf_boltz_int,get_nconf_boltzAutomatic = boltzd.variables(self)
            beta = 1 / (temp_k * k)
            denom = 0
            list_get_energy = []
            for j in range(1, get_nconf_boltz_int + 1):
                item1 = self.apy_ui.tables.item(j, 0)       #Pegando as energias digitadas na tabela
                itemget = item1.text()                      #transformando o objeto em texto(o numero na tabela é um objeto nao iteravel)
                list_get_energy.append(float(itemget))      #Armazenando na lista os valores

                denom = denom + e ** (-beta * list_get_energy[j - 1])   #Calculando o denominador
                #print('Energys = ', list_get_energy)

            for jj in range(1, get_nconf_boltz_int + 1):
                calc_boltz = (e ** (-beta * list_get_energy[jj - 1]) * 100 / denom)     #Calculando tudo

                self.apy_ui.tables.setItem(jj, 1, QtWidgets.QTableWidgetItem(str(calc_boltz)))      #Devolvendo o valor para a coluna %Ci

        except ValueError:
            pass

        except AttributeError:
            pass

    def dictAutogeneration(self):
        try:
            file = '{}elowconf.log'.format(self.tmp_dir)
            with open('{}'.format(file), 'r') as j:
                file = j.readlines()
            # print(file)

            num_min = int(self.apy_ui.ln_automaticboltz.text())
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
            # print('confs_mins = {}'.format(confs_mins))

            get_conf_final = []
            dict1 = {}
            # print(list(enumerate(get_energys)))
            for indx, energyy in enumerate(get_energys):
                # print(indx,energy)
                for v in confs_mins:
                    if energyy == v:
                        get_conf_final.append('Confomero {} = {} kj/mol'.format((indx + 1), energyy))
                        dict1['Confomero {}'.format(indx + 1)] = energyy
            return dict1

        except FileNotFoundError:
            pass