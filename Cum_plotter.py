# -*- coding: utf-8 -*-
"""
Created on Mon May 30 17:22:34 2016

@author: spookfish
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
from matplotlib.ticker import ScalarFormatter


x = [2,3,4,5,6,7,8,9]
string_name_pedf = 'Mesh_8xtestx20_C3D20F_1.4_pe_12480.0'
string_name_pedf2 = 'Mesh_8xtestx20_C3D20F_1.4_pe_10800.0'
string_name_pedf3 = 'Mesh_8xtestx20_C3D20F_1.4_pe_7800.0'

PE_plot = pd.read_pickle(string_name_pedf)
PE_plot2 = pd.read_pickle(string_name_pedf2)
PE_plot3 = pd.read_pickle(string_name_pedf3)


fig, ax = plt.subplots()
plt.plot(PE_plot['Time'],PE_plot['PE'], lw=2)
#plt.plot(PE_plot2['Time'],PE_plot2['PE'], label='2.89 K/min', lw=2)
#plt.plot(PE_plot3['Time'],PE_plot3['PE'], label='4.00 K/min', lw=2)
plt.ylabel('Creep Strain')
plt.xlabel('Time(s)')
#legend = ax.legend(loc='upper left')
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))
plt.savefig('Cum_creep.png', format='png', dpi=1200, bbox_inches='tight')
plt.show()