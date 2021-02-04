#!/usr/bin/python
import glob,os,sys

out = open("prodE.csv","w")
out.write("Product,State,Energy,Freq\n")
for file in glob.glob("./*.log"):
    molname = file.split("\\")[1]
    strname = file.split("\\")[1]
    try:
        lines = open(file,"r").readlines()
    except:
        print(file)
        continue
    e=0
    freq=0
    good=False
    for line in reversed(lines):
        if "Normal termination" in line:
            good=True
        if "SCF Done" in line:
            e = float(line.split("=")[1].split("A.U.")[0])
            break
        if "Sum of electronic and thermal Free Energies" in line:
            freq = float(line.split("=")[1].split("\n")[0])
    if good:
        out.write(molname+","+strname+","+str(e)+","+str(freq)+"\n")
out.close()