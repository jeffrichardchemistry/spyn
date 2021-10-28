import subprocess
from PyQt5.QtWidgets import QMessageBox
from scipy.signal import savgol_filter as savgo
import numpy as np
from direct import Dirs

class allPlots(Dirs):

    def getToolsplot(self):
        try:
            #pegando todas as variaveis da pagina spec
            ppm = [float(ppm) for ppm in self.apy_ui.ln_tensors.text().split(',')]

            reference = self.apy_ui.ln_reference.text()
            if reference.isalpha() is True:
                #referencia = 0
                referencia = 'None'
            elif reference == '' or reference == None:
                referencia = 'None'
            else:
                referencia = float(reference)

            xmin = self.apy_ui.ln_xmin.text()
            xmax = self.apy_ui.ln_xmax.text()
            ymin = self.apy_ui.ln_ymin.text()
            ymax = self.apy_ui.ln_ymax.text()
            A = self.apy_ui.ln_intensity.text()
            width = self.apy_ui.ln_width.text()
            suav = self.apy_ui.ln_suavization.text()
            cbox_method = self.apy_ui.cbox_lorentzianSticks.currentText()
            return ppm,referencia,float(xmin),float(xmax),float(ymin),float(ymax),float(A),float(width),int(suav),cbox_method

        except ValueError:
            csGA_QMBox = QMessageBox()
            csGA_QMBox.setIcon(QMessageBox.Critical)
            csGA_QMBox.setWindowTitle('Error')
            csGA_QMBox.setText('Please, fill in all parameters\nSuavization must be a integer value')
            csGA_QMBox.exec()
    
    def plotGiao(self):
        try:
            teste_ofile = open('{}giaout.out'.format(self.tmp_dir), 'r')
            teste_ofile.close()

            x0, referencia, xmin, xmax, ymin, ymax, A, width, suav, cbox_method = allPlots.getToolsplot(self)
            atom = self.apy_ui.cbox_nmrgraphGIPAW.currentText()
            
            grep1 = subprocess.getoutput("grep 'Isotropic ' {}giaout.out | grep '{} '".format(self.tmp_dir, atom))

            lst1 = grep1.split(' ')
            str1 = ''.join(lst1)
            
            ppm_x = []
            for l2 in str1.splitlines():
                ppm_x.append(round(float(l2[l2.find('{}'.format(atom)):l2.find('A')].replace('Isotropic=','').replace('{}'.format(atom),'')),2)) #Arrumo todo o texto, pego só os numeros, e ja retorno float
            print(ppm_x)
            ppm_x.sort()
            print(ppm_x)
            if cbox_method == 'Sticks':
                self.apy_ui.MplWidget.canvas.axes.clear()
                for tensors in ppm_x:
                    if referencia == 'None':
                        self.apy_ui.MplWidget.canvas.axes.axvline(tensors,ymin=0, ymax=0.45)
                    else:
                        self.apy_ui.MplWidget.canvas.axes.axvline(abs(tensors - referencia),ymin=0, ymax=0.45)
                self.apy_ui.MplWidget.canvas.axes.set_xlim([xmax,xmin])
                self.apy_ui.MplWidget.canvas.axes.set_ylim([ymin,ymax])
                self.apy_ui.MplWidget.canvas.draw()

            elif cbox_method == 'Lorentzian':
                xaray = np.arange(xmin, xmax, 0.001)
                md = []
                cnt = 0
                cnt2 = 0
                y = []
                if referencia == 'None':
                    x0 = [ppm for ppm in ppm_x]
                else:
                    x0 = [abs(ppm-referencia) for ppm in ppm_x]
                x0.sort()
                if len(x0) == 1: #list with 1 ppm
                    for xx in xaray:
                        y.append((A * (width ** 2)) / (width ** 2 + (4 * (x0[0] - xx) ** 2)))

                    self.apy_ui.MplWidget.canvas.axes.clear()
                    self.apy_ui.MplWidget.canvas.axes.plot(xaray, y)
                    self.apy_ui.MplWidget.canvas.axes.set_ylim([ymin, ymax])
                    self.apy_ui.MplWidget.canvas.axes.set_xlim([xmax, xmin])
                    self.apy_ui.MplWidget.canvas.axes.set_xlabel('ppm')
                    self.apy_ui.MplWidget.canvas.draw()

                elif len(x0) == 2: #list with 2 PPM
                    md.append(round((x0[0] + x0[1]) / 2, 2))  #calculus of media, in this case exist just 1 value
                    for xx in xaray:
                        y.append((A * (width ** 2)) / (
                                    width ** 2 + (4 * (round(x0[cnt], 3) - round(xx, 3)) ** 2)))  # faço a conta

                        if round(xx, 2) == md[0]:  # When x to arrive in median, up counter
                            cnt += 1
                            if cnt > 1:  # como a lista de x0 só tem 2 elementos, o contador nao pode passar de 1
                                cnt = 1  # entao eu mantenho ele sempre em 1

                    yhat = savgo(y, 51, suav)
                    self.apy_ui.MplWidget.canvas.axes.clear()
                    self.apy_ui.MplWidget.canvas.axes.plot(xaray, yhat)
                    self.apy_ui.MplWidget.canvas.axes.set_ylim([ymin, ymax])
                    self.apy_ui.MplWidget.canvas.axes.set_xlim([xmax, xmin])
                    self.apy_ui.MplWidget.canvas.axes.set_xlabel('ppm')
                    self.apy_ui.MplWidget.canvas.draw()

                else: #AQUI É PRA LISTA MAIOR Q 2 PPM
                    for tensor in range(len(x0)):
                        if tensor == len(x0) - 1:
                            break
                        else:
                            md.append(round((x0[tensor] + x0[tensor + 1]) / 2, 2))

                    for xx in xaray:  # percorro cada item do vetor
                        y.append((A * (width**2)) / (width**2 + (4*(round(x0[cnt], 3) - round(xx, 3))**2)))
                        if round(xx, 2) == md[cnt2]:  # qnd o x chegar na média sobe os 2 contadores (contador da lista média e da lista x0)
                            cnt2 += 1
                            cnt += 1
                            if cnt2 > len(md) - 1:  # se o contador da média for maior que a lista da média eu zero ele
                                cnt2 = 0

                    yhat = savgo(y, 51, suav)

                    self.apy_ui.MplWidget.canvas.axes.clear()
                    self.apy_ui.MplWidget.canvas.axes.plot(xaray, yhat)
                    self.apy_ui.MplWidget.canvas.axes.set_ylim([ymin, ymax])
                    self.apy_ui.MplWidget.canvas.axes.set_xlim([xmax, xmin])
                    self.apy_ui.MplWidget.canvas.axes.set_xlabel('ppm')
                    self.apy_ui.MplWidget.canvas.draw()
                    
        except FileNotFoundError:
            csGA_QMBox = QMessageBox()
            csGA_QMBox.setIcon(QMessageBox.Critical)
            csGA_QMBox.setWindowTitle('Error')
            csGA_QMBox.setText('Its necessary import GIAO output')
            csGA_QMBox.exec()

    def plotGipawManual(self):
        try:
            x0, referencia, xmin, xmax, ymin, ymax, A, width, suavization, cbox_method = allPlots.getToolsplot(self)
            
            x0.sort()
            print(x0)
            if cbox_method == 'Sticks':
                self.apy_ui.MplWidget.canvas.axes.clear()
                for tensors in x0:
                    if referencia == 'None':                        
                        self.apy_ui.MplWidget.canvas.axes.axvline(tensors,ymin=0, ymax=0.45)
                    else:
                        self.apy_ui.MplWidget.canvas.axes.axvline(abs(tensors - referencia), ymin=0, ymax=0.45)
                self.apy_ui.MplWidget.canvas.axes.set_xlim([xmax,xmin])
                self.apy_ui.MplWidget.canvas.axes.set_ylim([ymin,ymax])
                self.apy_ui.MplWidget.canvas.draw()
                
            elif cbox_method == 'Lorentzian':
                xaray = np.arange(xmin, xmax, 0.001)
                md = []
                y = []
                xx = []
                cnt = 0
                cnt2 = 0
                if referencia == 'None':
                    x0 = x0
                else:
                    x0 = [abs(ppm - referencia) for ppm in x0]
                x0.sort()
                if len(x0) == 1:
                    for x in xaray:
                        y.append((A * (width ** 2)) / (width ** 2 + (4 * (x0[0] - x) ** 2)))

                    self.apy_ui.MplWidget.canvas.axes.clear()
                    self.apy_ui.MplWidget.canvas.axes.plot(xaray, y)
                    self.apy_ui.MplWidget.canvas.axes.set_ylim([ymin, ymax])
                    self.apy_ui.MplWidget.canvas.axes.set_xlim([xmax, xmin])
                    self.apy_ui.MplWidget.canvas.axes.set_xlabel('ppm')
                    self.apy_ui.MplWidget.canvas.draw()

                elif len(x0) == 2:
                    md.append(round((x0[0] + x0[1]) / 2, 2))  # calculo a média nesse caso só vai ter 1 valor
                    for x in xaray:
                        y.append(
                            (A * (width ** 2)) / (width ** 2 + (4 * (round(x0[cnt], 3) - round(x, 3)) ** 2)))  # faço a conta

                        if round(x, 2) == md[0]:  # qnd o x chegar na média, sobe o contador
                            cnt += 1
                            if cnt > 1:  # como a lista de x0 só tem 2 elementos, o contador nao pode passar de 1
                                cnt = 1  # entao eu mantenho ele sempre em 1

                    yhat = savgo(y, 51, suavization)
                    self.apy_ui.MplWidget.canvas.axes.clear()
                    self.apy_ui.MplWidget.canvas.axes.plot(xaray, yhat)
                    self.apy_ui.MplWidget.canvas.axes.set_ylim([ymin, ymax])
                    self.apy_ui.MplWidget.canvas.axes.set_xlim([xmax, xmin])
                    self.apy_ui.MplWidget.canvas.axes.set_xlabel('ppm')
                    self.apy_ui.MplWidget.canvas.draw()

                else:
                    for tensor in range(len(x0)):
                        if tensor == len(x0) - 1:
                            break
                        else:
                            md.append(round((x0[tensor] + x0[tensor + 1]) / 2, 2))

                    for x in xaray:  # percorro cada item do vetor
                        y.append((A * (width ** 2)) / (width ** 2 + (4 * (round(x0[cnt], 3) - round(x, 3)) ** 2)))  # faço o calculo
                        xx.append(x)  # armazeno o x em uma lista (nao precisa disso)
                        if round(x, 2) == md[cnt2]:  # qnd o x chegar na média sobe os 2 contadores (contador da lista média e da lista x0)
                            cnt2 += 1
                            cnt += 1
                            if cnt2 > len(md) - 1:  # se o contador da média for maior que a lista da média eu zero ele
                                cnt2 = 0

                    yhat = savgo(y, 51, suavization)
                    #self.apy_ui.MplWidget.canvas.axes.clear()
                    self.apy_ui.MplWidget.canvas.axes.plot(xaray, yhat)
                    self.apy_ui.MplWidget.canvas.axes.set_ylim([ymin, ymax])
                    self.apy_ui.MplWidget.canvas.axes.set_xlim([xmax, xmin])
                    self.apy_ui.MplWidget.canvas.axes.set_xlabel('ppm')
                    self.apy_ui.MplWidget.canvas.draw()
        except TypeError:
            pass
        except IndexError:
            pass #quando tenho só numeros repetidos da erro, arrumar isso

    def plotGipawcalc(self):
        try:
            ppm,referencia, xmin, xmax, ymin, ymax, A, width, suav, cbox_method = allPlots.getToolsplot(self)
            try:
                get_combox = self.apy_ui.cbox_nmrgraphGIPAW.currentText()

                grep1 = subprocess.getoutput("grep 'Total sigma' {}gipawout.out | grep '{} '".format(self.tmp_dir, get_combox))

                lstg1 = [x for x in grep1.split(' ')]  # tirar espaços e juntar tudo
                grep2 = ''.join(lstg1)  # transformar em string

                lstg2 = []
                for y in grep2.splitlines():  # for pra pegar só o numero do atomo e o sigma
                    findC = y.find('{}'.format(get_combox))  # pega a posição onde encontra o C
                    findTs = y.find('sigma')  # pega a posição do sigma
                    lstg2.append(y[:findC] + ' atomo ' + '*' + y[
                                                               findTs:] + ' ppm\n')  # pego tudo até o C depois pego tudo do sigma pra frente

                grep3 = ''.join(lstg2)  # transformando em string
                grep4 = grep3.replace(':', ' = ')  # arrumando texto
                grep5 = grep4.replace('atomo', '{}'.format(get_combox))  # colocando qual atomo é(arrumando texto)
                grep6 = grep5.replace('*', ':')  # arrumando texto
                grep7 = grep6.replace('Atom', '')
                grep8 = grep7.replace('{}'.format(get_combox), '')
                grep9 = grep8.replace(':sigma =', '')
                grep10 = grep9.replace('ppm', '')
                index_ppm = [filter for filter in grep10.split()]
                ppm = index_ppm[1::2] #pegando só os tensores
                ppm_x = [float(x) for x in ppm]

                if cbox_method == 'Sticks':
                    self.apy_ui.MplWidget.canvas.axes.clear()
                    for tensors in ppm_x:
                        if referencia == 'None':
                            self.apy_ui.MplWidget.canvas.axes.axvline(tensors,ymin=0, ymax=0.45)
                        else:
                            self.apy_ui.MplWidget.canvas.axes.axvline(abs(tensors - referencia),ymin=0, ymax=0.45)
                    self.apy_ui.MplWidget.canvas.axes.set_xlim([xmax,xmin])
                    self.apy_ui.MplWidget.canvas.axes.set_ylim([ymin,ymax])
                    self.apy_ui.MplWidget.canvas.draw()
                ###
                else:
                    xaray = np.arange(xmin, xmax, 0.001)
                    md = []
                    cnt = 0
                    cnt2 = 0
                    y = []
                    if referencia == 'None':
                        x0 = [ppm for ppm in ppm_x]
                    else:
                        x0 = [abs(ppm - referencia) for ppm in ppm_x]
                    x0.sort()
                    if len(x0) == 1: #LISTA COM 1 PPM
                        for xx in xaray:
                            y.append((A * (width ** 2)) / (width ** 2 + (4 * (x0[0] - xx) ** 2)))

                        self.apy_ui.MplWidget.canvas.axes.clear()
                        self.apy_ui.MplWidget.canvas.axes.plot(xaray, y)
                        self.apy_ui.MplWidget.canvas.axes.set_ylim([ymin, ymax])
                        self.apy_ui.MplWidget.canvas.axes.set_xlim([xmax, xmin])
                        self.apy_ui.MplWidget.canvas.axes.set_xlabel('ppm')
                        self.apy_ui.MplWidget.canvas.draw()

                    elif len(x0) == 2: #LISTA COM 2 PPM
                        md.append(round((x0[0] + x0[1]) / 2, 2))  # calculo a média nesse caso só vai ter 1 valor
                        for xx in xaray:
                            y.append((A * (width ** 2)) / (
                                        width ** 2 + (4 * (round(x0[cnt], 3) - round(xx, 3)) ** 2)))  # faço a conta

                            if round(xx, 2) == md[0]:  # qnd o x chegar na média, sobe o contador
                                cnt += 1
                                if cnt > 1:  # como a lista de x0 só tem 2 elementos, o contador nao pode passar de 1
                                    cnt = 1  # entao eu mantenho ele sempre em 1

                        yhat = savgo(y, 51, suav)
                        self.apy_ui.MplWidget.canvas.axes.clear()
                        self.apy_ui.MplWidget.canvas.axes.plot(xaray, yhat)
                        self.apy_ui.MplWidget.canvas.axes.set_ylim([ymin, ymax])
                        self.apy_ui.MplWidget.canvas.axes.set_xlim([xmax, xmin])
                        self.apy_ui.MplWidget.canvas.axes.set_xlabel('ppm')
                        self.apy_ui.MplWidget.canvas.draw()

                    else: #AQUI É PRA LISTA MAIOR Q 2 PPM
                        for tensor in range(len(x0)):
                            if tensor == len(x0) - 1:
                                break
                            else:
                                md.append(round((x0[tensor] + x0[tensor + 1]) / 2, 2))

                        for xx in xaray:  # percorro cada item do vetor
                            y.append((A * (width**2)) / (width**2 + (4*(round(x0[cnt], 3) - round(xx, 3))**2)))
                            if round(xx, 2) == md[cnt2]:  # qnd o x chegar na média sobe os 2 contadores (contador da lista média e da lista x0)
                                cnt2 += 1
                                cnt += 1
                                if cnt2 > len(md) - 1:  # se o contador da média for maior que a lista da média eu zero ele
                                    cnt2 = 0

                        yhat = savgo(y, 51, suav)

                        self.apy_ui.MplWidget.canvas.axes.clear()
                        self.apy_ui.MplWidget.canvas.axes.plot(xaray, yhat)
                        self.apy_ui.MplWidget.canvas.axes.set_ylim([ymin, ymax])
                        self.apy_ui.MplWidget.canvas.axes.set_xlim([xmax, xmin])
                        self.apy_ui.MplWidget.canvas.axes.set_xlabel('ppm')
                        self.apy_ui.MplWidget.canvas.draw()
                    ####

            except ValueError:
                csGA_QMBox = QMessageBox()
                csGA_QMBox.setIcon(QMessageBox.Critical)
                csGA_QMBox.setWindowTitle('Error')
                csGA_QMBox.setText('Its necessary calculated Gipaw first or import output')
                csGA_QMBox.exec()

        except TypeError:
            pass

    def scfPlot(self):
        grep_iter = subprocess.getoutput(
            "grep '     total energy  ' {}pwgrep".format(self.tmp_dir))  # pegando o grep
        lst = [x for x in grep_iter.split('=')]  # quebrando pelo sinal de =
        lst2 = lst[1:]  # pegando do segundo elemento pra frente, pq só tem os numeros e mais algumas coisas
        strlst = ''.join(lst2)  # transformando em string
        lst3 = strlst.split('total energy')  # cortando total energy, o retorno é uma lista
        strlst2 = ''.join(lst3)  # voltando pra string para poder manipular
        lst4 = strlst2.split('Ry')  # Manipulando a string strlst2 pra cortar os Ry o retorno é uma lista
        strlst3 = ''.join(lst4)  # voltando pra string para poder manipular
        lst5 = [float(y) for y in strlst3.split()]  # ja pega somente as energias
        cnt = 0  # contar as iterações
        grep_final = []  # pegar o formato certo do texto a ser printado na tela
        for gf in lst5:
            cnt = cnt + 1  # numeros de iterações
            grep_final.append('Iteration {}:  Energy  =  {:5f} Ry\n'.format(cnt, gf))  # formato do texto
        iterations = len(grep_final)    #pegando quantas iterações tem
        text_scf = ''.join(grep_final)  #transformando a lista bruta em str
        lst6 = [z for z in text_scf.split('=')] #quebrando por igual
        strlst4 = ''.join(lst6) #str
        r_iter = strlst4.replace('Iteration', '') #excluindo
        r_energy = r_iter.replace('Energy', '') #excluindo
        r_ry = r_energy.replace('Ry', '')#excluindo
        r_dot = r_ry.replace(':', '') #excluindo
        get_scf_xy = [float(xy) for xy in r_dot.split()] #aqui o arquivo ja está mais limpo, é só quebrar por espaços
        get_scf_y = get_scf_xy[1::2]    #as posições impares são as iterações e pares as energias, GERA AS POSIÇÕES Y
        get_scf_x = [xxx for xxx in range(1,iterations + 1)]    #Gera as posições x

        self.apy_ui.MplWidget.canvas.axes.clear()
        self.apy_ui.MplWidget.canvas.axes.plot(get_scf_x, get_scf_y)
        self.apy_ui.MplWidget.canvas.axes.set_ylabel('Energy (Ry)')
        self.apy_ui.MplWidget.canvas.axes.set_xlabel('Iterations')
        # self.apy_ui.MplWidget.canvas.axes.set_ylim([ymin, ymax])
        # self.apy_ui.MplWidget.canvas.axes.set_xlim([xmax, xmin])
        self.apy_ui.MplWidget.canvas.draw()

    def resetSpec(self):
        self.apy_ui.MplWidget.canvas.axes.clear()
        self.apy_ui.MplWidget.canvas.axes.set_ylim(-0.1, 2)
        self.apy_ui.MplWidget.canvas.axes.set_xlim(10, 0)
        self.apy_ui.MplWidget.canvas.draw()


