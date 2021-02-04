import sys,os,glob

for file in glob.glob("./nosolv*xyz"):
    lines = open(file,"r").readlines()
    del lines[0]
    del lines[0]
    lines.insert(0,"0 1\n")
    lines.insert(0,"\n")
    lines.insert(0,"Untitled\n")
    lines.insert(0,"\n")
    lines.insert(0,"# aug-cc-pvtz scrf=(cpcm,solvent=water) empiricaldispersion=gd3bj rpbe1pbe pop=nboread\n")    
    lines.append("\n$NBO $END\n\n")
    wfile = open(file.replace("xyz","gjf"),"w")
    wfile.write("".join(lines))
    wfile.close()
    
    