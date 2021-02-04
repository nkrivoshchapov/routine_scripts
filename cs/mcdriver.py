import os, sys, subprocess, time
from shutil import copy2
nproc = int(sys.argv[1])
NCONF = 400
for file in (os.listdir("./")):
    if file.endswith(".mc"):
        print("Performing Monte-Carlo CS for " + file.split(".")[0])

        procs = []
        for i in range(1,nproc+1):
            print("./"+file + " "+ str(i))
            procs.append(subprocess.Popen("./"+file + " " + str(i),shell=True))
        while True:
            print("Checking...")
            count = 0
            for i in os.listdir("./temp_xyz"):
                if ".xyz" in i and file.split(".")[0] in i:
                    count += 1
            if count >= NCONF:
                break
            else:
                time.sleep(1)
            print(str(count))
        for proc in procs:
            print("Termination...")
            proc.terminate()
