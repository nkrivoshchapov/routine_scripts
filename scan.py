import numpy as np
import os, sys

name = "peroxBw"
rotl = [25,26,27,28] # atoms to rotate
for i in rotl:
    rotl[rotl.index(i)] -= 1
axl = [25,5] # axis
for i in axl:
    axl[axl.index(i)] -= 1
atlines = [] # all lines of the file
coords = [] # coordinates of atoms
indicies = [] 
lines = open(name+".gjf","r").readlines()
for line in lines:
    atlines.append(line)
    if line.startswith(" H") or line.startswith(" C") or line.startswith(" O") or line.startswith(" N"):
        indicies.append(atlines.index(line))
        line = line.replace(" N", "")
        line = line.replace(" O", "")
        line = line.replace(" C", "")
        line = line.replace(" H", "")
        shit = line.split(" ")
        coo = []
        for i in shit:
            if len(i) > 3:
                coo.append(float(i))
        coords.append(coo)
coords_back= coords
atlines_back = atlines

at1 = np.array(coords[axl[0]])
at2 = np.array(coords[axl[1]])
print(at2)
at3 = np.array(coords[1])
trans_vec = np.array(3)
trans_vec = at1 - at2
trans_vec = trans_vec/np.linalg.norm(trans_vec)
ex = np.array(3)
ey = np.array(3)
ez = np.array(3)
ex = trans_vec
ey = np.cross(ex,at3-at2)
ey = ey/np.linalg.norm(ey)
ez = np.cross(ex,ey)
da = 0
dr = 0
astep = 0
rstep = 0
while dr <= 0.6:
    rstep += 1
    for i in rotl:
        atom = np.array(coords[i]) 
        atom2 = np.array([np.dot(atom- at2,ex),np.dot(atom- at2,ey),np.dot(atom- at2,ez)])
        rotmat = np.array([[1,0,0],[0,np.cos(da),-np.sin(da)],[0,np.sin(da),np.cos(da)]])
        atom = np.matmul(rotmat,atom2)
        atom2[:] = atom[0]*ex[:] + atom[1]*ey[:] + atom[2]*ez[:] + at2[:] + trans_vec[:]*dr
        sign = " " + atlines[indicies[i]][1]
        atlines[indicies[i]] = '%2s%28.8f%14.8f%14.8f\n' % (sign, (atom2[0]),(atom2[1]),(atom2[2]))
    
    fil = open(name+"_"+str(rstep)+".gjf","w")
    fil.write("".join(atlines))
    
    coords = coords_back
    atlines = atlines_back
    dr += 0.04

    