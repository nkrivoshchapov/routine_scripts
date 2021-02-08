import os,sys,glob,math,subprocess
from copy import deepcopy
def sortKey(elem):
    return elem[1]

def rmsd(a,b):
    print(a + " AND " + b)
    out = subprocess.run(['calc_rmsd',a,b], stdout=subprocess.PIPE)
    print(str(float(out.stdout)))
    return float(out.stdout)

for mol in glob.glob("../c_files/*.c"):
    print(mol)
    bonds = []
    bond1 = []
    bond2 = []
    mollines = open(mol,"r").readlines()
    maxdist = []
    mindist = []
    bondlines=[]

    for i in range(len(mollines)):
        if "const static float mindist" in mollines[i]:
            parts = mollines[i].split("{{")[1].split("}}")[0].split("},{")
            for item in parts:
                mindist.append(deepcopy(item.split(",")))
        if "const static float maxdist" in mollines[i]:
            parts = mollines[i].split("{{")[1].split("}}")[0].split("},{")
            for item in parts:
                maxdist.append(deepcopy(item.split(",")))
        if "const static int bond1" in mollines[i]:
            bond1 = deepcopy(mollines[i].split("{")[1].split("}")[0].split(","))
        if "const static int bond2" in mollines[i]:
            bond2 = deepcopy(mollines[i].split("{")[1].split("}")[0].split(","))

    for i in range(1,len(bond1)):
        bonds.append([int(bond1[i]),int(bond2[i])])

    for i in range(len(maxdist)):
        for j in range(len(maxdist[i])):
            maxdist[i][j] = float(maxdist[i][j])

    for i in range(len(mindist)):
        for j in range(len(mindist[i])):
            mindist[i][j] = float(mindist[i][j])

    print(repr(bonds))
    xyzlist = []

    if len(glob.glob("./"+mol.split("/")[2].split(".")[0]+"*xyz"))==0:
        continue

    for xyzf in glob.glob("./"+mol.split("/")[2].split(".")[0]+"*xyz"):
        print(xyzf)
        xyzlines = open(xyzf,"r").readlines()
        xyz=[]
        for i in range(2,len(xyzlines)-1):
            parts = xyzlines[i].replace("\n","").split(" ")
            parts = list(filter(None, parts))
            xyz.append([float(parts[1]),float(parts[2]),float(parts[3])])
        good = True
        #print(repr(xyz))

        for i in range(0,len(xyz)):
            for j in range(0,i):
                dist = math.sqrt((xyz[i][0]-xyz[j][0])**2+(xyz[i][1]-xyz[j][1])**2+(xyz[i][2]-xyz[j][2])**2)
                if [i+1,j+1] in bonds or [j+1,i+1] in bonds:
                    if maxdist[i+1][j+1] > 0 and dist - maxdist[i+1][j+1] > 0.3:#not abs(dist-1.72887) < 0.001 and dist > 1.6:
                        print("Bond ban (%d,%d). Real = %f. Expected = %f"%(i+1,j+1,dist,maxdist[i+1][j+1] ))
                        good = False
                else:
                    if dist < 1.4:
                        good = False
                if dist < 0.8:
                    good = False
        if good:
            if xyzlines[1].split(";")[0] == "NA":
                print("NA!!!")
                continue
            else:
                xyzlist.append([xyzf,float(xyzlines[1].split(":")[1].split("gnorm")[0])])
    xyzlist.sort(key=sortKey)
    dftlist = [xyzlist[0][0]]
    for i in range(1,len(xyzlist)):
        if abs(xyzlist[i][1] - xyzlist[i-1][1]) < 0.00001:
            print("SAME: %s AND %s"%(xyzlist[i][0],xyzlist[i-1][0]))
            continue
        elif abs(xyzlist[i][1] - xyzlist[i-1][1]) < 0.001:
            if rmsd(xyzlist[i][0], xyzlist[i-1][0]) > 0.4:
                dftlist.append(xyzlist[i][0])
        else:
            dftlist.append(xyzlist[i][0])
    nconf = 0
    for i in dftlist:
        xyzlines = open(i,"r").readlines()
        xyzlines.remove(xyzlines[1])
        xyzlines.remove(xyzlines[0])
        outlines = ["# opt=maxcycle=300 6-311++g(d,p) scrf=(smd,solvent=methanol) empiricaldispersion=gd3bj rpbe1pbe","","Conformation","","0 1"]
        outfile = open("%s_dft_%d.gjf"%(mol.split("/")[2].split(".")[0],nconf),"w")
        outfile.write("\n".join(outlines)+"\n"+"".join(xyzlines)+"\n\n")
        outfile.close()
        nconf += 1
