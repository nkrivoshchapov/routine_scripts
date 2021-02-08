import os, sys, subprocess, time, glob
import signal
import ntpath

from shutil import copy2
nproc = int(sys.argv[1])
docalc = []
procs = []
for calcdir in glob.glob("./aminoprod1L*gjf"):
    docalc.append(calcdir)

while len(docalc) > 0 or len(procs) > 0:
    for i in reversed(range(len(procs))):
        if not procs[i].poll() == None:
            del procs[i]
    while len(procs) < nproc and len(docalc) > 0:
        calcdir = docalc.pop()
        print("Performing Monte-Carlo CS for " + ntpath.basename(calcdir))
        procs.append(subprocess.Popen("rung " + ntpath.basename(calcdir), shell = True))
    time.sleep(1)
