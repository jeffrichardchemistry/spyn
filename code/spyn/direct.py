import subprocess
class Dirs():
    def __init__(self):
        self.pwd = subprocess.getoutput('pwd')
        self.diroutput_cs = '{}/tmp/output.sdf'.format(self.pwd)
        self.dirscript_conf = '{}/scripts/conformer_order.sh'.format(self.pwd)
        self.dir_images = '{}/fig'.format(self.pwd)
        self.cif_pwscf = '{}/scripts/'.format(self.pwd)
        self.tmp_dir = '{}/tmp/'.format(self.pwd)
        self.pp_dir = '{}/pp/'.format(self.pwd)
