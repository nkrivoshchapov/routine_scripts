import sys,os,glob
import ntpath

for file in glob.glob("./*gjf"):
    lines = open(file,"r").readlines()
    lines[0] = "%nprocshared=8\n"
    wfile = open(file,"w")
    wfile.write("".join(lines))
    wfile.close()
    