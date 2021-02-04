import sys,os

inplines = open(sys.argv[1], "r").readlines()
prevpoint = -1
breaknext = len(inplines)-1
for line in reversed(inplines):
    if "scan point" in line:
        curpoint = int(line.split("point")[1].split("out")[0])
        if curpoint == prevpoint:
            continue
        newfile = open("nosolv_point_%d.log"%prevpoint,"w")
        newfile.write("".join(inplines[inplines.index(line):breaknext]))
        breaknext = inplines.index(line)
        newfile.close()
        prevpoint = curpoint
        
