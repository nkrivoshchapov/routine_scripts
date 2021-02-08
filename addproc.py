import sys,os,glob
import ntpath

for file in glob.glob("./*gjf"):
    lines = open(file,"r").readlines()
    idx = -1
    for i in range(len(lines)):
        if "%%nprocshared" in lines[i]:
            idx = i
    if idx > -1:
        lines[idx] = "%%nprocshared=%d\n" % int(sys.argv[1])
    else:
        lines.insert(0,"%%nprocshared=%d\n" % int(sys.argv[1])) 
    myfile = open(file,"w")
    myfile.write("".join(lines))
    myfile.close()