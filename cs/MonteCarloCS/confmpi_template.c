#include <iostream>
#include <stdlib.h>
#include <ctime>
#include <fstream>
#include <stdio.h>
#include "vector.h"
#include <cstdlib>
#include <time.h>
#include <math.h>
#include "randutils.hpp"
#define MAXCONF 500
using namespace std;

static int guessnum;
static bool checkinit;

PASTE HERE

Vector cross(const Vector&,const Vector&);
float dot(const Vector&,const Vector&);
Matrix matmul(const Matrix&, const Matrix&);
void matvec(const Matrix&, Vector*);
static char *name;

void walk(bool **carry, int start, int other, const int* bond1, const int* bond2, int numb){
	carry[numb][start] = true;
	int i;
	for(i=1;i<n_bond+1;++i){
		if((start==bond1[i])&&(other!=bond2[i])&&(!carry[numb][bond2[i]])){
			carry[numb][bond2[i]] = true;
			walk(carry, bond2[i], start, bond1, bond2, numb);
		} else if((start==bond2[i])&&(other!=bond1[i])&&(!carry[numb][bond1[i]])) {
			carry[numb][bond1[i]] = true;
			walk(carry, bond1[i], start, bond1, bond2, numb);
		}
	}
	
}

void gen_tors(float *torsions){
	static randutils::mt19937_rng rng;
	for(int i = 1;i<n_tor+1;++i){
		torsions[i] = rng.uniform(0.0,6.29);
	}
}

void restore_conf(Vector *cxyz, Vector *xyz){
	for(int i = 1; i<n_at+1;++i)
		cxyz[i].setvec(xyz[i]);
}

bool check_conf(Vector *cxyz, const int *bonds[2]){
	float dd;
	for(int i = 1; i < n_at+1; ++i)
		for(int j = 1; j < i; ++j){
			dd = pow(cxyz[i].cord[1]-cxyz[j].cord[1],2) + pow(cxyz[i].cord[2]-cxyz[j].cord[2],2) + pow(cxyz[i].cord[3]-cxyz[j].cord[3],2);
			if ((dd < mindist[i][j])||(maxdist[i][j] > 0.001)&&(dd > maxdist[i][j])){
				return false;
			}
		}
	float test;
	for(int i =1; i<n_pol+1;++i)
	{
		test = dot(	cxyz[polyats[i][2]]-cxyz[polyats[i][1]]	,	cross(	cxyz[polyats[i][3]]-cxyz[polyats[i][1]], cxyz[polyats[i][4]]-cxyz[polyats[i][1]]	));
		if(abs(polyvol[i]) < 0.0001){
			if(abs(test) > 0.001)
				return false;
		} else {
			if(abs((test-polyvol[i])/polyvol[i]) > 0.1)
				return false;
		}
		
		
	}
	return true;
}

int main(int argc, char *argv[]){
	name = THERE IS THE NAME;
	char filename[100];
	bool **carry = (bool**)malloc(sizeof(bool*)*(n_tor));
	carry--;
	int i,j;
	for(i=1;i<n_tor+1;i++) {
		carry[i] = (bool*)malloc(sizeof(bool)*(n_at));
		carry[i]--;
	}
	
	for(i=1;i<n_at+1;i++)
		for(j=1;j<n_tor+1;j++)
			carry[j][i] = false;
	int thrnum,confnum;
	thrnum=atoi(argv[1]);
	confnum=0;
	srand(time(NULL));
	
	for(i=1;i<n_tor+1;++i)
		walk(carry,axes[1][i],axes[2][i],bond1,bond2,i);
	
	float *torsions = (float*)malloc(sizeof(float)* n_tor);
	Vector *cxyz = new Vector[n_at];
	Vector *xyz = new Vector[n_at];
	const int *bonds[2];
	bonds[1]=bond1;bonds[2]=bond2;
	
	xyz--;cxyz--;torsions--;
	int conf_count=0;
	for(int i =1; i<n_at+1; ++i)
		xyz[i].setvec(Vector(x[i],y[i],z[i]));
	checkinit=false;
	Vector a = Vector();
	Vector b = Vector();
	Vector ex = Vector();
	Vector ey = Vector();
	Vector ez = Vector();
	Matrix basch = Matrix();
	Matrix baschinv = Matrix();
	Matrix rot = Matrix();
	Matrix fullmat = Matrix();
	int subtotal=0;
	while(confnum < MAXCONF){
		gen_tors(torsions);
		restore_conf(cxyz, xyz);
		for(int i = 1; i<n_tor+1; ++i){
			a.setvec(cxyz[axes[1][i]]);
			b.setvec(cxyz[axes[2][i]]);
			ex.setvec(b-a);
			ex.set_norm();
			ey.getrandom();
			ey.set_norm();
			ey.setvec(ey + ex);
			ey.setvec(cross(ey,ex));
			ey.set_norm();
			ez.setvec(cross(ex,ey));
			basch.setmat(Matrix(ex,ey,ez));
			baschinv.setmat(Matrix(ex,ey,ez));
			baschinv.transpose();
			rot.setmat(Matrix(torsions[i]));
			fullmat.setmat(matmul(basch,rot));
			fullmat.setmat(matmul(fullmat,baschinv));
			for(int j=1;j<n_at+1;++j)
				if(carry[i][j]) {
					cxyz[j].setvec(cxyz[j]-a);
					matvec(fullmat,cxyz+j);
					cxyz[j].setvec(cxyz[j]+a);
				}
		}
		
		if(check_conf(cxyz,bonds)){
			ofstream myfile;
			char filename[100];
			sprintf(filename,"./temp_xyz/conf_%s_%d_%d.xyz",name,thrnum,++confnum);
			myfile.open(filename);
			myfile << n_at << endl;
			for(int i = 1; i<n_at+1;++i)
				myfile << ch[i] <<"\t" << cxyz[i].cord[1]<<"\t" << cxyz[i].cord[2]<<"\t" << cxyz[i].cord[3] << endl;
			myfile.close();
		}
	}

	delete[] ++cxyz;
	delete[] ++xyz;
	for(i=1;i<n_tor+1;i++)
		free(++carry[i]);
	free(++carry);
	return 0;
}
