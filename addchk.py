import sys,os,glob
import ntpath

for file in glob.glob("./*gjf"):
    lines = open(file,"r").readlines()
    need=False
    for line in lines:
        if "calcfc" in line or "freq" in line:
            need = True
            break
    if need:
        lines.insert(0, "%chk="+ntpath.basename(file).split(".")[0]+".chk\n")
        wfile = open(file,"w")
        wfile.write("".join(lines))
        wfile.close()
    