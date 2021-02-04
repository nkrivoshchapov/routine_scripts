import os,sys,glob

sumfile = open("summary.csv","w")
sumfile.write("Molecule,NBO\n")

for log in glob.glob("./*log"):
    totener = 0
    print(log)
    file = open(log,"r").readlines()
    starts = 0
    stops = 0
    bases=[]
    for line in file:
        if "Second Order Perturbation Theory Analysis of Fock Matrix" in line:
            starts = file.index(line)+8
        if "Natural Bond Orbitals (Summary)" in line:
            stops = file.index(line) - 3
            print(str(stops))
    for i in range(starts,stops):
        line = file[i]
        if "RY" not in line:
            donor=line[6:37].strip()
            accep=line[43:76].strip()
            ener=line[77:84].strip()
            if "LP" in donor and "O" in donor and "C" in accep and "O" in accep:
                bases.append([donor,accep,ener])
                totener+=float(ener)
    file = open(log.split("\\")[1].split(".")[0]+"_nbo.csv","w")
    sumfile.write(log+","+str(totener)+"\n")
    file.write("Donor,Acceptor,Energy\n")
    for line in bases:
        file.write(",".join(line)+"\n")
    file.close()
sumfile.close()
    