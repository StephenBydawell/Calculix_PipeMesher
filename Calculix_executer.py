# -*- coding: utf-8 -*-
"""
Created on Thu May  5 08:59:18 2016

@author: spookfish
"""

import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import time

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
reduced = 1

direc = "Tests/"

if quad == 1:
    elestr = "C3D20"
else:
    elestr = "C3D8"
if reduced == 1:
    interstr = "R"
else:
    interstr = "F"

num_tests = 8
Dall_max = np.zeros((num_tests))
Von_Mises_max = np.zeros((num_tests))
PE_max = np.zeros((num_tests))
T = np.zeros((num_tests))

for i in range(num_tests):
    start = time.time()
    thickness = i + 2

    pipe_mesh(direc,length, thickness, radial, section, r, quad, reduced)
    
    #meshfile = direc+"Mesh_" + str(length) + "x" + str(thickness) + "x" + str(2*radial) + "_" + elestr +interstr +".inp"
        
    os.system("/home/spookfish/CalculiXLauncher-02/bin/ccx29 /home/spookfish/Projects/Masters/Calculix_PipeMesher/Tests/Test5")
    #os.system("/home/stephen/Documents/CalculiXLauncher-02/bin/ccx29 /home/stephen/Projects/Calculix_PipeMesher/Tests/Test")
    print "\nSystem solved."
    
    resultsfile = direc+'Test5.frd'
    selecttime = None
    
    timestamp,disps,temps,stresses,strains,pe = readfrd(resultsfile)
    
    Dall, Von_Mises, Principal = Aux_results(timestamp,disps,temps,stresses,strains)
    
    
    disps_df = pd.DataFrame(disps, columns=['Time', 'Node', 'dx', 'dy', 'dz'])
    temps_df = pd.DataFrame(temps, columns=['Time', 'Node', 'T'])
    stresses_df = pd.DataFrame(stresses, columns=['Time', 'Node', 'Sxx', 'Syy', 'Szz', 'Sxy', 'Sxz', 'Syz'])
    strains_df = pd.DataFrame(strains, columns=['Time', 'Node', 'Exx', 'Eyy', 'Ezz', 'Exy', 'Exz', 'Eyz'])
    PE_df = pd.DataFrame(pe, columns=['Time', 'Node', 'PE'])
    
    Dall_df = pd.DataFrame(Dall, columns=['Time', 'Node', 'Utot'])
    Von_Mises_df = pd.DataFrame(Von_Mises, columns=['Time', 'Node', 'Von Mises Stress'])
    Principal_df = pd.DataFrame(Principal, columns=['Time', 'Node', 'P1','P2','P3'])
    
    Dall_max[i] = Dall_df.loc[Dall_df['Time'] == timestamp]['Utot'].max()
    Von_Mises_max[i] = Von_Mises_df.loc[Von_Mises_df['Time'] == timestamp]['Von Mises Stress'].max()
    PE_max[i] = PE_df.loc[PE_df['Time'] == timestamp]['PE'].max()
    
    end = time.time()
    T[i] = (end - start)
#plt.plot(Von_Mises_max)
    print "\nTest finished in: " + str(T[i]) + " seconds."
        
string_name_vm = "Mesh_" + str(length) + "x" + "test" + "x" + str(n) + "_"+ elestr +interstr+"_"+str(r)+"_vm"
string_name_pe = "Mesh_" + str(length) + "x" + "test" + "x" + str(n) + "_"+ elestr +interstr+"_"+str(r)+"_pe"

np.save(string_name_vm,Von_Mises_max,allow_pickle = True)
np.save(string_name_pe,PE_max,allow_pickle = True)

