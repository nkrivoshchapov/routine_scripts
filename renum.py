import os,sys

fil1 = "peroxH.xyz"
fil2 = "btripoleB2H.xyz"
lin1 = open(fil1,"r").readlines()
lin2 = open(fil2,"r").readlines()
fil1 = open("r"+fil1,"w")
fil2 = open("r"+fil2,"w")
while True:
    text = input("")
    if text == "kek":
        fil1.close()
        fil2.close()
        sys.exit(0)
    n1 = int(text.split(" ")[0])
    n2 = int(text.split(" ")[1])
    fil1.write(lin1[n1-1])
    fil2.write(lin2[n2-1])
    
"""
1 16
2 18
3 17
4 19
5 4
6 5
7 7
8 6
9 24
10 3
11 23
12 12
13 15
14 14
15 13
16 8
17 10
18 9
19 11
20 2
21 21
22 1
22 20
23 27
24 28
25 25
26 22
27 26
28 29
29 30
kek"""
    
    
    