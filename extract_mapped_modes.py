#!/usr/bin/env python

## \file compute_polar_modes.py
#  \brief Polar computation using the FSI tools, with different mode amplitudes.
#  \version 7.1.0 "Blackbird"
#
# SU2 Project Website: https://su2code.github.io
#
# The SU2 Project is maintained by the SU2 Foundation
# (http://su2foundation.org)
#
# Copyright 2012-2020, SU2 Contributors (cf. AUTHORS.md)
#
# SU2 is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# SU2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with SU2. If not, see <http://www.gnu.org/licenses/>.
#
#
# Author: Nicola Fonzi

import numpy as np
import os
import shutil

def main():

    # Main variables
    Modes = [ i for i in range(3)]
    NumbProc = 38
    HOME = os.getcwd()
    FluidCfg = HOME+"/fluid.cfg"
    SolidCfg = HOME+"/solid.cfg"
    FsiCfg = HOME+"/fsi.cfg"
    MeshFile = HOME+"/airfoil.su2"
    PchFile = HOME+"/modal.pch"
    MeshFileNastran = HOME+"/modal.f06"


    # Initialisation
    writeFluidCfg(FluidCfg)
    writeFsiCfg(FsiCfg)
    for mode in Modes:
        writeSolidCfg(mode,SolidCfg)
        HOMEMODE = os.getcwd()+"/Mode={:2.1f}".format(mode)
        os.mkdir(HOMEMODE)
        shutil.copyfile(FluidCfg,HOMEMODE+"/fluid_new.cfg")
        shutil.copyfile(SolidCfg,HOMEMODE+"/solid_new.cfg")
        shutil.copyfile(MeshFile,HOMEMODE+"/airfoil.su2")
        shutil.copyfile(FsiCfg,HOMEMODE+"/fsi.cfg")
        shutil.copyfile(MeshFileNastran,HOMEMODE+"/modal.f06")
        shutil.copyfile(PchFile,HOMEMODE+"/modal.pch")
        os.chdir(HOMEMODE)
        os.system("mpirun -np {} python3 /scratch/aero/nfonzi/SU2/bin/fsi_computation.py --parallel -f fsi.cfg > log.txt".format(int(NumbProc)))
        os.chdir(HOME)

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def writeFluidCfg(FluidCfg):
    line_num = 0
    with open(FluidCfg) as configfile:
      while 1:
        line = configfile.readline()
        if not line:
          break
        pos = line.find('INNER_ITER')
        if pos  >=  0:
          break
        line_num = line_num + 1
    replace_line(FluidCfg,line_num,"INNER_ITER = 1 \n")
    line_num = 0
    with open(FluidCfg) as configfile:
      while 1:
        line = configfile.readline()
        if not line:
          break
        pos = line.find('TIME_ITER')
        if pos  >=  0:
          break
        line_num = line_num + 1
    replace_line(FluidCfg,line_num,"TIME_ITER = 1 \n")
    line_num = 0
    with open(FluidCfg) as configfile:
      while 1:
        line = configfile.readline()
        if not line:
          break
        pos = line.find('TIME_STEP')
        if pos  >=  0:
          break
        line_num = line_num + 1
    replace_line(FluidCfg,line_num,"TIME_STEP = 0.001 \n")

def writeFsiCfg(FluidCfg):
    line_num = 0
    with open(FluidCfg) as configfile:
      while 1:
        line = configfile.readline()
        if not line:
          break
        pos = line.find('UNST_TIME')
        if pos  >=  0:
          break
        line_num = line_num + 1
    replace_line(FluidCfg,line_num,"UNST_TIME = 0.001 \n")
    line_num = 0
    with open(FluidCfg) as configfile:
      while 1:
        line = configfile.readline()
        if not line:
          break
        pos = line.find('UNST_TIMESTEP')
        if pos  >=  0:
          break
        line_num = line_num + 1
    replace_line(FluidCfg,line_num,"UNST_TIMESTEP = 0.001 \n")

def writeSolidCfg(mode,SolidCfg):
    line_num = 0
    with open(SolidCfg) as configfile:
      while 1:
        line = configfile.readline()
        if not line:
          break
        pos = line.find('INITIAL_MODES')
        if pos  >=  0:
          break
        line_num = line_num + 1
    replace_line(SolidCfg,line_num,"INITIAL_MODES = {"+str(int(mode))+":1.0}\n")


if __name__ == '__main__':
    main()
