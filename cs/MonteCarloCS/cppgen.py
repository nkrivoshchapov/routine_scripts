from rdkit import Chem
from rdkit.Chem import AllChem
from copy import deepcopy, copy
import numpy as np
import sys
import os
import subprocess


class Structure:
    def __init__(self, name, mol, hbonds=[], poly=[], singles=[], make_copy=True):
        self.name = name
        if make_copy:
            self.mol = deepcopy(mol)
            self.hbonds = deepcopy(hbonds)
            self.poly = deepcopy(poly)
            self.sing = deepcopy(singles)
        else:
            self.mol = mol
            self.hbonds = hbonds
            self.poly = poly
            self.sing = singles
        self.changelist = []
        
    def setchangelist(self,newlist):
        self.changelist = deepcopy(newlist)
        for i in range(len(self.changelist)):
            self.changelist[i][0] = self.changelist[i][0].replace(" ","")
            self.changelist[i][1] = self.changelist[i][1].replace(" ","")
    
    def addhbond(self,newhbond,polycheck=True): #ATOM NUMBERS START FROM 1
        nhb = deepcopy(newhbond)
        for i in range(2):
            nhb[i] -= 1
        
        if nhb not in self.hbonds:
            self.hbonds.append(nhb)
            if polycheck:
                self.autopoly(nhb[0])
                self.autopoly(nhb[1])
        else:
            print("%s is already here"%(repr(newhbond)))
    
    def autopoly(self, centatom):
        centatom += 1
        print("Input: " + str(centatom))
        coord_list = []
        for bond in self.mol.GetBonds():
            at1 = bond.GetBeginAtomIdx()
            at2 = bond.GetEndAtomIdx()
            if centatom == at1:
                other_at = at2
            elif centatom == at2:
                other_at = at1
            else:
                continue
            if other_at not in coord_list:
                coord_list.append(other_at)
        print(repr(coord_list))
        if len(coord_list) == 4:
            self.poly.append(deepcopy(coord_list))
        elif len(coord_list) == 3:
            coord_list.append(centatom)
            self.poly.append(deepcopy(coord_list))
        else:
            print("can't constrain coordinational polyhedra")
        
    def addpoly(self, newpoly):
        npl = deepcopy(newpoly)
        for i in range(4):
            npl[i] -= 1
        if npl not in self.poly:
            self.poly.append(npl)
        else:
            print("%s is already here"%(repr(newpoly)))
    
    def tosing(self,newbond):
        nb = deepcopy(newbond)
        for i in range(2):
            nb[i] -= 1 
        if nb not in self.sing:
            self.sing.append(nb)
        else:
            print("%s is already here"%(repr(newhbond)))
    
    def tomol(self):
        lines = Chem.MolToMolBlock(self.mol).split("\n")
        if len(self.hbonds) > 0:
            for item in self.hbonds:
                at1Coords = np.array(self.mol.GetConformer().GetAtomPosition(item[0]))
                at2Coords = np.array(self.mol.GetConformer().GetAtomPosition(item[1]))
                maxdist = np.linalg.norm(at1Coords-at2Coords)+0.1
                lines.append("H %d %d %f"%(item[0],item[1],maxdist))
        if len(self.poly) > 0:
            # 0 X Y Z
            for item in self.poly:
                at0Coords = np.array(self.mol.GetConformer().GetAtomPosition(item[0]))
                atXCoords = np.array(self.mol.GetConformer().GetAtomPosition(item[1]))
                atYCoords = np.array(self.mol.GetConformer().GetAtomPosition(item[2]))
                atZCoords = np.array(self.mol.GetConformer().GetAtomPosition(item[3]))
                bondX = atXCoords - at0Coords
                bondY = atYCoords - at0Coords
                bondZ = atZCoords - at0Coords
                vol = np.dot(bondX,np.cross(bondY,bondZ))
                lines.append("P %d %d %d %d %f"%(item[0],item[1],item[2],item[3],vol))
        print("\n".join(lines))
    
    def cppgen(self):
        initlines = []
        emol = Chem.RWMol(self.mol)
        for bond in self.hbonds:
            emol.RemoveBond(bond[0],bond[1])
        for bond in self.sing:
            emol.RemoveBond(bond[0],bond[1])
            emol.AddBond(bond[0],bond[1],Chem.BondType.SINGLE)
        tmol = emol.GetMol()
        tmol.UpdatePropertyCache()
        Chem.GetSymmSSSR(tmol)
        initlines.append("const static int n_at = %d;"%(tmol.GetNumAtoms()))
        initlines.append("const static int n_bond = %d;"%(tmol.GetNumBonds()))
        initlines.append("const static int n_pol = %d;"%(len(self.poly)))
        smarts_torsion = "[*]~[!$(*#*)&!D1]-&!@[!$(*#*)&!D1]~[*]"
        pattern_tor = Chem.MolFromSmarts(smarts_torsion)
        torsion = list(tmol.GetSubstructMatches(pattern_tor))
        print(repr(torsion))
        check = True
        while check:
            check = False
            for bond in torsion:
                if tmol.GetBondBetweenAtoms(bond[1],bond[2]).IsInRing():
                    check = True
                    print("Bond " + str(bond) + "is between atoms " + str(bond[1]) + "-" + str(bond[2]) + " in ring")
                    torsion.remove(bond)
                elif tmol.GetBondBetweenAtoms(bond[2],bond[1]).IsInRing():
                    check = True
                    print("Bond " + str(bond) + "is between atoms " + str(bond[1]) + "-" + str(bond[2]) + " in ring")
                    torsion.remove(bond)

        for_remove = []
        for x in reversed(range(len(torsion))):
            for y in reversed(range(x)):
                if (torsion[x][1] == torsion[y][1] and torsion[x][2] == torsion[y][2]) or (torsion[x][1] == torsion[y][2] and torsion[x][2] == torsion[y][1]):
                    if torsion[y] not in for_remove:
                        for_remove.append(torsion[y])
        for item in for_remove:
            torsion.remove(item)
        initlines.append("const static int n_tor = %d;"%(len(torsion)))

        tor1 = [str(0)]
        tor2 = [str(0)]
        for item in torsion:
            tor1.append(str(item[1]+1))
            tor2.append(str(item[2]+1))
        initlines.append("const static int axes[][%d] = {{0,0},{%s},{%s}};"%(len(torsion)+1,",".join(tor1),",".join(tor2)))

        bond1 = [str(0)]
        bond2 = [str(0)]
        for bond in tmol.GetBonds():
            if ([bond.GetBeginAtomIdx(),bond.GetEndAtomIdx()] not in self.hbonds ) and ([bond.GetEndAtomIdx(),bond.GetBeginAtomIdx()] not in self.hbonds  ):
                bond1.append(str(bond.GetBeginAtomIdx()+1))
                bond2.append(str(bond.GetEndAtomIdx()+1))
            else:
                print("Bond [%d,%d] has been hidden"%(bond.GetBeginAtomIdx(),bond.GetEndAtomIdx()))
            
        initlines.append("const static int bond1[] = {%s};"%(",".join(bond1)))
        initlines.append("const static int bond2[] = {%s};"%(",".join(bond2)))
        x=[str(0.0)]
        y=[str(0.0)]
        z=[str(0.0)]
        for at in tmol.GetConformers()[0].GetPositions():
            x.append(str(at[0]))
            y.append(str(at[1]))
            z.append(str(at[2]))
        initlines.append("const static float x[] = {%s};"%(",".join(x)))
        initlines.append("const static float y[] = {%s};"%(",".join(y)))
        initlines.append("const static float z[] = {%s};"%(",".join(z)))

        maxdist = []
        mindist = []
        n_at = tmol.GetNumAtoms()
        for i in range(n_at):
            temp= [0]
            for j in range(n_at):
                temp.append(0)
            maxdist.append(deepcopy(temp))
            temp= [0]
            for j in range(n_at):
                temp.append(1.3)
            mindist.append(deepcopy(temp))
        
        for bond in tmol.GetBonds():
            j = bond.GetEndAtomIdx()
            i = bond.GetBeginAtomIdx()
            if ([i,j] not in self.hbonds) and ([j,i] not in self.hbonds):
                at1Coords = np.array(tmol.GetConformer().GetAtomPosition(i))
                at2Coords = np.array(tmol.GetConformer().GetAtomPosition(j))
                maxdist[i][j+1] = np.linalg.norm(at1Coords-at2Coords)+0.1
                maxdist[j][i+1] = np.linalg.norm(at1Coords-at2Coords)+0.1
                mindist[i][j+1] = np.linalg.norm(at1Coords-at2Coords)-0.1
                mindist[j][i+1] = np.linalg.norm(at1Coords-at2Coords)-0.1
                
        
                
        for item in self.hbonds:
            at1Coords = np.array(tmol.GetConformer().GetAtomPosition(item[0]))
            at2Coords = np.array(tmol.GetConformer().GetAtomPosition(item[1]))
            md = np.linalg.norm(at1Coords-at2Coords)+0.1
            maxdist[item[0]][item[1]+1] = md+0.1
            maxdist[item[1]][item[0]+1] = md+0.1
            mindist[item[0]][item[1]+1] = md-0.2
            mindist[item[1]][item[0]+1] = md-0.2
            
        #for bond in self.hbonds:
        #    maxdist[bond[0]][bond[1]+1] = 3.0
        #    maxdist[bond[1]][bond[0]+1] = 3.0
        #    mindist[bond[0]][bond[1]+1] = 2.5
        #    mindist[bond[1]][bond[0]+1] = 2.5
        temp = [0]
        for i in range(n_at):
            temp.append(0)
        maxdist.insert(0,deepcopy(temp))
        mindist.insert(0,deepcopy(temp))
        for i in range(n_at+1):
            for j in range(n_at+1):
                maxdist[i][j] = str(maxdist[i][j]**2)
                mindist[i][j] = str(mindist[i][j]**2)
        
        maxlines = []
        for line in maxdist:
            maxlines.append( "{%s}"%(",".join(line)) )
        initlines.append("const static float maxdist[][%d] = {%s};"%(n_at+1,",".join(maxlines)))

        minlines = []
        for line in mindist:
            minlines.append( "{%s}"%(",".join(line)) )
        initlines.append("const static float mindist[][%d] = {%s};"%(n_at+1,",".join(minlines)))
        
        poly_ats = ["{%s}"%(",".join(["0","0","0","0","0"]))]
        poly_vol = ["0"]
        for i in range(len(self.poly)):
            at0Coords = np.array(tmol.GetConformer().GetAtomPosition(self.poly[i][0]))
            atXCoords = np.array(tmol.GetConformer().GetAtomPosition(self.poly[i][1]))
            atYCoords = np.array(tmol.GetConformer().GetAtomPosition(self.poly[i][2]))
            atZCoords = np.array(tmol.GetConformer().GetAtomPosition(self.poly[i][3]))
            bondX = atXCoords - at0Coords
            bondY = atYCoords - at0Coords
            bondZ = atZCoords - at0Coords
            vol = np.dot(bondX,np.cross(bondY,bondZ))
            poly_vol.append(str(vol))
            poly_ats.append("{%s}"%(",".join(  ["0",str(self.poly[i][0]+1),str(self.poly[i][1]+1),str(self.poly[i][2]+1),str(self.poly[i][3]+1)]  )))
        initlines.append("const static float polyvol[] = {%s};"%(",".join(poly_vol)))
        initlines.append("const static int polyats[][5] = {%s};"%(",".join(poly_ats)))
        
        ch=["\"\""]
        for at in tmol.GetAtoms():
            newsubj = "\""+at.GetSymbol()+"\""
            for item in self.changelist:
                if item[1] in newsubj:
                    newsubj = newsubj.replace(item[1],item[0])
            ch.append(newsubj)
        initlines.append("const static string ch[] = {%s};"%(",".join(ch)))

        lines = open("confmpi_template.c","r").readlines()
        for i in reversed(range(len(lines))):
            if "THERE IS THE NAME" in lines[i]:
                lines[i] = lines[i].replace("THERE IS THE NAME","\""+self.name+"\"")
            if "PASTE HERE" in lines[i]:
                lines[i]=""
                for line in initlines:
                    lines.insert(i,line+"\n")
                break
        file = open(self.name+".c","w")
        file.write("".join(lines))
        file.close()


