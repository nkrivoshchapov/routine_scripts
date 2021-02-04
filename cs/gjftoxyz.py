import sys,os,glob

for filename in glob.glob("./*gjf"):
    lines = open(filename, "r").readlines()
    start = False
    xyzlines = []
    for i in range(len(lines)):
        if start and len(lines[i]) > 10:
            xyzlines.append(lines[i])
        if "0 1" in lines[i]:
            start = True
    xyzlines.insert(0,"\n")
    xyzlines.insert(0,str(len(xyzlines)-1)+"\n")
    
    xyzfile = open(filename.replace("gjf","xyz"),"w")
    xyzfile.write("".join(xyzlines))
    xyzfile.close()
    

        
     
