#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <stdio.h>
#include "vector.h"
#include <math.h>
using namespace std;
Vector::Vector(){
	cord=(float*)malloc(sizeof(float)*3);
	cord--;
	cord[1]=0;
	cord[2]=0;
	cord[3]=0;
}

Vector::Vector(float **xyz, int myrow){
	cord=(float*)malloc(sizeof(float)*3);
	cord--;
	for(int i =1;i<4;++i)
		cord[i]=xyz[i][myrow];
}

Vector::Vector(float *xyz){
	cord=(float*)malloc(sizeof(float)*3);
	cord--;
	for(int i =1;i<4;++i)
		cord[i]=xyz[i];
}

Vector::Vector(float x,float y,float z) {
	cord=(float*)malloc(sizeof(float)*3);
	cord--;
	cord[1]=x;
	cord[2]=y;
	cord[3]=z;
}

void Vector::getrandom(){
	srand (time(NULL));
	cord[1]=((float)rand())/RAND_MAX+1;
	cord[2]=((float)rand())/RAND_MAX+1;
	cord[3]=((float)rand())/RAND_MAX+1;
}

Vector::~Vector() {
	free(++cord);
}

Vector Vector::operator+ (const Vector& b){
	Vector c(0,0,0);
	for(int i =1;i<4;++i)
		c.cord[i] = this->cord[i] + b.cord[i];
	return c;
}

Vector Vector::operator- (const Vector& b){
	Vector c(0,0,0);
	for(int i =1;i<4;++i)
		c.cord[i] = this->cord[i] - b.cord[i];
	return c;
}

void Vector::setvec(const Vector& a){
	for(int i =1;i<4;++i)
		cord[i] = a.cord[i];
}

void Vector::set_norm(){
	float res=0;
	for(int i =1;i<4;++i)
		res += cord[i]*cord[i];
	res = sqrt(res);
	for(int i =1;i<4;++i)
		cord[i] = cord[i]/res;
}

Vector cross(const Vector& a, const Vector& b) {
	Vector c(0,0,0);
	c.cord[1] = a.cord[2]*b.cord[3]-a.cord[3]*b.cord[2];
	c.cord[2] = a.cord[3]*b.cord[1]-a.cord[1]*b.cord[3];
	c.cord[3] = a.cord[1]*b.cord[2]-a.cord[2]*b.cord[1];
	return c;
}

float dot(const Vector& a, const Vector& b) {
	float res;
	for(int i=1; i<4;++i)
		res += a.cord[i]*b.cord[i];
	return res;
}

void Vector::print() {
	std::cout << "("<<cord[1] << "," << cord[2] << "," << cord[3] << ")\n";
}


void Vector::put(float **xyz, int myrow){
	for(int i =1;i<4;++i)
		xyz[i][myrow]=cord[i];
}

Matrix::Matrix(){
	col1 = (float*)malloc(sizeof(float)*3);
	col2 = (float*)malloc(sizeof(float)*3);
	col3 = (float*)malloc(sizeof(float)*3);
	cols = (float**)malloc(sizeof(float*)*3);
	cols--; col1--;col2--;col3--;
	cols[1] = col1; cols[2] = col2; cols[3] = col3; 
	for(int i =1;i<4;++i){
		col1[i] = 0;
		col2[i] = 0;
		col3[i] = 0;
	}
}

Matrix::Matrix(const Vector& x,const Vector& y,const Vector& z){
	col1 = (float*)malloc(sizeof(float)*3);
	col2 = (float*)malloc(sizeof(float)*3);
	col3 = (float*)malloc(sizeof(float)*3);
	cols = (float**)malloc(sizeof(float*)*3);
	cols--; col1--;col2--;col3--;
	cols[1] = col1; cols[2] = col2; cols[3] = col3; 
	for(int i =1;i<4;++i){
		cols[1][i] = x.cord[i];
		cols[2][i] = y.cord[i];
		cols[3][i] = z.cord[i];
	}
}

Matrix::Matrix(float angle){
	Vector x(1,0,0);
	Vector y(0,cos(angle),sin(angle));
	Vector z(0,-sin(angle),cos(angle));
	
	col1 = (float*)malloc(sizeof(float)*3);
	col2 = (float*)malloc(sizeof(float)*3);
	col3 = (float*)malloc(sizeof(float)*3);
	cols = (float**)malloc(sizeof(float*)*3);
	cols--; col1--;col2--;col3--;
	cols[1] = col1; cols[2] = col2; cols[3] = col3; 

	for(int i =1;i<4;++i){
		cols[1][i] = x.cord[i];
		cols[2][i] = y.cord[i];
		cols[3][i] = z.cord[i];
	}
}

Matrix::~Matrix(){
	free(++col1);
	free(++col2);
	free(++col3);
	free(++cols);
}

Matrix matmul(const Matrix& a, const Matrix& b){
	Matrix res = Matrix();
	for(int i = 1; i<4; ++i)
		for(int j = 1; j<4; ++j)
			for(int k = 1; k<4; ++k)
				res.cols[i][j] += a.cols[k][j]*b.cols[i][k];
	return res;
}

void Matrix::setmat(const Matrix& a){
	for(int i = 1; i < 4; i++)
        for(int j = 1; j < 4; j++) {
			cols[i][j] = a.cols[i][j];
			//cout << i << "  " << j << endl;
		}
}

void Matrix::printMat() {
	cout << cols[1][1] << "\t" << cols[2][1] << "\t" << cols[3][1] << endl;
	cout << cols[1][2] << "\t" << cols[2][2] << "\t" << cols[3][2] << endl;
	cout << cols[1][3] << "\t" << cols[2][3] << "\t" << cols[3][3] << endl;
}

void Matrix::transpose(){
	float c;
	
	c = cols[1][3];
	cols[1][3] = cols[3][1];
	cols[3][1] = c;
	
	c = cols[2][3];
	cols[2][3] = cols[3][2];
	cols[3][2] = c;
	
	c = cols[1][2];
	cols[1][2] = cols[2][1];
	cols[2][1] = c;
}

void matvec(const Matrix& mat, Vector *vec){
	float newvec[4];
	for(int i = 1; i<4;++i)
		newvec[i] = 0;
	for(int i = 1; i<4;++i)
		for(int j = 1; j<4;++j)
			newvec[i] += mat.cols[j][i]*vec->cord[j];
	for(int i = 1; i<4;++i)
		vec->cord[i] = newvec[i];
}