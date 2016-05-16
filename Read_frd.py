# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 12:29:09 2016

@author: stephen
"""

import numpy as np
import subprocess as sp
import os
import pandas as pd
import re

#os.system("/home/stephen/Documents/CalculiXLauncher-02/bin/ccx29 Test_v2.0")


#infile = open('Test_v2.0.frd', 'r')

#T_temps ={}
#T_disps = {}
#T_stresses = {}
#T_strain = {}

#resultsfile = 'Test_v2.0.frd'
#selecttime = None

#infile = open('Test_v2.0.frd', 'r')

def initiate(resultsfile):
    infile = open(resultsfile, 'r')
    return infile

#def readline(infile):
#    line = infile.readline()
#    while line == '\n':
#        line = infile.readline()
#    return line
    
def readchar(line):
    c = line
    parts = re.split("([IE]\+..|[IE]\-..)", c)
    
    shift = re.split("(-)", parts[0])
    for i in range(len(shift)):
        if shift[i] == '-':
            shift[i] = ' ' + shift[i]
    parts[0] = "".join(shift)
    
    for i in range(len(parts)):
        if parts[i][0] =='-':
            parts[i] = ' '+parts[i]
    #parts.insert(3, ' ')
    string= "".join(parts)
    split = string.split()
    return split

    
def skipline(infile,num):
    for i in range(num):
        infile.readline()

def splitread(infile,line):
    line = infile.readline() 
    splitline = line.split()
    return splitline
    
def readfrd(resultsfile,selecttime=None):
    i = 0
    temps = []
    disps = []
    stresses = []
    strains = []
    infile = initiate(resultsfile)
    
    while True:
        i += 1
        line = infile.readline()
        
        if '1PSTEP' in line:
            line = infile.readline() 
            splitline = line.split()
            
            time = splitline[2]
            time = float(time)
            
            line = infile.readline() 
            splitline = line.split()
            mode = splitline[1]
            
            if time == selecttime or selecttime == None:
            
                if mode == 'DISP':
                    skipline(infile,4)
                    while True:
                        line = infile.readline()
                        splitline = readchar(line)
                        if splitline[0] == '-3':
                            break
                        U = [time,float(splitline[1]),float(splitline[2]),float(splitline[3]),float(splitline[4])]
                        disps.append(U)
                        
                if mode == 'NDTEMP':
                    skipline(infile,1)
                    while True:
                        line = infile.readline()
                        splitline = readchar(line)
                        if splitline[0] == '-3':
                            break
                        T = [time,float(splitline[1]),float(splitline[2])]
                        temps.append(T)
                        
                if mode == 'STRESS':
                    skipline(infile,6)
                    while True:
                        line = infile.readline()
                        splitline = readchar(line)
                        if splitline[0] == '-3':
                            break
                        S = [time,float(splitline[1]),float(splitline[2]),
                        float(splitline[3]),float(splitline[4]),float(splitline[5]),
                        float(splitline[6]),float(splitline[7])]
                        stresses.append(S)
                        
                if mode == 'TOSTRAIN':
                    skipline(infile,6)
                    while True:
                        line = infile.readline()
                        splitline = readchar(line)
                        if splitline[0] == '-3':
                            break
                        E = [time,float(splitline[1]),float(splitline[2]),
                        float(splitline[3]),float(splitline[4]),float(splitline[5]),
                        float(splitline[6]),float(splitline[7])]
                        strains.append(E)
                               
        splitline = line.split()
        
        if splitline[0] == '9999':
            break
        
    return time, disps, temps, stresses, strains


#time,disps,temps,stresses,strains = readfrd(infile,selecttime)