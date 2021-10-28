import subprocess
from direct import Dirs

class Clear(Dirs):
    def __init__(self):
        Dirs.__init__(self)

    def clearTxt(self):
        self.apy_ui.txt_log_show.clear()
        self.apy_ui.txt_conformer_show.clear()
        self.apy_ui.txt_energy_show.clear()
        self.apy_ui.txt_pwin.clear()
        self.apy_ui.txt_pwout.clear()
        self.apy_ui.txt_gipaw.clear()

    def clearTmp(self):
        subprocess.run('rm -rf {}*'.format(self.tmp_dir), shell=True)