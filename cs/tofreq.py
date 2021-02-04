import os,sys,glob,math,subprocess
from copy import deepcopy
def sortKey(elem):
    return elem[1]
xyzlist = []
for xyzf in glob.glob("./"+sys.argv[1]+"*.xyz"):
    xyzlines = open(xyzf,"r").readlines()
    xyzlist.append([xyzf,float(xyzlines[1].split(";")[0])])
xyzlist.sort(key=sortKey)
dftlist = [xyzlist[0][0]]

for i in range(1,len(xyzlist)):
    if abs(xyzlist[i][1] - xyzlist[i-1][1]) < 0.00001:
        continue
    if len(dftlist)<int(sys.argv[2]):
        dftlist.append(xyzlist[i][0])
    else:
        break
nconf = 0
for i in dftlist:
    xyzlines = open(i,"r").readlines()
    xyzlines.remove(xyzlines[1])
    xyzlines.remove(xyzlines[0])
    outlines = ["# opt=(tight,maxcycle=300) freq 6-311++g(d,p) scrf=(smd,solvent=methanol) empiricaldispersion=gd3bj rpbe1pbe","","Conformation","","0 1"]
    outfile = open("%s_dft_%d.gjf"%(sys.argv[1],nconf),"w")
    outfile.write("\n".join(outlines)+"".join(xyzlines)+"\n\n")
    outfile.close()
    nconf += 1