def diastereo(startmol, chir_carb, struct):
    newconf = [deepcopy(startmol)]
    for at in chir_carb:
        newconf[0].GetAtomWithIdx(at - 1).SetChiralTag(Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CW)
    for at in chir_carb:
        oldmol = copy(newconf)
        for mol in oldmol:
            newmol = deepcopy(mol)
            newmol.GetAtomWithIdx(at - 1).SetChiralTag(Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CCW)
            newconf.append(newmol)
    
    res = []
    ind = 0
    for item in newconf:
        ind += 1
        Chem.AllChem.EmbedMolecule(item)
        newitem = Structure(struct.name + "iso%d" % (ind), item, make_copy=False)
        res.append(newitem)
    return res


def savemol(mol, name):
    file = open(name+".sdf","w")
    file.write(Chem.MolToMolBlock(mol))
    file.close()


def draw(mol):
    return Chem.Draw.MolToImage(mol)


def gv(mol):
    file = open("preview.sdf","w")
    file.write(Chem.MolToMolBlock(mol))
    file.close()
    subprocess.Popen("gview preview.sdf",shell=True)


def cc(mol):
    file = open("preview.sdf","w")
    file.write(Chem.MolToMolBlock(mol))
    file.close()
    subprocess.Popen("Chemcraft preview.sdf",shell=True)
