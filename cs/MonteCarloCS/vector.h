#ifndef VECTOR_H
#define VECTOR_H

class Vector {
	public:
		Vector();
		Vector(float **, int);
		Vector(float *);
		Vector(float,float,float);
		~Vector();
		Vector operator+(const Vector&);
		Vector operator-(const Vector&);
		void setvec(const Vector&);
		Vector operator/(const float&);
		void set_norm();
		void getrandom();
		void print();
		void put(float **,int);
		Vector cross(const Vector&,const Vector&);
		float *cord;
};	

#endif //VECTOR

#ifndef MATRIX_H
#define MATRIX_H

class Matrix {
	public:
		Matrix();
		Matrix(const Vector&,const Vector&,const Vector&);
		Matrix(float);
		~Matrix();
		void setmat(const Matrix&);
		void transpose();
		void printMat();
		float *col1,*col2,*col3,**cols;
		
};	

#endif //MATRIX