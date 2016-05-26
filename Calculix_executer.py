# -*- coding: utf-8 -*-
"""
Created on Thu May  5 08:59:18 2016

@author: spookfish
"""

import numpy as np
import subprocess as sp
import os
import pandas as pd
import re
import matplotlib.pyplot as plt

from Pipe_Mesh_Function import pipe_mesh
from Read_frd import readfrd
from Aux_results import Aux_results

length = 8
thickness = 1
radial = 10
n = 2*radial

section = 2
r = 1.4

quad = 1
reduced = 0

direc = "Tests/"

if quad == 1:
    elestr = "C3D20"
else:
    elestr = "C3D8"
if reduced == 1:
    interstr = "R"
else:
    interstr = "F"

num_tests = 1
Dall_max = np.zeros((num_tests))
Von_Mises_max = np.zeros((num_tests))

for i in range(num_tests):
    
    thickness = i + 4

    pipe_mesh(direc,length, thickness, radial, section, r, quad, reduced)
    
    #meshfile = direc+"Mesh_" + str(length) + "x" + str(thickness) + "x" + str(2*radial) + "_" + elestr +interstr +".inp"
        
    os.system("/home/spookfish/CalculiXLauncher-02/bin/ccx29 /home/spookfish/Projects/Masters/Calculix_PipeMesher/Tests/Test2")
    #os.system("/home/stephen/Documents/CalculiXLauncher-02/bin/ccx29 /home/stephen/Projects/Calculix_PipeMesher/Tests/Test")
    
    
    resultsfile = direc+'Test2.frd'
    selecttime = None
    
    time,disps,temps,stresses,strains = readfrd(resultsfile)
    
    Dall, Von_Mises, Principal = Aux_results(time,disps,temps,stresses,strains)
    
    
    disps_df = pd.DataFrame(disps, columns=['Time', 'Node', 'dx', 'dy', 'dz'])
    temps_df = pd.DataFrame(temps, columns=['Time', 'Node', 'T'])
    stresses_df = pd.DataFrame(stresses, columns=['Time', 'Node', 'Sxx', 'Syy', 'Szz', 'Sxy', 'Sxz', 'Syz'])
    strains_df = pd.DataFrame(strains, columns=['Time', 'Node', 'Exx', 'Eyy', 'Ezz', 'Exy', 'Exz', 'Eyz'])
    
    Dall_df = pd.DataFrame(Dall, columns=['Time', 'Node', 'Utot'])
    Von_Mises_df = pd.DataFrame(Von_Mises, columns=['Time', 'Node', 'Von Mises Stress'])
    Principal_df = pd.DataFrame(Principal, columns=['Time', 'Node', 'P1','P2','P3'])
    
    Dall_max[i] = Dall_df.loc[Dall_df['Time'] == 600]['Utot'].max()
    Von_Mises_max[i] = Von_Mises_df.loc[Von_Mises_df['Time'] == 600]['Von Mises Stress'].max()
    
#plt.plot(Von_Mises_max)
        
string_name = "Mesh_" + str(length) + "x" + "test" + "x" + str(n) + "_"+ elestr +interstr+"_"+str(r)

np.save(string_name,Von_Mises_max,allow_pickle = True)

