import glob,os,sys
from shutil import copy2

try:
    os.mkdir("good")
    os.mkdir("bad")
except:
    pass

for file in glob.glob("./*.log"):
    try:
        lines = open(file,"r").readlines()
    except:
        print(file)
        continue
    good=False
    for i in range(len(lines)-10,len(lines)):
        if "Normal termination" in lines[i]:
            good=True
    if good:
        copy2(file,"good")
        os.remove(file.replace("log","gjf"))
    else:
        copy2(file,"bad")
