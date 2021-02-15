import os,sys

fil1 = "peroxH.xyz"
fil2 = "btripoleB2H.xyz"
lin1 = open(fil1,"r").readlines()
lin2 = open(fil2,"r").readlines()
fil1 = open("r"+fil1,"w")
fil2 = open("r"+fil2,"w")
while True:
    text = input("")
    if text == "stop":
        fil1.close()
        fil2.close()
        sys.exit(0)
    n1 = int(text.split(" ")[0])
    n2 = int(text.split(" ")[1])
    fil1.write(lin1[n1-1])
    fil2.write(lin2[n2-1])