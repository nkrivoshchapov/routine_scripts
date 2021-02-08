import os, sys
from shutil import move
loglines = open("nohup.out","r").readlines()
for i, line in enumerate(loglines):
    if "Performing" in line and "monoperoxNCycleBiso3" not in line:
        name = line.split("for ")[1].replace("\n", "").replace("\r","")
        try:
            move("./%s.c" % name, "./c_files/")
            os.remove("./%s.mc" % name)
        except:
            pass
