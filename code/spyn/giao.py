import subprocess
from direct import Dirs
from dir import get_dir

class giaoMethods(Dirs, get_dir):
    def __init__(self):
        get_dir.__init__(self)

    def inGiao(self):
        get_dir.getopenAll(self) #uso pra pegar o diretorio/arquivo
        subprocess.run('obabel {} -O {}gausin.com'.format(self.open_file,self.tmp_dir),shell=True) #rodo o gerador de input

        get_namefile = [y for y in self.open_file.split('/')] #percorro a string com o diretorio separando por barra
        title = get_namefile[-1][:-4] #pra pegar somente o nome
        parameters = """%chk={}.chk\n%mem=6GB\n%nprocshared=3\n#P b3lyp/cc-pvtz nmr=giao maxdisk=-1\n\n {}\n\n""".format(
            title, title) #cabeçalho do input

        with open('{}gausin.com'.format(self.tmp_dir), 'r') as f:   #Abro o arquivo e leio jogando o texto para uma variavel
            fread = f.read()

        lst1 = [x for x in fread.splitlines()]  #percorro o texto para separar as linhas em um item da matriz e assim excluir as primeiras
        del lst1[0:4]
        del_firlines = '\n'.join(lst1) #transformo em string de novo

        input_gaussian = parameters + del_firlines          #concateno as coordenadas com o cabeçalho
        self.apy_ui.txt_log_show.setText(input_gaussian)