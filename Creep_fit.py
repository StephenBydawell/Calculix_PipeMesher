# -*- coding: utf-8 -*-
"""
Created on Sat May 28 10:04:57 2016

@author: spookfish
"""

import numpy as np
from scipy.optimize import curve_fit
from sklearn import datasets, linear_model
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.ticker import ScalarFormatter

e873 = []
s873 = []
e823 = []
s823 = []
e773 = []
s773 = []
A =[]
n = []

infile = open('Data1', 'r')

while True:
    
    line = infile.readline()
    
    if line == "":
        break
    
    line = line.replace(",", ".")
    splitline = line.split()
    e873.append(float(splitline[1]))
    s873.append(float(splitline[0]))
    
e873 = np.array(e873)/3600
s873 = np.array(s873)

Xtrain = np.log(s873)
Ytrain = np.log(e873)

slope, intercept, r_value, p_value, std_err = stats.linregress(Xtrain,Ytrain)

A.append(np.exp(intercept))
n.append(slope)

infile = open('Data2', 'r')

while True:
    
    line = infile.readline()
    
    if line == "":
        break
    
    line = line.replace(",", ".")
    splitline = line.split()
    e823.append(float(splitline[1]))
    s823.append(float(splitline[0]))
    
e823 = np.array(e823)/3600
s823= np.array(s823)

Xtrain = np.log(s823)
Ytrain = np.log(e823)

slope, intercept, r_value, p_value, std_err = stats.linregress(Xtrain,Ytrain)

A.append(np.exp(intercept))
n.append(slope)

infile = open('Data3', 'r')

while True:
    
    line = infile.readline()
    
    if line == "":
        break
    
    line = line.replace(",", ".")
    splitline = line.split()
    e773.append(float(splitline[1]))
    s773.append(float(splitline[0]))
    
e773 = np.array(e773)/3600
s773 = np.array(s773)

Xtrain = np.log(s773)
Ytrain = np.log(e773)

slope, intercept, r_value, p_value, std_err = stats.linregress(Xtrain,Ytrain)

A.append(np.exp(intercept))
n.append(slope)

A2 = [0]*3
n2 = [0]*3
n2[0] = 6.2
n2[1] = 6.2
n2[2] = 6.2
A2[0] = 6.0e-21
A2[2] = 1.0e-22
A2[1] = 4.0e-24

S1 = np.arange(180., 400., 2)
S2 = np.arange(220, 400., 2)
S3 = np.arange(250., 400., 2)
S11 = np.arange(60., 180., 2)
S22 = np.arange(60., 250., 2)
S33 = np.arange(60., 220., 2)

fig, ax = plt.subplots()
plt.loglog(s873,e873,'kd',label='T = 873K') 
plt.loglog(s823,e823,'bd',label='T = 823K') 
plt.loglog(s773,e773,'rd',label='T = 773K') 
plt.loglog(S1,A[0]*S1**(n[0]),'r-') 
plt.loglog(S2,A[1]*S2**(n[1]),'r-') 
plt.loglog(S3,A[2]*S3**(n[2]),'r-') 
plt.loglog(S11,A2[0]*S11**(n2[0]),'r-') 
plt.loglog(S22,A2[1]*S22**(n2[1]),'r-') 
plt.loglog(S33,A2[2]*S33**(n2[2]),'r-') 
plt.axis([60, 400,10e-11,10e-4])
ax.set_xticks([60, 80,100, 200, 300, 400])
ax.get_xaxis().set_major_formatter(ScalarFormatter())
plt.xlabel('Stress MPa')
plt.ylabel('Minimum creep rate 1/s')
legend = ax.legend(loc='upper left')
plt.savefig('Creep_X20.png', format='png', dpi=1200)
plt.show()


