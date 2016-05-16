# -*- coding: utf-8 -*-
"""
Created on Thu May 12 13:29:52 2016

@author: spookfish
"""
import numpy as np

def Aux_results(time,disps,temps,stresses,strains):
    Dall = []
    Von_Mises = []
    Principal = []
    for i in range(len(disps)):
        d = [disps[i][0],disps[i][1],np.sqrt(disps[i][2]**2 + disps[i][3]**2 + disps[i][4]**2)]
        Dall.append(d)
        
        [s11, s22, s33, s12, s13, s23] = stresses[i][2],stresses[i][3],stresses[i][4],stresses[i][5],stresses[i][6],stresses[i][7]
        
        aval = s11 - s22
        bval = s22 - s33
        cval = s33 - s11
        dval = s12**2 + s23**2 +s13**2
        s = (0.5*(aval**2 + bval**2 + cval**2 +6*dval))**0.5
        s = [stresses[i][0],stresses[i][1],s]
        Von_Mises.append(s)
        
        aval = 1
        bval = (s11 + s22 + s33)*-1.0
        cval = (s11*s22 + s11*s33 + s22*s33 - s12**2 - s13**2 - s23**2)
        dval = (s11*s22*s33 + 2*s12*s13*s23 - s11*(s23**2) - s22*(s13**2)
                - s33*(s12**2))*-1.0
        p = list(np.roots([aval, bval, cval, dval]))
        p = sorted(p, reverse=True)
        p = [stresses[i][0],stresses[i][1],p[0],p[1],p[2]]
        Principal.append(p)

    
    return Dall,Von_Mises,Principal