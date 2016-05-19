# -*- coding: utf-8 -*-
"""
Created on Wed May 18 07:53:49 2016

@author: stephen
"""

import numpy as np
import matplotlib.pyplot as plt

#y1 = np.load('C8-1.4.npy')
#y2 = np.load('C8-1.npy')
#y3 = np.load('C20-1.npy')

x = [2,3,4,5,6,7,8,9]

string_name1 = 'Mesh_8xtestx20_C3D8R_1.npy'
string_name2 = 'Mesh_8xtestx20_C3D8R_1.4.npy'
string_name3 = 'Mesh_8xtestx20_C3D8F_1.npy'
string_name4 = 'Mesh_8xtestx20_C3D8F_1.4.npy'
string_name5 = 'Mesh_8xtestx20_C3D20R_1.npy'
string_name6 = 'Mesh_8xtestx20_C3D20R_1.4.npy'
string_name7 = 'Mesh_8xtestx20_C3D20F_1.npy'
string_name8 = 'Mesh_8xtestx20_C3D20F_1.4.npy'

y1 = np.load(string_name1,allow_pickle = True)
y2 = np.load(string_name2,allow_pickle = True)
y3 = np.load(string_name3,allow_pickle = True)
y4 = np.load(string_name4,allow_pickle = True)
y5 = np.load(string_name5,allow_pickle = True)
y6 = np.load(string_name6,allow_pickle = True)
y7 = np.load(string_name7,allow_pickle = True)
y8 = np.load(string_name8,allow_pickle = True)

plt.figure(1)
plt.plot(x,y1, label='Line 1')
plt.plot(x,y2, label='Line 2')
plt.plot(x,y3, label='Line 3')
plt.plot(x,y4, label='Line 4')
plt.plot(x,y5, label='Line 5')
plt.plot(x,y6, label='Line 6')
plt.plot(x,y7, label='Line 7')
plt.plot(x,y8, label='Line 8')

legend = plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))