import sys,os,glob

for file in glob.glob("./*gjf"):
    lines = open(file,"r").readlines()
    for i in range(len(lines)):
        if "0 1" in lines[i]:
            lines[i] = lines[i].replace("0 1", "0 1\n")
    newfile = open(file,"w")
    newfile.write("".join(lines))
    newfile.close()
