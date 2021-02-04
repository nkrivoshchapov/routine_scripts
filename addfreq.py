import sys,os,glob
import ntpath

for file in glob.glob("./*gjf"):
    lines = open(file,"r").readlines()
    for i in range(len(lines)):
        if "opt=(calcfc,ts,noeigentest,maxcycle=300)" in lines[i]:
            lines[i] = lines[i].replace("opt=(calcfc,ts,noeigentest,maxcycle=300)","opt=(calcfc,ts,noeigentest,maxcycle=300) freq")
            break
    wfile = open(file,"w")
    wfile.write("".join(lines))
    wfile.close()
    