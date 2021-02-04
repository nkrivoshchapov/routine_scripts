import sys,os
import glob
xyzpath = sys.argv[1]
destpath = sys.argv[2]
NCONF = 400
types = []
for file in os.listdir(xyzpath):
    if file.split("_")[1] not in types:
        types.append(file.split("_")[1])
for type in types:
    count = 0
    print("Doing "+type)
    for xyzfile in os.listdir(xyzpath):
        if type in xyzfile:
            count += 1
            if count >= NCONF:
                #os.remove("./temp_xyz/"+xyzfile)
                break
            gjffile = open(destpath+"/"+xyzfile.split("_")[1]+"_"+str(count)+".gjf","w")
            lines = open(xyzpath+"/"+xyzfile,"r").readlines()
            #gjffile.write("# opt=maxcycle=300 6-311++g(d,p) scrf=(smd,solvent=methanol) empiricaldispersion=gd3bj rpbe1pbe\n\nConformation\n\n0 1\n")
            gjffile.write("# opt=(maxcycle=300,tight) scrf=(cpcm,solvent=methanol) rpm6\n\nConformation\n\n0 1\n")
            for i in range(1,len(lines)):
                gjffile.write(lines[i])
            gjffile.write("\n\n")
            #os.remove("./temp_xyz/"+xyzfile)
