import os, sys, subprocess, time, glob
import signal
from shutil import copy2
nproc = int(sys.argv[1])
docalc = []
procs = []
for calcdir in glob.glob("./*"):
    if os.path.isdir(calcdir):
        docalc.append(calcdir)

while len(docalc) > 0 or len(procs) > 0:
    for i in reversed(range(len(procs))):
        if not procs[i].poll() == None:
            del procs[i]
    while len(procs) < nproc and len(docalc) > 0:
        calcdir = docalc.pop()
        print("Doing CREST job for file " + calcdir.split("/")[0])
        procs.append(subprocess.Popen("../../runxtbcs.sh " + calcdir.split("/")[1], shell = True))
    time.sleep(1)
