# -*- coding: utf-8 -*-
"""
Created on Wed May 18 07:53:49 2016

@author: stephen
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

#y1 = np.load('C8-1.4.npy')
#y2 = np.load('C8-1.npy')
#y3 = np.load('C20-1.npy')

x = [2,3,4,5,6,7,8,9]

string_name1 = 'Mesh_8xtestx20_C3D8R_1.0_vm.npy'
string_name2 = 'Mesh_8xtestx20_C3D8R_1.4_vm.npy'
string_name3 = 'Mesh_8xtestx20_C3D8F_1.0_vm.npy'
string_name4 = 'Mesh_8xtestx20_C3D8F_1.4_vm.npy'
string_name5 = 'Mesh_8xtestx20_C3D20R_1.0_vm.npy'
string_name6 = 'Mesh_8xtestx20_C3D20R_1.4_vm.npy'
string_name7 = 'Mesh_8xtestx20_C3D20F_1.0_vm.npy'
string_name8 = 'Mesh_8xtestx20_C3D20F_1.4_vm.npy'

y1 = np.load(string_name1,allow_pickle = True)
y2 = np.load(string_name2,allow_pickle = True)
y3 = np.load(string_name3,allow_pickle = True)
y4 = np.load(string_name4,allow_pickle = True)
y5 = np.load(string_name5,allow_pickle = True)
y6 = np.load(string_name6,allow_pickle = True)
y7 = np.load(string_name7,allow_pickle = True)
y8 = np.load(string_name8,allow_pickle = True)

plt.figure(1)
plt.plot(x,y1, label='C3D8R; r = 1.0', lw=2)
plt.plot(x,y2, label='C3D8R; r = 1.4', lw=2)
plt.plot(x,y3, label='C3D8F; r = 1.0', lw=2)
plt.plot(x,y4, label='C3D8F; r = 1.4', lw=2)
plt.plot(x,y5, label='C3D20R; r = 1.0', lw=2)
plt.plot(x,y6, label='C3D20R; r = 1.4', lw=2)
plt.plot(x,y7, label='C3D20F; r = 1.0', lw=2)
plt.plot(x,y8, label='C3D20F; r = 1.4', lw=2)

plt.xlabel('No. through thickness divisions')
plt.ylabel('Von Mises Stress MPa')
legend = plt.legend(loc='upper right', bbox_to_anchor=(1.5, 1))

plt.savefig('VM_refinement.png', format='png', dpi=1200)
plt.show()

string_name1 = 'Mesh_8xtestx20_C3D8R_1.0_pe.npy'
string_name2 = 'Mesh_8xtestx20_C3D8R_1.4_pe.npy'
string_name3 = 'Mesh_8xtestx20_C3D8F_1.0_pe.npy'
string_name4 = 'Mesh_8xtestx20_C3D8F_1.4_pe.npy'
string_name5 = 'Mesh_8xtestx20_C3D20R_1.0_pe.npy'
string_name6 = 'Mesh_8xtestx20_C3D20R_1.4_pe.npy'
string_name7 = 'Mesh_8xtestx20_C3D20F_1.0_pe.npy'
string_name8 = 'Mesh_8xtestx20_C3D20F_1.4_pe.npy'

y1_pe = np.load(string_name1,allow_pickle = True)
y2_pe = np.load(string_name2,allow_pickle = True)
y3_pe = np.load(string_name3,allow_pickle = True)
y4_pe = np.load(string_name4,allow_pickle = True)
y5_pe = np.load(string_name5,allow_pickle = True)
y6_pe = np.load(string_name6,allow_pickle = True)
y7_pe = np.load(string_name7,allow_pickle = True)
y8_pe = np.load(string_name8,allow_pickle = True)

fig = plt.figure(2)
fig, ax = plt.subplots()
plt.plot(x,y1_pe, label='C3D8R; r = 1.0', lw=2)
plt.plot(x,y2_pe, label='C3D8R; r = 1.4', lw=2)
plt.plot(x,y3_pe, label='C3D8F; r = 1.0', lw=2)
plt.plot(x,y4_pe, label='C3D8F; r = 1.4', lw=2)
plt.plot(x,y5_pe, label='C3D20R; r = 1.0', lw=2)
plt.plot(x,y6_pe, label='C3D20R; r = 1.4', lw=2)
plt.plot(x,y7_pe, label='C3D20F; r = 1.0', lw=2)
plt.plot(x,y8_pe, label='C3D20F; r = 1.4', lw=2)

ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))

plt.xlabel('No. through thickness divisions')
plt.ylabel('Creep Strain ')
legend = plt.legend(loc='upper right', bbox_to_anchor=(1.5, 1))

plt.savefig('PE_refinement.png', format='png', dpi=1200)
plt.show()