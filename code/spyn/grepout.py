import subprocess
from direct import Dirs

class grepoutput(Dirs):
    def __init__(self):
        Dirs.__init__(self)

    def grepScf(self):
        get_combox = self.apy_ui.cbox_filterscfout.currentText()
        if get_combox == 'Iterations':
            grep_iter = subprocess.getoutput("grep '     total energy  ' {}pwgrep".format(self.tmp_dir)) #pegando o grep
            lst = [x for x in grep_iter.split('=')] #quebrando pelo sinal de =
            lst2 = lst[1:]  #pegando do segundo elemento pra frente, pq só tem os numeros e mais algumas coisas
            strlst = ''.join(lst2)  #transformando em string
            lst3 = strlst.split('total energy') #cortando total energy, o retorno é uma lista
            strlst2 = ''.join(lst3)     #voltando pra string para poder manipular
            lst4 = strlst2.split('Ry')  #Manipulando a string strlst2 pra cortar os Ry o retorno é uma lista
            strlst3 = ''.join(lst4)     #voltando pra string para poder manipular
            lst5 = [float(y) for y in strlst3.split()] #ja pega somente as energias
            cnt = 0 #contar as iterações
            grep_final = [] #pegar o formato certo do texto a ser printado na tela
            for gf in lst5:
                cnt = cnt + 1 #numeros de iterações
                grep_final.append('Iteration {}:  Energy  =  {:8f} Ry\n'.format(cnt,gf)) #formato do texto
            self.apy_ui.txt_pwout.setText(''.join(grep_final)) #transformo a lista em uma string e jogo pra dentro do software

        elif get_combox == 'Total energy':
            grep_iter = subprocess.getoutput("grep '! ' {}pwgrep".format(self.tmp_dir))
            self.apy_ui.txt_pwout.setText(grep_iter)

    def grepGipaw(self):
        get_combox = self.apy_ui.cbox_filtergipawout.currentText()

        grep1 = subprocess.getoutput("grep 'Total sigma' {}gipawout.out | grep '{} '".format(self.tmp_dir, get_combox))
        print(grep1)
        lstg1 = [x for x in grep1.split(' ')]  # tirar espaços e juntar tudo
        grep2 = ''.join(lstg1)  # transformar em string

        lstg2 = []
        for y in grep2.splitlines():  # for pra pegar só o numero do atomo e o sigma
            findC = y.find('{}'.format(get_combox))  # pega a posição onde encontra o C
            findTs = y.find('sigma')  # pega a posição do sigma
            lstg2.append(y[:findC] + ' atomo ' +'*' + y[findTs:] + ' ppm\n')  # pego tudo até o C depois pego tudo do sigma pra frente

        grep3 = ''.join(lstg2)  # transformando em string
        grep4 = grep3.replace(':', ' = ')  # arrumando texto
        grep5 = grep4.replace('atomo','{}'.format(get_combox)) #colocando qual atomo é(arrumando texto)
        grep_final = grep5.replace('*', ':')  # arrumando texto
        self.apy_ui.txt_gipaw.setText(grep_final)