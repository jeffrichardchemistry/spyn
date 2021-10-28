import subprocess
import time
from dir import get_dir
from direct import Dirs
from PyQt5.QtCore import QProcess,Qt
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import pandas as pd

####### EU AINDA PRECISO RODAR UMA MOLECULA QUE GERE VARIOS CONFOMEROS, PARA PODER TESTAR O SED

class csGA(get_dir, Dirs):
    def __init__(self):
        get_dir.__init__(self)          #puxar o construtor do arquivo dir, onde eu pego a variavel que tem a string diretório
        self.defreeze2 = QtGui.QGuiApplication.processEvents

    def run_CS_GA(self):
        try:
            #self.process = QProcess(self) #função pra iniciar terminal
            #self.process.start('xterm top') #comando top no terminal
            get_dir.getopenAll(self)  # necessario rodar pra rodar a função que pega a variavel que tem o diretório e joga no construtor
            self.apy_ui.progbar.setHidden(False)

            # Linebox for get the number typed
            nconf_text = self.apy_ui.txt_ncon.text()
            children_text = self.apy_ui.txt_child.text()
            mutability_text = self.apy_ui.txt_mut.text()
            converge_text = self.apy_ui.txt_conv.text()
            score_text = self.apy_ui.txt_scor.text()

            contt = 0
            self.defreeze2() #descongelando a tela
            #rodando o calculo
            get_cmd_log = subprocess.Popen(
                'obabel {} -O {} --conformer --nconf {} --children {} --mutability {} --converge {} --score {} --writeconformers &'.format(
                    self.open_file,
                    self.diroutput_cs,
                    nconf_text,
                    children_text,
                    mutability_text,
                    converge_text,
                    score_text), stdout=subprocess.PIPE ,shell=True)
            time.sleep(1) #tempo de espera pra pegar o pidof
            pidof_babel = subprocess.getoutput('pidof obabel')

            self.defreeze2()
            while pidof_babel != '':
                contt += 1
                if contt > 100:     #resetando o contador
                    contt = 0
                pidof_babel = subprocess.getoutput('pidof obabel') #buscando o pidof a cada loop
                self.apy_ui.progbar.setValue(contt)

                if self.apy_ui.progbar.value() == self.apy_ui.progbar.maximum():        #testando o valor da progbar e resetando o valor na barra de progresso
                    self.apy_ui.progbar.reset()
                    self.apy_ui.progbar.setValue(contt)
                self.defreeze2()

            self.apy_ui.progbar.setValue(100) #FIM DO CALCULO, SETA EM 100%
            self.apy_ui.progbar.setHidden(True) #SOME COM A BARRA
            self.apy_ui.progbar.reset() #resetar para a proxima vez que começar o calculo
            self.apy_ui.txt_log_show.setText(get_cmd_log.stdout.read().decode())    #JOGA O TEXTO DO LOG

            # Run script to show the sequence of conformers
            subprocess.call(
                'sh {}'.format(self.dirscript_conf), shell=True)  # Colocar a ordem dos confomeros mudar o diretório no script
            with open(self.diroutput_cs) as babel_read:
                run_cs_read = babel_read.read()
                self.apy_ui.txt_conformer_show.setText(run_cs_read)

            ##########

            self.apy_ui.progbar.setHidden(True)
            #self.process.close()

        except NameError:
            csGA_QMBox = QMessageBox()
            csGA_QMBox.setIcon(QMessageBox.Warning) #pra puxar a imagem, tem que construir a janela do zero
            csGA_QMBox.setWindowTitle('Warning')
            csGA_QMBox.setText('File not find or empty')
            csGA_QMBox.exec()

        except FileNotFoundError:
            csGA_QMBox = QMessageBox()
            csGA_QMBox.setIcon(QMessageBox.Critical)  # pra puxar a imagem, tem que construir a janela do zero
            csGA_QMBox.setWindowTitle('Error')
            csGA_QMBox.setText('File not find or empty')
            csGA_QMBox.exec()

    def exportCSGA(self):
        try:
            get_lnconfs = self.apy_ui.ln_exportConformers.text()
            get_ln = [int(x) for x in get_lnconfs.split(';')]  # pegando a lista de conformeros exigidos

            with open('{}output.sdf'.format(self.tmp_dir), 'r') as nconf:  # ler o arquivo e jogar em uma variavel
                nconfread = nconf.read()

            conf1 = pd.DataFrame(
                ['{}'.format(confs) for confs in nconfread.split('\n')])  # colocando o quebra linha em geral

            putildes_init = [kids for k in get_ln for kids in (
                conf1.index[
                    conf1[0] == ('Conformer {}'.format(k))].values)]  # aqui pega os indexes inicial do Conformer x

            # PEGAR INDEX FINAL DE CADA CONF
            def conf_end(vip):
                while conf1.loc[vip, 0] != '$$$$':
                    vip += 1
                yield (vip - 1)

            putildes_end = [kudos for vip in putildes_init for kudos in
                            conf_end(vip)]  # aqui pega as posições finais dos confomeros"onde tem $"

            conf_list = []
            for l in range(len(get_ln)):  # aqui arrumamos os conformeros pedidos dentro de uma lista
                conf_list.extend([(pd.DataFrame(conf1.loc[putildes_init[l]:putildes_end[l], 0])).to_csv(index=False,
                                                                                                        header=False)])  # usa o to_csv, para tabular dentro do dataframe

            confs_str = ''.join(conf_list)  # arrumando o arquivo de saida
            grep1 = confs_str.replace('''""''', ' ')  # arrumando o arquivo de saida
            grep2 = grep1.replace('Conformer', '\nConformer')  # arrumando o arquivo de saida

            get_exportDir, trash = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                         'Save Energy')  # nome e diretório do arquivo pra salvar
            confile = open('{}.sdf'.format(get_exportDir), 'w')
            confile.write(grep2)
            confile.close()


        except FileNotFoundError:
            csGA_QMBox = QMessageBox()
            csGA_QMBox.setIcon(QMessageBox.Critical)
            csGA_QMBox.setWindowTitle('Error')
            csGA_QMBox.setText('The conformers were not generated')
            csGA_QMBox.exec()
        except IndexError:
            csGA_QMBox = QMessageBox()
            csGA_QMBox.setIcon(QMessageBox.Critical)
            csGA_QMBox.setWindowTitle('Error')
            csGA_QMBox.setText('The amount of conformations generated is smaller than the requested')
            csGA_QMBox.exec()
        except ValueError:
            csGA_QMBox = QMessageBox()
            csGA_QMBox.setIcon(QMessageBox.Critical)
            csGA_QMBox.setWindowTitle('Error')
            csGA_QMBox.setText('Type the number of conformer')
            csGA_QMBox.exec()

    def checkBox_overlap(self):
        get_check = self.apy_ui.chkbox_overlapALL.checkState()  # Pegando status, pode ser 2 pra check e 0 pra uncheck
        if get_check == 2:
            self.apy_ui.ln_overlapConfs.setReadOnly(
                self.apy_ui.chkbox_overlapALL.checkState() != Qt.Unchecked)  # travar o qline
            self.apy_ui.chkbox_overlapALL.stateChanged.connect(
                lambda get_check: self.apy_ui.ln_overlapConfs.setReadOnly(get_check != Qt.Unchecked))  # travar o qline

            return 2
        else:
            return 0

    def plotAllconfs(self):
        try:
            with open('{}output.sdf'.format(self.tmp_dir), 'r') as f:
                fread = f.read()

            ln_confs = list(range(1, fread.count('Conformer') + 1)) #pego o numero maximo de confomeros

            dict_lnconfs = {}
            for get_ln in ln_confs:

                conf1 = pd.DataFrame(
                    ['{}'.format(confs) for confs in fread.split('\n')])  # colocando o quebra linha em geral'''

                putildes_init = list(conf1.index[conf1[0] == ('Conformer {}'.format(get_ln))].values - 1)

                # PEGAR INDEX FINAL DE CADA CONF
                def conf_end(vip):
                    while conf1.loc[vip, 0] != '$$$$':
                        vip += 1
                    yield (vip)

                putildes_end = [kudos for vip in putildes_init for kudos in
                                conf_end(vip)]  # aqui pega as posi��es finais dos confomeros"onde tem $"

                indexes = list(range(putildes_init[0], putildes_end[
                    0] + 1))  # crio uma lista com o range dos indexes, para poder pegar essas linhas
                get_confFormated = conf1.loc[indexes, 0].to_csv(index=False,
                                                                header=False)  # localizo todas as linhas do confomero pedido e ja retorno formatado
                conf_formatedSTR = ''.join(get_confFormated)  # coloco como string, para poder exportar

                # arrumando o arquivo de saida
                grep1 = conf_formatedSTR.replace('''""''', ' ')  # arrumando o arquivo de saida
                grep2 = grep1.replace('$$$$', ' ')  # arrumando o arquivo de saida
                dict_lnconfs['Conformer{}'.format(get_ln)] = grep2 #Faço um dicionario, onde as chaves são os nomes dos confomeros

                fconf = open('{}Conformer{}.sdf'.format(self.tmp_dir,get_ln), 'w') #gravo em arquivos de texto para poder rodar o script do jmol
                fconf.write(grep2)
                fconf.close()

            allconf_list = (list(dict_lnconfs.keys())) #salvo as chaves do dicionario em uma lista, pois são os nomes que vão no script do jmol
            allconf_list2 = ["'{}.sdf' ".format(y) for y in allconf_list] #Arrumo o nome pra ir no script
            jmol = ['load files '] #comando base do script-jmol pra sobrepor
            jmol.extend(allconf_list2) #juntando o nome das conformações e o comando base
            overlap_Str = ''.join(jmol) #transformando em string
            foverlap = open('{}overlapConfs.spt'.format(self.tmp_dir), 'w') #gravando o script jmol no pc
            foverlap.write(overlap_Str)
            foverlap.close()

            subprocess.run('cd {} && jmol -ILi -s {}overlapConfs.spt'.format(self.tmp_dir, self.tmp_dir), shell=True)

            subprocess.run('rm {}Conformer* {}overlapConfs*'.format(self.tmp_dir,self.tmp_dir), shell=True)

        except FileNotFoundError:
            csGA_QMBox = QMessageBox()
            csGA_QMBox.setIcon(QMessageBox.Warning)  # pra puxar a imagem, tem que construir a janela do zero
            csGA_QMBox.setWindowTitle('Warning')
            csGA_QMBox.setText('File not find/empty or the conformers was not calculated')
            csGA_QMBox.exec()

    def plotConfs(self):
        try:
            ln_confs = [int(x) for x in self.apy_ui.ln_overlapConfs.text().split(';')] # pegando quais confomeros serão exportados

            dict_lnconfs = {}
            for get_ln in ln_confs:

                with open('{}output.sdf'.format(self.tmp_dir), 'r') as nconf:  # ler o arquivo e jogar em uma variavel
                    nconfread = nconf.read()

                conf1 = pd.DataFrame(
                    ['{}'.format(confs) for confs in nconfread.split('\n')])  # colocando o quebra linha em geral

                putildes_init = list(conf1.index[conf1[0] == ('Conformer {}'.format(get_ln))].values - 1) #pego a posição inicial do nome Confomero no dataframe conf1

                # PEGAR INDEX FINAL DE CADA CONF
                def conf_end(vip):
                    while conf1.loc[vip, 0] != '$$$$':
                        vip += 1
                    yield (vip)

                putildes_end = [kudos for vip in putildes_init for kudos in
                                conf_end(vip)]  # aqui pega as posições finais dos confomeros"onde tem $"

                indexes = list(range(putildes_init[0], putildes_end[
                    0] + 1))  # crio uma lista com o range dos indexes, para poder pegar essas linhas
                get_confFormated = conf1.loc[indexes, 0].to_csv(index=False,
                                                                header=False)  # localizo todas as linhas do confomero pedido e ja retorno formatado
                conf_formatedSTR = ''.join(get_confFormated)  # coloco como string, para poder exportar

                # arrumando o arquivo de saida
                grep1 = conf_formatedSTR.replace('''""''', ' ')  # arrumando o arquivo de saida
                grep2 = grep1.replace('$$$$', ' ')  # arrumando o arquivo de saida
                dict_lnconfs['Conformer{}'.format(get_ln)] = grep2

                fconf = open('{}Conformer{}.sdf'.format(self.tmp_dir,get_ln), 'w')
                fconf.write(grep2)
                fconf.close()

            allconf_list = (list(dict_lnconfs.keys()))
            allconf_list2 = ["'{}.sdf' ".format(y) for y in allconf_list]
            jmol = ['load files ']
            jmol.extend(allconf_list2)
            overlap_Str = ''.join(jmol)
            foverlap = open('{}overlapConfs.spt'.format(self.tmp_dir), 'w')
            foverlap.write(overlap_Str)
            foverlap.close()

            subprocess.run('cd {} && jmol -ILi -s {}overlapConfs.spt'.format(self.tmp_dir,self.tmp_dir), shell=True)

            subprocess.run('rm {}Conformer* {}overlapConfs*'.format(self.tmp_dir,self.tmp_dir), shell=True)

        except FileNotFoundError:
            csGA_QMBox = QMessageBox()
            csGA_QMBox.setIcon(QMessageBox.Warning)  # pra puxar a imagem, tem que construir a janela do zero
            csGA_QMBox.setWindowTitle('Warning')
            csGA_QMBox.setText('File not find/empty or the conformers was not calculated')
            csGA_QMBox.exec()

        except ValueError:
            csGA_QMBox = QMessageBox()
            csGA_QMBox.setIcon(QMessageBox.Warning)  # pra puxar a imagem, tem que construir a janela do zero
            csGA_QMBox.setWindowTitle('Warning')
            csGA_QMBox.setText("Type the which conformers must be generated. To more than 1 conformer, separate by ';'. example: 1;2;3;4;5")
            csGA_QMBox.exec()

