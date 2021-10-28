import subprocess
import time
from dir import get_dir
from direct import Dirs
from PyQt5 import QtGui
from PyQt5.QtCore import QProcess, Qt

class qe(Dirs, get_dir):
    def __init__(self):
        get_dir.__init__(self)
        Dirs.__init__(self)
        self.bash_top = QProcess(self)

    def clickBoxx(self):
        get_check = self.apy_ui.chk_kauto.checkState() #Pegando status, pode ser 2 pra check e 0 pra uncheck
        if get_check == 2:
            self.apy_ui.ln_kgrid.setReadOnly(self.apy_ui.chk_kauto.checkState() != Qt.Unchecked) #travar o qline
            self.apy_ui.chk_kauto.stateChanged.connect(
                lambda get_check: self.apy_ui.ln_kgrid.setReadOnly(get_check != Qt.Unchecked))  #travar o qline

            self.apy_ui.ln_kgrid.setText('default')
        else:
            self.apy_ui.ln_kgrid.setText('111 111')

    def threads(self):
        nproc = subprocess.getoutput('nproc')
        if self.apy_ui.chkbox_threadsnmr.checkState() == 2:
            self.apy_ui.ln_threadsnmr.setReadOnly(self.apy_ui.chkbox_threadsnmr.checkState() != Qt.Unchecked)  # travar o qline
            self.apy_ui.chkbox_threadsnmr.stateChanged.connect(
                lambda get_check: self.apy_ui.ln_threadsnmr.setReadOnly(get_check != Qt.Unchecked))  # travar o qline

            self.apy_ui.ln_threadsnmr.setText(nproc)
            return 2
        else:
            return 0

    def pw_input(self):
        get_cbox_diag = self.apy_ui.cbox_diagonalization.currentText() #pegando o texto da combo box
        get_cbox_nosym = self.apy_ui.cbox_nosym.currentText() #pegando o texto da combo box
        if get_cbox_diag == 'David': #condição da comnbo box diag, jogando o valor dela na variavel diag
            diag = 'david'
        else:
            diag = 'cg'

        if get_cbox_nosym == 'True': #condição da comnbo box nosym, jogando o valor dela na variavel nosym
            nosym = '.true.'
        else:
            nosym = '.false.'

        try:
            get_cuttof = self.apy_ui.ln_cutoff.text() #pegando cutoff digitado
            get_stepscf = self.apy_ui.ln_stepscf.text() #pegando electron_maxstep
            get_accuracyscf = self.apy_ui.ln_acuraccyscf.text() #pegando precisão pra convergencia do scf
            get_kgrid = self.apy_ui.ln_kgrid.text() #pegando kgrid digitado
            get_chboxkgrid = self.apy_ui.chk_kauto.isChecked() #Chegando o status do checkbox (FALSO OU TRUE)
            get_ibrav = self.apy_ui.ln_ibrav.text() #pegando ibrav

            if get_chboxkgrid is True: #condição da check box
                #Rodando input com kpoint automatico(calculado)
                get_dir.getopenAll(self)

                run_pwin = subprocess.Popen("sh {}convert_kauto.sh {}".format(self.cif_pwscf, self.open_file),
                                            stdout=subprocess.PIPE, shell=True) #roda o script de montar input para kpoint automatico
                get_pwin = run_pwin.stdout.read().decode() #le e decodifica e joga o input na variavel get_pwin
                chan_tmp = get_pwin.replace('/tmpdir','{}'.format(self.tmp_dir)) #daqui pra baixa, é substituição de nomes
                chan_pp = chan_tmp.replace('/PPdir', '{}'.format(self.pp_dir))
                chan_cutoff = chan_pp.replace('CUTOFF','{}'.format(get_cuttof))
                chan_diago = chan_cutoff.replace('pydiag','{}'.format(diag))
                chan_nosym = chan_diago.replace('cboxnosym','{}'.format(nosym))
                chan_stepscf = chan_nosym.replace('pystepscf','{}'.format(get_stepscf))
                chan_acurscf = chan_stepscf.replace('pyaccuracyscf','{}'.format(get_accuracyscf))
                chan_ibrav = chan_acurscf.replace('ibcell','{}'.format(get_ibrav))
                self.apy_ui.txt_pwin.setText(chan_ibrav)        #Manda o input pro texto no software

                pwin_write = open('{}pwin.in'.format(self.tmp_dir), 'w')
                pwin_write.write(chan_ibrav)
                pwin_write.close()

            else:
                # Rodando input com kpoint manual
                get_dir.getopenAll(self) #pego as variaveis do outro arquivo

                ###########  Arrumando kpoint
                kpoint_spaceless = get_kgrid.replace(' ', '') #arrumando os espaços
                kgrid = ' '.join(kpoint_spaceless) #transformando a lista em string
                ###########
                run_pwin = subprocess.Popen("sh {}convert_kmanu.sh {}".format(self.cif_pwscf, self.open_file),
                                            stdout=subprocess.PIPE, shell=True)
                get_pwin = run_pwin.stdout.read().decode()
                chan_tmp = get_pwin.replace('/tmpdir', '{}'.format(self.tmp_dir))
                chan_pp = chan_tmp.replace('/PPdir', '{}'.format(self.pp_dir))
                chan_cutoff = chan_pp.replace('CUTOFF', '{}'.format(get_cuttof))
                chan_diago = chan_cutoff.replace('pydiag', '{}'.format(diag))
                chan_nosym = chan_diago.replace('cboxnosym', '{}'.format(nosym))
                chan_stepscf = chan_nosym.replace('pystepscf', '{}'.format(get_stepscf))
                chan_acurscf = chan_stepscf.replace('pyaccuracyscf', '{}'.format(get_accuracyscf))
                chan_kpoints = chan_acurscf.replace('kgrid_manual','{}'.format(kgrid))
                chan_ibrav = chan_kpoints.replace('ibcell', '{}'.format(get_ibrav))
                self.apy_ui.txt_pwin.setText(chan_ibrav)  # Manda o input pro texto no software

                pwin_write = open('{}pwin.in'.format(self.tmp_dir), 'w')
                pwin_write.write(chan_ibrav)
                pwin_write.close()
        except NameError:
            self.apy_ui.txt_pwin.setText("File cif not found or empty")

    def pw_output(self):

        #self.bash_top.start('xterm top') #Abrir uma dialog com o comando top do linux
        self.defreeze = QtGui.QGuiApplication.processEvents
        check = qe.threads(self)

        try:
            if check == 2:
                nproc = subprocess.getoutput('nproc')
            else:
                nproc = self.apy_ui.ln_threadsnmr.text()

            fpwin = open('{}pwin.in'.format(self.tmp_dir), 'r') #só serve para nao aparecer a mensagem de erro de diretório na tela
            fpwin.close() #quando roda direto o pwout
            self.apy_ui.progbar_qe.setVisible(True) #Mostrar a barra de progresso do qe na janela
            #print(fpwin.read())
            subprocess.call("mpirun -np {} pw <{}pwin.in>{}pwout.out &".format(nproc, self.tmp_dir, self.tmp_dir), shell=True) #rodar o calculo
            time.sleep(1) #tempo de esperar pra começar a rodar o calculo, pq assim da pra pegar o pid do pw
            pidof = subprocess.getoutput('pidof pw') #pegando o pid do pw

            cnt=0 #contador da barra de progresso
            self.defreeze() #carrega função para nao congelar a tela
            while pidof != '': #contador que testa o pidof, pra saber qnd o calculo vai acabar (o pidof some quando o calculo acaba
                cnt += 1
                if cnt > 100: #condição pro contador ficar resetando, pois assim a barra de progresso tbm reseta
                    cnt = 0
                pidof = subprocess.getoutput('pidof pw')    #pega o pidof do pw a cada loop
                self.apy_ui.progbar_qe.setValue(cnt)    #seta o valor do contador na barra de progresso

                if self.apy_ui.progbar_qe.value() == self.apy_ui.progbar_qe.maximum(): #testar se a barra de progresso atingiu o valor maximo
                    self.apy_ui.progbar_qe.reset()
                    self.apy_ui.progbar_qe.setValue(cnt)
                self.defreeze() #emite o sinal para descongelar a tela
                #subprocess.run('cp {}pwout.out {}pwgrep'.format(self.tmp_dir, self.tmp_dir), shell=True) #Modo interativo da mineração do pw, mas deixa o software pesado


            self.apy_ui.progbar_qe.setVisible(False) #qnd o calculo acabar, some com a barra de progresso

            f = open('{}pwout.out'.format(self.tmp_dir), 'r') #abre o arquivo de saida do pwscf
            fread = f.read()
            f.close()
            self.apy_ui.txt_pwout.setText(fread) #joga o output na tela
            self.defreeze()

            subprocess.run('cp {}pwout.out {}pwgrep'.format(self.tmp_dir, self.tmp_dir), shell=True) #copiar o output pra deixar um arquivo pra grep
            subprocess.run('rm {}pwin.in {}pwout.out'.format(self.tmp_dir, self.tmp_dir), shell=True) #apagar os arquivos de input e output, isso é necessário pq se rodar direto o pwout o input nao é printado
            fend = open('{}end'.format(self.tmp_dir), 'w') #cria um arquivo quando o calculo termina, serve para saber se o gipaw tem que rodar o pwout ou nao
            fend.write('end')
            fend.close()

        except FileNotFoundError: #rodando direto o pw output
            qe.pw_input(self) #roda a função de montar o input
            debug = 'pass'
            try:
                get_dir.getopenAll(self) #busca pelo caminho, se o CIF ja foi aberto
            except NameError:
                debug = 'debugerror'
            if debug == 'debugerror':           #se o cif nao for aberto
                self.apy_ui.txt_pwout.setText("File cif not found or empty")
            else:
                qe.pw_output(self) #roda a função de output

        finally:
            pass
            #self.bash_top.close()

    def gipaw(self):
        check = qe.threads(self) #checando a opção de threads
        self.defreeze = QtGui.QGuiApplication.processEvents #função para destravar a tela
        debug = 'pass'
        try:
            get_dir.getopenAll(self) #testando se o CIF foi aberto
        except NameError:
            debug = 'debugerror'

        if debug == 'pass': #se o CIF foi aberto, rode normal
            try:
                get_prefix = get_dir.getopenAll(self) #pegando o diretorio completo, com nome do arquivo no final
                lst = [x for x in get_prefix.split("/")] #tirando tudo e deixando só o ultimo nome, no caso é o nome do arquivo
                prefix = lst[-1][:-4] #tirando o .cif do nome do arquivo
            except NameError: #erro qnd o cara nao abriu o cif
                self.apy_ui.txt_gipaw.setText('Please choose a cif file')

            try:
                combobox = self.apy_ui.cbox_diagonalization.currentText() #pegando a combobox
                if combobox == 'David':
                    diag_gipaw = 'david'
                else:
                    diag_gipaw = 'cg'

                input_gipaw = ("&inputgipaw\n"
                               "      job = 'nmr'\n"
                               "      prefix = '{}'\n"
                               "      tmp_dir = '{}'\n"
                               "      diagonalization = '{}'\n"
                               "      verbosity = 'high'\n"
                               "      q_gipaw = 0.01\n"
                               "      spline_ps = .true.\n"
                               "      use_nmr_macroscopic_shape = .true.\n"
                               "/\n"
                               " ".format(prefix, self.tmp_dir, diag_gipaw)) #montando o input

                f_gin = open('{}gipawin.in'.format(self.tmp_dir), 'w') #criando o arquivo com input do gipaw
                f_gin.write(input_gipaw)
                f_gin.close()
            except UnboundLocalError:
                self.apy_ui.txt_gipaw.setText('Please choose a cif file') #debugando para o usuario abrir um arquivo cif


            try:
                if check == 2:
                    nproc = subprocess.getoutput('nproc')
                else:
                    nproc = self.apy_ui.ln_threadsnmr.text()

                fend = open('{}end'.format(self.tmp_dir), 'r') #esse try é pra ver se ja rodamos o pwout antes e assim nao ter que rodar de novo
                fend.close()

                self.apy_ui.progbar_qe.setVisible(True) #ativando progbar
                subprocess.call('mpirun -np {} gipaw <{}gipawin.in>{}gipawout.out &'.format(nproc,self.tmp_dir, self.tmp_dir),
                                shell=True)  # rodando o gipaw
                time.sleep(1) #daqui pra baixo ja está explicado na função pwout
                pidof = subprocess.getoutput('pidof gipaw')
                cnt = 0
                self.defreeze()
                while pidof != '':
                    cnt += 1
                    if cnt > 100:
                        cnt = 0
                    pidof = subprocess.getoutput('pidof gipaw')
                    self.apy_ui.progbar_qe.setValue(cnt)

                    if self.apy_ui.progbar_qe.value() == self.apy_ui.progbar_qe.maximum():
                        self.apy_ui.progbar_qe.reset()
                        self.apy_ui.progbar_qe.setValue(cnt)
                    self.defreeze()

                self.apy_ui.progbar_qe.setVisible(False)
                f_gout = open('{}gipawout.out'.format(self.tmp_dir), 'r')
                f_goutread = f_gout.read()
                f_gout.close()
                self.apy_ui.txt_gipaw.setText(f_goutread)
                self.defreeze()

            except FileNotFoundError:   #esse except é pra rodarmos o gipaw direto
                qe.pw_input(self) #Roda o pw input
                qe.pw_output(self) #Roda o pw output

                self.apy_ui.progbar_qe.setVisible(True)
                subprocess.call('mpirun -np {} gipaw <{}gipawin.in>{}gipawout.out &'.format(nproc,self.tmp_dir, self.tmp_dir),
                                shell=True)  # rodando o gipaw
                time.sleep(1)
                pidof = subprocess.getoutput('pidof gipaw')
                cnt = 0
                self.defreeze()
                while pidof != '':
                    cnt += 1
                    if cnt > 100:
                        cnt = 0
                    pidof = subprocess.getoutput('pidof gipaw')
                    self.apy_ui.progbar_qe.setValue(cnt)

                    if self.apy_ui.progbar_qe.value() == self.apy_ui.progbar_qe.maximum():
                        self.apy_ui.progbar_qe.reset()
                        self.apy_ui.progbar_qe.setValue(cnt)
                    self.defreeze()

                self.apy_ui.progbar_qe.setVisible(False)
                f_gout = open('{}gipawout.out'.format(self.tmp_dir), 'r')
                f_goutread = f_gout.read()
                f_gout.close()
                self.apy_ui.txt_gipaw.setText(f_goutread)
                self.defreeze()

                time.sleep(0.8)
                subprocess.call('mv {}/*.magres {}'.format(self.pwd, self.tmp_dir),shell=True)
        else:
            self.apy_ui.txt_gipaw.setText("File cif not found or empty")
