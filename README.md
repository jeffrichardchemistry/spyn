[![DOI](https://zenodo.org/badge/225914130.svg)](https://zenodo.org/badge/latestdoi/225914130)

# Spyn
Its a software for conformational search, Boltzmann calculations, solid-state nuclear magnetic resonance (ssNMR) with the theory GIPAW and plot for visualization outputs spectra. The source code is all free in the tar.gz file.

This software works in Linux's environments. Was tested in debian's distributions: Debian 10, Linux mint 19.3, Linux Ubuntu 18.04 LTS and Elementary OS 5.1

# Install
1º - Download and unzip.

2º - cd ../Spyn_1.0_alpha 

3º - python3 install_ui.py.

4º - Will be install some dependencies, type the root password.

5º - Choose a directory to install, then press INSTALL.

6º - A terminal will open with the installation step by step, if necessary enter the root password.

# Setting externally 
In case of errors in installation, try install dependencies on a terminal.

Repositories Debian's - dependencies:

- gawk, gfortran, openmpi-bin, openmpi-doc, libopenmpi-dev, xterm, openbabel, jmol, python3-dev, python3-pip, python3-pyqt5

Python dependencies:

- PyQt5, matplotlib, pandas, scipy, numpy

This software use a module of Quantum-Espresso(QE) to performe GIPAW calculations, In case of errors in installation, its possible install QE externaly, then create a simbolic link for executable <b>pw.x</b> with name <b>pw</b> and another simbolic link for executable <b>gipaw.x</b> with name <b>gipaw</b>, thus, its possible to use any version of QE. The default version of QE in spyn is 6.3. 
Any information about Quantum-Espresso can be found in: https://www.quantum-espresso.org/

# Non Debians distributions
For systems not derived from debian, it is possible to install only externally, i.e, install the dependencies on a terminal, and then extract the tar.gz file and execute the spyn.sh file.
