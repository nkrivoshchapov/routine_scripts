import sys,os,glob,subprocess

def getE(line):
    parts = line.split(" ")
    vals=[]
    for part in parts:
        if len(part) > 0:
            vals.append(part)
    return vals[len(vals)-1]
csvlines= []
for file in glob.glob("./*.log"):
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
    csvlines.append(file.split("\\")[1]+","+ener)
cfile=open("res.csv","w")
cfile.write("\n".join(csvlines))
cfile.close()