# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 10:18:31 2016

@author: stephen

Version: 0.1

This script create a .inp file for calculix for a straight section of pipe. The
created mesh is a hex mesh swept along the pipe. The user has control of the 
through-thickness, radial and length-wise element divisions. Furthermore, the user
has three options as to how the through-thickness divisions are created so that more
elements can be positioned on the inside of the the pipe.
The script can create linear 8 node elements or 20 node quadratic elements with 
reduced or full intergration.
The script also creates the nodal groups for each surface on the pipe and creates 
element and surface groups for the inside and outside of the pipe.
"""

import numpy as np

# Toggle to turn inputs on and off
inputs = 0

#Asks for the input variables else sets defaults
if inputs == 1:
    
    ID = input("Enter the Inner Diameter of the pipe: ")
    t = input("Enter the thickness: ")
    l = input("Enter the length of the pipe: ")
    thickness = input("Enter the through-thickness divisions: ")
    radial = input("Enter the radial divisions: ")
    length = input("Enter the length divisions: ")
    section = input("Would you like golden section (type 1) or geometric (type 2) divisions: ")
    if section == 2:
        r = input("Would you like the common ratio to be: ")
        r = float(r)
    quad = input("Would you like linear(0) or quadratic(1) elements: ")
    reduced = input("Would you like reduced integration (type 1)")
    
else:
    
    ID = 250.0
    t = 29.0
    l = 1000.0

    length = 6
    thickness = 6
    radial = 10
    
    section = 2
    r = 1.2
    
    quad = 1
    reduced = 0

#Secodanry inputs are defined
OD = ID + 2*t
n = 2*radial
theta = (2*np.pi)/n
sec = np.zeros((thickness,1))
c = t

#The through thickness divisions are set based on the pipe thickness
# and sectioning methodology

#Golden section
if section == 1:
    golden = (1 + 5 ** 0.5) / 2 
    for i in range(thickness-1):
        sec[i] = c/golden
        sec[i+1] = c - sec[i]
        c = sec[i+1].copy()
    sec = sec[::-1]
#Geometric sequence
elif section == 2:
     a = t/((1-r**thickness)/(1-r))
     sec[0] = a
     for i in range(thickness-1):
         sec[i+1] = a*r**(i+1)
#Regular sections
else:
    for i in range(thickness-1):
        sec[i] = t/thickness
        sec[i+1] = t/thickness
        
#Fixes the section if there is one element through the thickness
if thickness == 1:
    sec[:] = t
    
#Node Positionsing
'''This section creates the node position in 3D space. 
The indexing is based on a cylindrical co-ordinate system [length,thickness,radial].
The even indicies: 0,2,4.. are for the corner nodes. 
The odd indicies: 1,3,4.. are for the midside nodes
NOTE! Not all the midside nodes have values e.g in the middle of an element there is 
an empty poition.
The zero position node is at [0,0,ID of pipe].'''
mid_nodes = np.zeros((length*2+1,thickness*2+1,n*2,3))

for i in range(thickness+1):
    mid_nodes[0,2*i,0] = [0,0,ID/2 + sum(sec[0:i])] 
    for j in range(n-1):
        mid_nodes[0,2*i,2*j+2] = [0,mid_nodes[0,2*i,0,1]*np.cos(theta*(j+1))-mid_nodes[0,2*i,0,2]*np.sin(theta*(j+1)),
        mid_nodes[0,2*i,0,1]*np.sin(theta*(j+1))+mid_nodes[0,2*i,0,2]*np.cos(theta*(j+1))]

for i in range(thickness+1):
    mid_nodes[0,i*2,1] = [0,-(ID/2 + sum(sec[0:i]))*np.sin((theta/2)),(ID/2 + sum(sec[0:i]))*np.cos((theta/2))]
    
    for j in range(n-1):
        mid_nodes[0,i*2,(j*2+3)] = [0,mid_nodes[0,i*2,1,1]*np.cos(theta*(j+1))-mid_nodes[0,i*2,1,2]*np.sin(theta*(j+1)),
        mid_nodes[0,i*2,1,1]*np.sin(theta*(j+1))+mid_nodes[0,i*2,1,2]*np.cos(theta*(j+1))]

for i in range(thickness):
    mid_nodes[0,2*i+1,0] = [0,0,ID/2 + sum(sec[0:i]) + 0.5*sec[i]] 
    for j in range(n-1):
        mid_nodes[0,2*i+1,j*2+2] = [0,mid_nodes[0,2*i+1,0,1]*np.cos(theta*(j+1))-mid_nodes[0,2*i+1,0,2]*np.sin(theta*(j+1)),
        mid_nodes[0,2*i+1,0,1]*np.sin(theta*(j+1))+mid_nodes[0,2*i+1,0,2]*np.cos(theta*(j+1))]

for i in range(length):
    mid_nodes[2*i+2,:,:,:] = mid_nodes[2*i,:,:,:]
    mid_nodes[2*i+2,:,:,0] = mid_nodes[2*i,:,:,0] + l/length
    
for i in range(thickness+1):
    mid_nodes[1,2*i,0] = [l/(length*2),0,ID/2 + sum(sec[0:i])] 
    for j in range(n-1):
        mid_nodes[1,2*i,2*j+2] = [l/(length*2),mid_nodes[1,2*i,0,1]*np.cos(theta*(j+1))-mid_nodes[1,2*i,0,2]*np.sin(theta*(j+1)),
        mid_nodes[1,2*i,0,1]*np.sin(theta*(j+1))+mid_nodes[1,2*i,0,2]*np.cos(theta*(j+1))]

for i in range(length-1):
    mid_nodes[2*i+3,:,:,:] = mid_nodes[2*i+1,:,:,:]
    mid_nodes[2*i+3,:,:,0] = mid_nodes[2*i+1,:,:,0] + l/length


#Node numbering
'''Now that there are points assembed in 3D space, each point must be labelled 
with a node number. The nodes are numberd first by radial position then by length 
and then by thickness so that layers of pipe nodes are built up. The position matrix
is in the same cylindrical co-ordinate system as the nodes. 
The nodes numbers are pinted out in the .inp file with their respective positions
in 3D space [x,y,z].'''
node_num = 0
node_pos = np.zeros((length*2+1,thickness*2+1,n*2))
ele_num = 0
#Create/Overwrite File
if quad == 1:
    elestr = "C3D20"
else:
    elestr = "C3D8"
if reduced == 1:
    interstr = "R"
else:
    interstr = "F"

#mesh = open("Mesh_" + str(length) + "x" + str(thickness) + "x" + str(n) + "_"
#+ elestr +interstr +".inp","w")
mesh = open("Mesh.inp","w")
mesh.write("*node, nset=Nall\n")

for i in range(thickness+1):
    for j in range(length+1):
        for k in range(n):
            node_num +=1
            mesh.write(str(node_num) +", " + str(mid_nodes[2*j,2*i,2*k,0])+", " 
            + str(mid_nodes[2*j,2*i,2*k,1]) +", " 
            + str(mid_nodes[2*j,2*i,2*k,2]) + "\n")
            node_pos[2*j,2*i,2*k] = node_num
            
if quad == 1:

    for i in range(thickness+1):
        for j in range(length+1):
            for k in range(n):
                node_num +=1
                mesh.write(str(node_num) +", " + str(mid_nodes[2*j,2*i,2*k+1,0])+", " 
                + str(mid_nodes[2*j,2*i,2*k+1,1]) +", " 
                + str(mid_nodes[2*j,2*i,2*k+1,2]) + "\n")
                node_pos[2*j,2*i,2*k+1] = node_num
    
    for i in range(thickness+1):
        for j in range(length):
            for k in range(n):
                node_num +=1
                mesh.write(str(node_num) +", " + str(mid_nodes[2*j+1,2*i,2*k,0])+", " 
                + str(mid_nodes[2*j+1,2*i,2*k,1]) +", " 
                + str(mid_nodes[2*j+1,2*i,2*k,2]) + "\n")
                node_pos[2*j+1,2*i,2*k] = node_num
    
    for i in range(thickness):
        for j in range(length+1):
            for k in range(n):
                node_num +=1
                mesh.write(str(node_num) +", " + str(mid_nodes[2*j,2*i+1,2*k,0])+", " 
                + str(mid_nodes[2*j,2*i+1,2*k,1]) +", " 
                + str(mid_nodes[2*j,2*i+1,2*k,2]) + "\n")
                node_pos[2*j,2*i+1,2*k] = node_num

#mesh.close()
node_pos = node_pos.astype(int)
#Node Groups
'''The nodal groups are created and printed in the .inp file for the nodes on
on the inside, outside, inlet section and outlet section of the pipe. 
Due to the cylindrical reference system, this is easily achieved.'''
count = 0
mesh.write("*nset, nset=Inlet\n")
for i in range(thickness+1):
    for k in range(n):
        if count == 8:
            count =0
            mesh.write("\n")  
    
        count +=1
        
        mesh.write(str(node_pos[0,2*i,2*k]) +", ")
        
    if i == thickness:
        mesh.write("\n")  
        
if quad == 1:
            
    count = 0     
    for i in range(thickness+1):
        for k in range(n):
            if count == 8:
                count =0
                mesh.write("\n")  
        
            count +=1
            
            mesh.write(str(node_pos[0,2*i,2*k+1]) +", ")
        
        if i == thickness:
            mesh.write("\n")         
            
    count = 0    
    for i in range(thickness):
        for k in range(n):
            
            if count == 8:
                count =0
                mesh.write("\n")
                
            count +=1
            
            mesh.write(str(node_pos[0,2*i+1,2*k]) +", ")
            
        if i == thickness-1:
            mesh.write("\n") 
        
count = 0    
#Labelling is shuffled for better plane MPC   
x = range(n)
np.random.shuffle(x)     
mesh.write("*nset, nset=Outlet\n")
for i in range(thickness+1):
    for k in x:
        if count == 8:
            count =0
            mesh.write("\n")  
    
        count +=1
        
        mesh.write(str(node_pos[-1,2*i,2*k]) +", ")
        
    if i == thickness:
        mesh.write("\n")  
        
if quad == 1:
            
    count = 0     
    for i in range(thickness+1):
        for k in range(n):
            if count == 8:
                count =0
                mesh.write("\n")  
        
            count +=1
            
            mesh.write(str(node_pos[-1,2*i,2*k+1]) +", ")
        
        if i == thickness:
            mesh.write("\n")         
            
    count = 0    
    for i in range(thickness):
        for k in range(n):
            
            if count == 8:
                count =0
                mesh.write("\n")
                
            count +=1
            
            mesh.write(str(node_pos[-1,2*i+1,2*k]) +", ")
            
        if i == thickness-1:
            mesh.write("\n") 

count = 0
mesh.write("*nset, nset=Inside\n")
for i in range(length+1):
    for k in range(n):
        if count == 8:
            count =0
            mesh.write("\n")  
    
        count +=1
        
        mesh.write(str(node_pos[2*i,0,2*k]) +", ")
        
    if i == length:
        mesh.write("\n")  
        
if quad == 1:
            
    count = 0     
    for i in range(length+1):
        for k in range(n):
            if count == 8:
                count =0
                mesh.write("\n")  
        
            count +=1
            
            mesh.write(str(node_pos[2*i,0,2*k+1]) +", ")
        
        if i == length:
            mesh.write("\n")         
            
    count = 0    
    for i in range(length):
        for k in range(n):
            
            if count == 8:
                count =0
                mesh.write("\n")
                
            count +=1
            
            mesh.write(str(node_pos[2*i+1,0,2*k]) +", ")
            
        if i == length-1:
            mesh.write("\n") 

count = 0
mesh.write("*nset, nset=Outside\n")

for i in range(length+1):
    for k in range(n):
        if count == 8:
            count =0
            mesh.write("\n")  
    
        count +=1
        
        mesh.write(str(node_pos[2*i,-1,2*k]) +", ")
        
    if i == length:
        mesh.write("\n")  
        
if quad == 1:
            
    count = 0     
    for i in range(length+1):
        for k in range(n):
            if count == 8:
                count =0
                mesh.write("\n")  
        
            count +=1
            
            mesh.write(str(node_pos[2*i,-1,2*k+1]) +", ")
        
        if i == length:
            mesh.write("\n")         
            
    count = 0    
    for i in range(length):
        for k in range(n):
            
            if count == 8:
                count =0
                mesh.write("\n")
                
            count +=1
            
            mesh.write(str(node_pos[2*i+1,-1,2*k]) +", ")
            
        if i == length-1:
            mesh.write("\n") 

#Elements
'''The elements are now assembled and printed in the .inp file. As with the nodes, 
the elemets are created radially, then along the length and then thickness to
build up layers. The elements are changed to reduced integration elements if 
requested'''
ele_num = node_num
ele_pos = np.zeros((length,thickness,n))
#mesh2 = open("Mesh2.inp","w")
if quad == 1:
    if reduced == 1:
        mesh.write("*element, elset=Eall,type=C3D20R\n")
    else:
        mesh.write("*element, elset=Eall,type=C3D20\n")
else:
    if reduced == 1:
        mesh.write("*element, elset=Eall,type=C3D8R\n")
    else:
        mesh.write("*element, elset=Eall,type=C3D8\n")

for i in range(thickness):
    for j in range(length):
        for k in range(n):
            ele_num += 1
            if quad == 1:
                if k == n-1:
                    mesh.write(str(ele_num) +", " 
                    + str(node_pos[2*j,2*i,2*k])+", "
                    + str(node_pos[2*j,2*i,2*(k-(n-1))])+", "
                    + str(node_pos[2*j+2,2*i,2*(k-(n-1))])+", "
                    + str(node_pos[2*j+2,2*i,2*k])+", "
                    #
                    + str(node_pos[2*j,2*i+2,2*k])+", "
                    + str(node_pos[2*j,2*i+2,2*(k-(n-1))])+", "
                    + str(node_pos[2*j+2,2*i+2,2*(k-(n-1))])+", "
                    + str(node_pos[2*j+2,2*i+2,2*k])
                    #
                    +", "
                    + str(node_pos[2*j,2*i,2*k+1])+", "
                    + str(node_pos[2*j+1,2*i,2*(k-(n-1))])+", "
                    + str(node_pos[2*j+2,2*i,2*k+1])+", "
                    + str(node_pos[2*j+1,2*i,2*k])+", "
                    #
                    + str(node_pos[2*j,2*i+2,2*k+1])+", "
                    + str(node_pos[2*j+1,2*i+2,2*(k-(n-1))])+",\n"
                    + str(node_pos[2*j+2,2*i+2,2*k+1])+", "
                    + str(node_pos[2*j+1,2*i+2,2*k])+", "
                    #
                    + str(node_pos[2*j,2*i+1,2*k])+", "
                    + str(node_pos[2*j,2*i+1,2*(k-(n-1))])+", "
                    + str(node_pos[2*j+2,2*i+1,2*(k-(n-1))])+", "
                    + str(node_pos[2*j+2,2*i+1,2*k])+"\n")
                    
                    ele_pos[j,i,k] = ele_num
                    
                else:
                    mesh.write(str(ele_num) +", " 
                    + str(node_pos[2*j,2*i,2*k])+", "
                    + str(node_pos[2*j,2*i,2*k+2])+", "
                    + str(node_pos[2*j+2,2*i,2*k+2])+", "
                    + str(node_pos[2*j+2,2*i,2*k])+", "
                    #
                    + str(node_pos[2*j,2*i+2,2*k])+", "
                    + str(node_pos[2*j,2*i+2,2*k+2])+", "
                    + str(node_pos[2*j+2,2*i+2,2*k+2])+", "
                    + str(node_pos[2*j+2,2*i+2,2*k])
                    #
                    +", "
                    + str(node_pos[2*j,2*i,2*k+1])+", "
                    + str(node_pos[2*j+1,2*i,2*k+2])+", "
                    + str(node_pos[2*j+2,2*i,2*k+1])+", "
                    + str(node_pos[2*j+1,2*i,2*k])+", "
                    #
                    + str(node_pos[2*j,2*i+2,2*k+1])+", "
                    + str(node_pos[2*j+1,2*i+2,2*k+2])+",\n"
                    + str(node_pos[2*j+2,2*i+2,2*k+1])+", "
                    + str(node_pos[2*j+1,2*i+2,2*k])+", "
                    #
                    + str(node_pos[2*j,2*i+1,2*k])+", "
                    + str(node_pos[2*j,2*i+1,2*k+2])+", "
                    + str(node_pos[2*j+2,2*i+1,2*k+2])+", "
                    + str(node_pos[2*j+2,2*i+1,2*k])+"\n")
                    
                    ele_pos[j,i,k] = ele_num
            else:
                if k == n-1:
                    mesh.write(str(ele_num) +", " 
                    + str(node_pos[2*j,2*i,2*k])+", "
                    + str(node_pos[2*j,2*i,2*(k-(n-1))])+", "
                    + str(node_pos[2*j+2,2*i,2*(k-(n-1))])+", "
                    + str(node_pos[2*j+2,2*i,2*k])+", "
                    #
                    + str(node_pos[2*j,2*i+2,2*k])+", "
                    + str(node_pos[2*j,2*i+2,2*(k-(n-1))])+", "
                    + str(node_pos[2*j+2,2*i+2,2*(k-(n-1))])+", "
                    + str(node_pos[2*j+2,2*i+2,2*k])+"\n")  
                    
                    ele_pos[j,i,k] = ele_num
                else:
                    mesh.write(str(ele_num) +", " 
                    + str(node_pos[2*j,2*i,2*k])+", "
                    + str(node_pos[2*j,2*i,2*k+2])+", "
                    + str(node_pos[2*j+2,2*i,2*k+2])+", "
                    + str(node_pos[2*j+2,2*i,2*k])+", "
                    #
                    + str(node_pos[2*j,2*i+2,2*k])+", "
                    + str(node_pos[2*j,2*i+2,2*k+2])+", "
                    + str(node_pos[2*j+2,2*i+2,2*k+2])+", "
                    + str(node_pos[2*j+2,2*i+2,2*k])+"\n")
                    
                    ele_pos[j,i,k] = ele_num
 
#Element Groups
'''The element groups are now created. Only the elements on the inside and outside
of the pipe are grouped.'''
ele_pos = ele_pos.astype(int)
count = 0
mesh.write("*elset, elset=InsideF1\n")

for i in range(length):
    for k in range(n):
        if count == 8:
            count =0
            mesh.write("\n")  
    
        count +=1
        
        mesh.write(str(ele_pos[i,0,k]) +", ")
        
    if i == length-1:
        mesh.write("\n")
        
count = 0
mesh.write("*elset, elset=OutsideF2\n")

for i in range(length):
    for k in range(n):
        if count == 8:
            count =0
            mesh.write("\n")  
    
        count +=1
        
        mesh.write(str(ele_pos[i,-1,k]) +", ")
        
    if i == length-1:
        mesh.write("\n")

#Surface Groups
'''Because of the way the elements are printed, face 1 (S1) of each element is
always on the inside of the pipe layer and face 2 (S2) of each element is
always in the outside of the pipe layer.'''

mesh.write("*surface, type=element, name=sInside\n")
mesh.write("InsideF1, S1\n")
mesh.write("*surface, type=element, name=sOutside\n")
mesh.write("OutsideF2, S2\n")
#Close file
mesh.close() 
#End message
print "\nYour calculix.inp file has been created."