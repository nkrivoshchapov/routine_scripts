import sys,os,glob,subprocess
import ntpath
import numpy as np
from numpy.linalg import norm

def gettorsion(points):
    # 4 points are given
    fr1_side = points[0] - points[1]
    fr1_mid = points[2] - points[1]
    fr2_mid = -fr1_mid
    fr2_side = points[3] - points[2]

    for i in [fr1_side, fr1_mid, fr2_side, fr2_mid]:
        i /= norm(i)
    fr1_norm = np.cross(fr1_side, fr1_mid)
    fr2_norm = np.cross(fr2_mid, fr2_side)
    for i in [fr1_norm, fr2_norm]:
        i /= norm(i)
    ang = np.arccos(np.dot(fr1_norm, fr2_norm))
    if np.dot(np.cross(fr1_side, fr1_mid), fr2_side) < 0:
        ang = -ang
    return ang

atomnumbers = [2,1,8,13] # NORMAL NUMERATION (FROM 1)
at0 = atomnumbers[0]+1
at1 = atomnumbers[1]+1
at2 = atomnumbers[2]+1
at3 = atomnumbers[3]+1
piorb = ["LP (   2) O   7", "BD*(   2) C   1 - O   2"]
sigmaorb = ["LP (   1) O   7", "BD*(   1) C   1 - O   2"]
backorb = ["LP (   2) O   2", "BD*(   1) C   1 - O   7"]
outfile = open("summary.csv","w")
outfile.write("File,E_Energy,Torsion,Pdonation,SPdonation,COdonation\n")
for filename in glob.glob("./nosolv*xyz"):
    xyz_lines = open(filename,"r").readlines()
    Eenergy = float(xyz_lines[1].split(";")[0])
    
    points = []
    for i in [at0,at1,at2,at3]:
        parts = list(filter(None, xyz_lines[i].replace("\r","").replace("\n","").split(" ")))
        points.append(np.array([float(parts[1]),float(parts[2]),float(parts[3])]))
    torsion = float(gettorsion(points))*180/3.141593
    
    log_lines = open(filename.replace("xyz","log"), "r").readlines()
    for line in log_lines:
        if piorb[0] in line and piorb[1] in line:
            pienergy = float(list(filter(None, line.split(piorb[1])[1].replace("\r","").replace("\n","").split(" ")))[0])
        if sigmaorb[0] in line and sigmaorb[1] in line:
            sigmaenergy = float(list(filter(None, line.split(sigmaorb[1])[1].replace("\r","").replace("\n","").split(" ")))[0])
        if backorb[0] in line and backorb[1] in line:
            backenergy = float(list(filter(None, line.split(backorb[1])[1].replace("\r","").replace("\n","").split(" ")))[0])
    outfile.write("%s,%f,%f,%f,%f,%f\n" % (ntpath.basename(filename), Eenergy, torsion, pienergy, sigmaenergy,backenergy))
outfile.close()