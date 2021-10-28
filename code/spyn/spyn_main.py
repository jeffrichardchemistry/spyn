# -*- coding: utf-8 -*-
import sys
import subprocess
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QWidget, QTableWidgetItem,QMessageBox, QSplashScreen, QProgressBar
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QProcess, Qt
from PyQt5.QtGui import QPixmap
from spyn_ui import Ui_spyn_mainwindow
from boltz import boltzd
from csGA import csGA
from dir import get_dir
from direct import Dirs
from energy import energy
from pwscfnmr import qe
from clear import Clear
from grepout import grepoutput
from giao import giaoMethods
from plots import allPlots
from killprocess import killProcess
from imports import importAll
from stylesprogbar import layoutsProgbar
from scipy.signal import savgol_filter as savgo
import pandas as pd
import numpy as np
import time

class spyn_main(QMainWindow, QWidget):
    def __init__(self):
        super(spyn_main, self).__init__()
        spyn_main.initMAIN(self)
    
    def initMAIN(self):
        QMainWindow.__init__(self)
        Dirs.__init__(self) #pegando construtor da Dirs
        get_dir.__init__(self) #pegando construtor da get_dir
        energy.__init__(self) #pegando o contrutor da energy
        qe.__init__(self) #pegando o construtor do qe
        csGA.__init__(self)
        self.setWindowIcon(QtGui.QIcon('{}/spyn.png'.format(self.dir_images)))
        

        self.apy_ui = Ui_spyn_mainwindow() #carregando a classe da ui
        self.apy_ui.setupUi(self) #pegando os métodos
        self.apy_ui.progbar.setHidden(True) #escondendo a barra de prog
        self.apy_ui.progbar_qe.setHidden(True) #escondendo a barra de prog

        self.bash_top = QProcess(self)
            
        #Toolbar
        toolbar_open = QAction(QtGui.QIcon('{}/import.svg'.format(self.dir_images)), 'Open File for conformer searching calculation', self) #toolbutton open
        toolbar_open.triggered.connect(self.open_from_menu)
        toolbar_run_cs_ga = QAction(QtGui.QIcon('{}/Run_GA.png'.format(self.dir_images)), 'Run conformer searching for genetic algorithm', self)    #toolbutton csga calc
        toolbar_run_cs_ga.triggered.connect(self.run_CS_GA)
        toolbar_csenergy = QAction(QtGui.QIcon('{}/energy.svg'.format(self.dir_images)), 'Calculate conformers energy from genetic algorithm', self)  # toolbutton open
        toolbar_csenergy.triggered.connect(self.run_energy_GA)
        toolbar_export_cs = QAction(QtGui.QIcon('{}/export2.svg'.format(self.dir_images)), 'Export Energy', self)
        toolbar_export_cs.triggered.connect(self.export_energy_csga_all)
        toolbar_runboltz = QAction(QtGui.QIcon('{}/boltzmann.svg'.format(self.dir_images)), 'Calculate boltzmann distribution from the energy of the conformers', self)
        toolbar_runboltz.triggered.connect(self.boltzcalc)
        toolbar_pwout = QAction(QtGui.QIcon('{}/pwout.svg'.format(self.dir_images)), 'Run input and output of pwscf calculations', self)
        toolbar_pwout.triggered.connect(self.pw_output)
        toolbar_gipaw = QAction(QtGui.QIcon('{}/gipaw.svg'.format(self.dir_images)),
                                'Run gipaw calculations', self)
        toolbar_gipaw.triggered.connect(self.gipaw)
        toolbar_grepscf = QAction(QtGui.QIcon('{}/grep.svg'.format(self.dir_images)), 'Filter scf output', self)
        toolbar_grepscf.triggered.connect(self.grepScf)
        toolbar_grepgipaw = QAction(QtGui.QIcon('{}/grepgipaw.svg'.format(self.dir_images)), 'Filter gipaw output', self)
        toolbar_grepgipaw.triggered.connect(self.grepGipaw)
        toolbar_stoppwout = QAction(QtGui.QIcon('{}/stop_pwout.svg'.format(self.dir_images)), 'Stop process of pwscf calculations', self)
        toolbar_stoppwout.triggered.connect(self.stopPwout)
        toolbar_stopgipaw = QAction(QtGui.QIcon('{}/stop_pwout.svg'.format(self.dir_images)),
                                    'Stop process of gipaw calculations', self)
        toolbar_stopgipaw.triggered.connect(self.stopGipaw)
        toolbar_cleartxt = QAction(QtGui.QIcon('{}/eraser.svg'.format(self.dir_images)), 'Clear all text fields', self)
        toolbar_cleartxt.triggered.connect(self.clearTxt)
        toolbar_terminal = QAction(QtGui.QIcon('{}/bash.png'.format(self.dir_images)), 'Open a bash terminal with all process running', self)
        toolbar_terminal.triggered.connect(self.terminal)
        toolbar_cleartmp = QAction(QtGui.QIcon('{}/clear.png'.format(self.dir_images)), 'Clear all tmp files', self)
        toolbar_cleartmp.triggered.connect(self.clearTmp)
        self.toolbar = self.addToolBar("Extraction")    #create the toolbar
        self.toolbar.addAction(toolbar_open)            #link between toolbar and buttons
        self.toolbar.addAction(toolbar_run_cs_ga)
        self.toolbar.addAction(toolbar_csenergy)
        self.toolbar.addAction(toolbar_export_cs)
        self.toolbar.addAction(toolbar_runboltz)
        self.toolbar.addAction(toolbar_pwout)
        self.toolbar.addAction(toolbar_gipaw)
        self.toolbar.addAction(toolbar_grepscf)
        self.toolbar.addAction(toolbar_grepgipaw)
        self.toolbar.addAction(toolbar_stoppwout)
        self.toolbar.addAction(toolbar_stopgipaw)
        self.toolbar.addAction(toolbar_terminal)
        self.toolbar.addAction(toolbar_cleartxt)
        self.toolbar.addAction(toolbar_cleartmp)
        #Menubar
        self.apy_ui.menu_open.triggered.connect(self.open_from_menu)
        self.apy_ui.menu_quit.triggered.connect(self.close)
        self.apy_ui.menu_giao.triggered.connect(self.inGiao)
        self.apy_ui.menu_ConformersOut.triggered.connect(self.importConfs)
        self.apy_ui.menu_GipawOut.triggered.connect(self.importGipawout)
        self.apy_ui.menu_Giaoout.triggered.connect(self.importGiaoout)
        self.apy_ui.menu_runCSGA.triggered.connect(self.run_CS_GA)
        self.apy_ui.menu_runPWscf_input.triggered.connect(self.pw_input)
        self.apy_ui.menu_runPWscf_output.triggered.connect(self.pw_output)
        self.apy_ui.menu_runGipaw.triggered.connect(self.gipaw)
        self.apy_ui.menu_PWscfOut.triggered.connect(self.importPWscfout)
        self.apy_ui.menu_nmrexpCSV.triggered.connect(self.plotEXPcsv)
        #botoes
        self.apy_ui.btn_GA_run.clicked.connect(self.run_CS_GA)
        self.apy_ui.btn_energy_GA_run.clicked.connect(self.run_energy_GA)
        self.apy_ui.btn_pwin.clicked.connect(self.pw_input)
        self.apy_ui.btn_pwout.clicked.connect(self.pw_output)
        self.apy_ui.btn_lowerenergies.clicked.connect(self.run_tables)
        self.apy_ui.btn_gipaw.clicked.connect(self.gipaw)
        self.apy_ui.btn_exportConformers.clicked.connect(self.exportCSGA)
        self.apy_ui.btn_overlapConfs.clicked.connect(self.plotOverlap)
        self.apy_ui.btn_nmrgraphGIPAW.clicked.connect(self.plotGipawcalc)
        self.apy_ui.btn_pwscfPLOT.clicked.connect(self.plotPWscf)
        self.apy_ui.btn_plotMANUAL.clicked.connect(self.plotGipawManual)
        self.apy_ui.btn_resetPLOT.clicked.connect(self.resetSpec)
        self.apy_ui.btn_gerar_tables.clicked.connect(self.boltztable)
        self.apy_ui.txt_nconfboltz.returnPressed.connect(self.boltztable)
        self.apy_ui.btn_run_boltz.clicked.connect(self.boltzcalc)
        self.apy_ui.btn_automaticBoltz.clicked.connect(self.boltzAutomatic)
        self.apy_ui.btn_nmrgraphGIAO.clicked.connect(self.plotGiao)

        #Checkbox
        self.apy_ui.chk_kauto.stateChanged.connect(self.clickBox)
        self.apy_ui.chkbox_overlapALL.stateChanged.connect(self.checkBox_overlap)
        self.apy_ui.chkbox_threadsnmr.stateChanged.connect(self.threads)

    def threads(self):
        qe.threads(self)

    def resetSpec(self):
        allPlots.resetSpec(self)
    
    def plotGiao(self):
        allPlots.plotGiao(self)
              
    def importGiaoout(self):
        importAll.importGiaoout(self)

    def importPWscfout(self):
        importAll.importPWscfout(self)
        
    def importGipawout(self):
        importAll.importGipawout(self)        

    def importConfs(self):
        importAll.importConfs(self)        

    def plotEXPcsv(self):
        dir_expcsv, _ = QtWidgets.QFileDialog.getOpenFileName(self,'Open a NMR spectro','','csv (*.csv)')
        
        filenmr = pd.read_csv(dir_expcsv)
        cols = filenmr.columns #pego o nome das colunas
        df = filenmr.rename(columns={cols[0]:1, cols[1]:2}) #renomeio o nome das colunas
        
        self.apy_ui.MplWidget.canvas.axes.set_xlim(max(df[1]), min(df[1]))
        self.apy_ui.MplWidget.canvas.axes.plot(df[1],df[2])
        self.apy_ui.MplWidget.canvas.draw()
    
    def plotGipawManual(self):
        allPlots.plotGipawManual(self)

    def getToolsplot(self):
        allPlots.getToolsplot(self)

    def plotPWscf(self):
        allPlots.scfPlot(self)

    def plotGipawcalc(self):
        allPlots.plotGipawcalc(self)

    def checkBox_overlap(self):
        csGA.checkBox_overlap(self)

    def plotOverlap(self):
        if csGA.checkBox_overlap(self) == 2: #rodo a função da checkbox, pra saber se está selecionada
            spyn_main.plotAllconfs(self)
        else:
            spyn_main.plotConfs(self)

    def plotAllconfs(self):
        csGA.plotAllconfs(self)

    def plotConfs(self):
        csGA.plotConfs(self)

    def exportCSGA(self):
        csGA.exportCSGA(self)

    def terminal(self):
        killProcess.terminal(self)

    def stopPwout(self):
        killProcess.stopPwout(self)

    def stopGipaw(self):
        killProcess.stopGipaw(self)

    def scfPlot(self):
        allPlots.scfPlot(self)

    def clearTxt(self):
        Clear.clearTxt(self)

    def clearTmp(self):
        Clear.clearTmp(self)

    def run_tables(self):
        energy.runTables(self)

    def boltztable(self):
        boltzd.onpressed(self)

    def boltzcalc(self):
        boltzd.calcboltz(self)

    def boltzAutomatic(self):
        boltzd.boltzAutomatic(self)

    def open_from_menu(self):
        get_dir.open_from_menu(self)

    def run_CS_GA(self):
        csGA.run_CS_GA(self)

    def run_energy_GA(self):
        energy.calcEnergy(self)

    def export_energy_csga_all(self):
        energy.export_energy_GA(self)

    def clickBox(self):
        qe.clickBoxx(self)

    def pw_input(self):
        qe.pw_input(self)

    def pw_output(self):
        qe.pw_output(self)

    def gipaw(self):
        qe.gipaw(self)

    def grepScf(self):
        grepoutput.grepScf(self)

    def grepGipaw(self):
        grepoutput.grepGipaw(self)

    def inGiao(self):
        giaoMethods.inGiao(self)        

    def splash(self):        
        #splash_pix = QPixmap('{}/splash.png'.format(self.dir_images))
        ######### TEMPLATES
        style1, style2, style3, style4, style5, style6, style7 = layoutsProgbar.stylesProgbar(self)            
        ########
        splash_pix = QPixmap('{}/logo4.png'.format(self.dir_images))

        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        splash.setEnabled(False)
        
        # splash = QSplashScreen(splash_pix)
        # adding progress bar
        progressBar_splash = QProgressBar(splash)
        progressBar_splash.setMaximum(10)
        progressBar_splash.setGeometry(40, splash_pix.height() - 20, splash_pix.width() - 85, 17) #(Movimento em x, Movimento em Y, Largura da progbar, Altura da progbar)        
        progressBar_splash.setStyleSheet(style6)
 
        splash.setMask(splash_pix.mask())
        
        splash.show()
        #splash.showMessage("<h1><font color='green'>Welcome BeeMan!</font></h1>", Qt.AlignTop | Qt.AlignCenter, Qt.black)
        
        for i in range(1, 11):
            progressBar_splash.setValue(i)
            t = time.time()
            while time.time() < t + 0.1:
                app.processEvents()

        # Simulate something that takes time
        #time.sleep(5)        
        splash.finish(gui)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = spyn_main()
    gui.splash()
    gui.show()   
    
    sys.exit(app.exec_())

