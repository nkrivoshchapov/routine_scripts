import glob,os,sys
from shutil import copy2

for calcdir in glob.glob("./*"):
    if os.path.isdir(calcdir):
        try:
            lines = open(calcdir+"/LOGFILE","r").readlines()
        except:
            print("Couldn't read logfile for "+calcdir)
            continue
        good = False
        for line in reversed(lines):
            if "GEOMETRY OPTIMIZATION CONVERGED" in line:
                good = True
                break
        if good:
            copy2(calcdir+"/xtbopt.xyz", calcdir+".xyz")
        else:
            print("Not normal termination for " + calcdir)
