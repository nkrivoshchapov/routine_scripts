import sys,os,glob,subprocess
import ntpath
import numpy as np
from numpy.linalg import norm

def getvalangle(points):
    prevvec = points[0]
    curvec = points[1]
    nextvec = points[2]
    dir1 = prevvec - curvec
    dir2 = nextvec - curvec
    dir1 /= norm(dir1)
    dir2 /= norm(dir2)
    angle = np.arccos(np.dot(dir1, dir2))
    return angle

atomnumbers = [1, 2, 3] # NORMAL NUMERATION (FROM 1)
at0 = atomnumbers[0]+1
at1 = atomnumbers[1]+1
at2 = atomnumbers[2]+1
myNBO = "LP ( 1) N   2"
outfile = open("summary.csv","w")
outfile.write("File;E_Energy;VAngle;NBO s-character;NLMO s-character\n")
for filename in glob.glob("./*xyz"):
    xyz_lines = open(filename,"r").readlines()
    Eenergy = float(xyz_lines[1].split(";")[0])
    
    points = []
    for i in [at0,at1,at2]:
        parts = list(filter(None, xyz_lines[i].replace("\r","").replace("\n","").split(" ")))
        points.append(np.array([float(parts[1]),float(parts[2]),float(parts[3])]))
    myvangle = float(getvalangle(points))*180/3.141593
    
    log_lines = open(filename.replace("xyz","log"), "r").readlines()
    
    nbolist_start = 0
    nbolist_end = 0
    nlmolist_start = 0
    
    for i, line in enumerate(log_lines):
        if "NATURAL LOCALIZED MOLECULAR ORBITAL (NLMO) ANALYSIS:" in line:
            nlmolist_start = i
            break
        elif "(Occupancy)   Bond orbital/ Coefficients/ Hybrids" in line:
            nbolist_start = i
        elif "NHO Directionality and \"Bond Bending\" (deviations from line of nuclear centers)" in line:
            nbolist_end = i
        
    for i in range(nbolist_start, nbolist_end):
        if myNBO in log_lines[i]:
            nbo_schar = float(log_lines[i].split("s(")[1].split("%)p")[0])
    
    for i in range(nlmolist_start, len(log_lines)):
        if myNBO in log_lines[i]:
            nlmo_schar = float(log_lines[i + 3].split("s(")[1].split("%)p")[0])
    
    outfile.write("%s;%f;%f;%f;%f\n" % (ntpath.basename(filename), Eenergy, myvangle, nbo_schar, nlmo_schar))
outfile.close()