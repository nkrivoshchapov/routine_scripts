import sys,os,glob,subprocess
from shutil import copy2
from pathlib import Path

types = []
for file in glob.glob("./*.log"):
    if os.path.basename(file).split("_")[0] not in types:
        types.append(os.path.basename(file).split("_")[0])

def getE(line):
    parts = line.split(" ")
    vals=[]
    for part in parts:
        if len(part) > 0:
            vals.append(part)
    return vals[len(vals)-1]
csvlines= []
for type in types:
    myfile = ""
    min=0
    for file in glob.glob("./"+type+"*.log"):
        print(file)
        sseq = ['python','-m','goodvibes','-q','-t 273.15','-c 0.3188','--invertifreq=-15',file.replace("./","")]
        print(" ".join(sseq))
        out = subprocess.run(sseq, stdout=subprocess.PIPE)
        outlines = str(out.stdout).split("\\r\\n")
        ener = ""
        for i in range(0,len(outlines)):
            if "***" in outlines[i]:
                ener = getE(outlines[i+1])
                break
        if float(ener)<min:
            min = float(ener)
            myfile = file
        csvlines.append(file.split("\\")[1]+","+ener)
    print("myfile "+myfile)
    print("kek "+"./"+type+".log")
    copy2(myfile,"./"+type+".log")
    Path("./"+type+".log").touch()
cfile=open("res.csv","w")
cfile.write("\n".join(csvlines))
cfile.close()