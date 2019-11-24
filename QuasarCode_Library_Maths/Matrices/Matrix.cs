using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;
using System.Threading.Tasks;

namespace QuasarCode.Library.Maths.Matrices
{
    public class Matrix<T> : IMatrix<T>
    {
        private readonly T[,] Data;

        private Matrix<T> MinorsCasche = null;
        private Matrix<T> CofactorsCasche = null;
        private Matrix<T> AdjointCasche = null;

        public readonly bool CaschingEnabled;

        object IMatrix.this[int row, int column]
        {
            get { return this.Data[row, column]; }
        }

        public T this[int row, int column]
        {
            get { return this.Data[row, column]; }
            protected set { this.Data[row, column] = value; }
        }

        public int Rows { get { return Data.GetUpperBound(0) - Data.GetLowerBound(0) + 1; } }

        public int Columns { get { return Data.GetUpperBound(1) - Data.GetLowerBound(1) + 1; } }

        public int[] Shape { get { return new int[] { this.Rows, this.Columns }; } }

        public Matrix(T[,] data, bool enableCasching = true)
        {
            this.Data = data;
            this.CaschingEnabled = enableCasching;
        }

        public Matrix(IMatrix<T> matrix, bool enableCasching = true)
        {
            this.Data = (T[,])matrix.GetData().Clone();
            this.CaschingEnabled = enableCasching;
        }

        object[,] IMatrix.GetData()
        {
            return (object[,])this.Data.Clone();
        }

        public T[,] GetData()
        {
            return (T[,])this.Data.Clone();
        }

        public IMatrix<double> Identity()
        {
            return IdentityMatrix.CreateNew(this.Rows);
        }

        IMatrix IMatrix.Transpose()
        {
            return this.Transpose();
        }

        public IMatrix<T> Transpose()
        {
            T[,] items = new T[this.Rows, this.Columns];

            for (int i = 0; i < this.Rows; i++)
            {
                for (int j = 0; j < this.Columns; j++)
                {
                    items[j, i] = this.Data[i, j];
                }
            }

            return new Matrix<T>(items);
        }

        IMatrix IMatrix.Minors()
        {
            return this.Minors();
        }

        public IMatrix<T> Minors()
        {
            T[,] minors = new T[this.Rows, this.Columns];

            for (int i = 0; i < this.Rows; i++)
            {
                for (int j = 0; j < this.Columns; j++)
                {
                    T[,] componentItems = new T[this.Rows - 1, this.Columns - 1];

                    int kCorrection = 0;
                    for (int k = 0; k < this.Rows; k++)
                    {
                        if (k == i)
                        {
                            kCorrection = -1;
                            continue;
                        }

                        int lCorrection = 0;
                        for (int l = 0; l < this.Columns; l++)
                        {
                            if (l == j)
                            {
                                lCorrection = -1;
                                continue;
                            }

                            componentItems[k + kCorrection, l + lCorrection] = this.Data[k, l];
                        }
                    }

                    minors[i, j] = new Matrix<T>(componentItems).Determinant();
                }
            }

            return new Matrix<T>(minors);
        }

        public T Minor(int row, int column)
        {
            if (this.CaschingEnabled)
            {
                if (this.MinorsCasche is null)
                {
                    this.Minors();
                }

                return this.MinorsCasche[row, column];
            }
            else
            {
                return this.Minors()[row, column];
            }
        }

        IMatrix IMatrix.Cofactors()
        {
            return this.Cofactors();
        }

        public IMatrix<T> Cofactors()
        {
            try
            {
                return this.Minors().ElementwiseOperation<T, double>((T a, double b) => (dynamic)a * b, Matrix<double>.SignMatrix(this.Rows, this.Columns));
            }
            catch (ArithmeticException e)//TODO: check the type of exception for invalid type for a * b
            {
                throw new InvalidOperationException("The data type of the matrix was incompatable with multiplication with doubles and therfore cofactors can't be calculated.", e);
            }
        }

        public T Cofactor(int row, int column)
        {
            if (this.CaschingEnabled)
            {
                if (this.CofactorsCasche is null)
                {
                    this.Cofactors();
                }

                return this.CofactorsCasche[row, column];
            }
            else
            {
                return this.Cofactors()[row, column];
            }
        }

        object IMatrix.Determinant()
        {
            return this.Determinant();
        }

        public T Determinant()
        {
            if (this.Rows * this.Columns == 1)
            {
                return this.Data[0, 0];
            }
            else
            {
                Func<int, int, T> getCofactor;
                if (this.CaschingEnabled)
                {
                    getCofactor = (int row, int col) => this.Data[row, col];
                }
                else
                {
                    IMatrix<T> cofactors = this.Cofactors();
                    getCofactor = (int row, int col) => cofactors[row, col];
                }

                T sum = (dynamic)this.Data[0, 0] * getCofactor(0, 0);//TODO: catch type
                for (int i = 0; i < this.Columns; i++)
                {
                    sum += (dynamic)this.Data[0, i] * getCofactor(0, i);//TODO: catch type
                }

                return sum;
            }
        }

        IMatrix IMatrix.Adjoint()
        {
            return this.Adjoint();
        }

        public IMatrix<T> Adjoint()
        {
            return this.Cofactors().Transpose();
        }

        object IMatrix.Trace()
        {
            return this.Trace();
        }

        public T Trace()
        {
            //TODO: check if square

            T sum = this.Data[0, 0];
            for (int i = 1; i < this.Rows; i++)
            {
                sum += (dynamic)this.Data[i, i];//TODO: catch type
            }

            return sum;
        }

        IMatrix IMatrix.Inverse()
        {
            return this.Inverse();
        }

        public IMatrix<T> Inverse()
        {
            return this.Adjoint().Divide(this.Determinant());
        }







        IMatrix IMatrix.Add(IMatrix matrix)
        {
            return ((IMatrix)this).ElementwiseOperation((object a, object b) => (dynamic)a + b, matrix);
        }

        public static IMatrix operator +(Matrix<T> a, IMatrix b)
        {
            return ((IMatrix)a).Add(b);
        }

        public IMatrix<T> Add(IMatrix<T> matrix)
        {
            return this.ElementwiseOperation<T, T>((T a, T b) => (dynamic)a + b, matrix);
        }

        public static Matrix<T> operator +(Matrix<T> a, IMatrix<T> b)
        {
            return (Matrix<T>)a.Add(b);
        }

        public IMatrix<T> Add(T value)
        {
            return this.ElementwiseOperation<T, T>((T a, T b) => (dynamic)a + b, value);
        }

        public static Matrix<T> operator +(Matrix<T> a, T b)
        {
            return (Matrix<T>)a.Add(b);
        }



        IMatrix IMatrix.Subtract(IMatrix matrix)
        {
            return ((IMatrix)this).ElementwiseOperation((object a, object b) => (dynamic)a - b, matrix);
        }

        public static IMatrix operator -(Matrix<T> a, IMatrix b)
        {
            return ((IMatrix)a).Subtract(b);
        }

        public IMatrix<T> Subtract(IMatrix<T> matrix)
        {
            return this.ElementwiseOperation<T, T>((T a, T b) => (dynamic)a - b, matrix);
        }

        public static Matrix<T> operator -(Matrix<T> a, IMatrix<T> b)
        {
            return (Matrix<T>)a.Subtract(b);
        }

        public IMatrix<T> Subtract(T value)
        {
            return this.ElementwiseOperation<T, T>((T a, T b) => (dynamic)a - b, value);
        }

        public static Matrix<T> operator -(Matrix<T> a, T b)
        {
            return (Matrix<T>)a.Subtract(b);
        }



        IMatrix IMatrix.Multiply(IMatrix matrix)
        {
            //TODO: check if this.Columns matches matrix.Rows

            object[,] items = new object[this.Rows, matrix.Columns];

            for (int i = 0; i < this.Rows; i++)
            {
                for (int j = 0; j < matrix.Columns; j++)
                {
                    items[i, j] = (dynamic)this.Data[i, 0] * matrix[0, j];//TODO: catch type
                    for (int l = 1; l < this.Columns; l++)
                    {
                        items[i, j] = (dynamic)this.Data[i, l] * matrix[l, j];//TODO: catch type
                    }
                }
            }

            return new Matrix<object>(items);
        }

        public static IMatrix operator *(Matrix<T> a, IMatrix b)
        {
            return ((IMatrix)a).Multiply(b);
        }

        public virtual IMatrix<T> Multiply(IMatrix<T> matrix)
        {
            //TODO: check if this.Columns matches matrix.Rows

            T[,] items = new T[this.Rows, matrix.Columns];

            for (int i = 0; i < this.Rows; i++)
            {
                for (int j = 0; j < matrix.Columns; j++)
                {
                    items[i, j] = (dynamic)this.Data[i, 0] * matrix[0, j];//TODO: catch type
                    for (int l = 1; l < this.Columns; l++)
                    {
                        items[i, j] = (dynamic)this.Data[i, l] * matrix[l, j];//TODO: catch type
                    }
                }
            }

            return new Matrix<T>(items);
        }

        public static Matrix<T> operator *(Matrix<T> a, IMatrix<T> b)
        {
            return (Matrix<T>)a.Multiply(b);
        }

        public IMatrix<T> Multiply(T value)
        {
            return this.ElementwiseOperation<T, T>((T a, T b) => (dynamic)a * b, value);
        }

        public static Matrix<T> operator *(Matrix<T> a, T b)
        {
            return (Matrix<T>)a.Multiply(b);
        }



        IMatrix IMatrix.Divide(IMatrix matrix)
        {
            return ((IMatrix)this).Multiply(matrix.Inverse());
        }

        public static IMatrix operator /(Matrix<T> a, IMatrix b)
        {
            return ((IMatrix)a).Divide(b);
        }

        public IMatrix<T> Divide(IMatrix<T> matrix)
        {
            return this.Multiply(matrix.Inverse());
        }

        public static Matrix<T> operator /(Matrix<T> a, IMatrix<T> b)
        {
            return (Matrix<T>)a.Divide(b);
        }

        public IMatrix<T> Divide(T value)
        {
            return this.ElementwiseOperation<T, T>((T a, T b) => (dynamic)a / b, value);
        }

        public static Matrix<T> operator /(Matrix<T> a, T b)
        {
            return (Matrix<T>)a.Divide(b);
        }












        public object Clone()
        {
            return new Matrix<T>((T[,])this.Data.Clone());
        }

        //TODO: catch type? error
        IMatrix IMatrix.ElementwiseOperation(Func<object, object, object> operation, IMatrix matrix)
        {
            //TODO: Check matching shape
            object[,] items = new object[this.Rows, this.Columns];

            for (int i = 0; i < this.Rows; i++)
            {
                for (int j = 0; j < this.Columns; j++)
                {
                    items[i, j] = operation(this.Data[i, j], matrix[i, j]);
                }
            }

            return new Matrix<object>(items);
        }

        IMatrix IMatrix.ElementwiseOperation(Func<object, object, object> operation, object value)
        {
            object[,] items = new object[this.Rows, this.Columns];

            for (int i = 0; i < this.Rows; i++)
            {
                for (int j = 0; j < this.Columns; j++)
                {
                    items[i, j] = operation(this.Data[i, j], value);
                }
            }

            return new Matrix<object>(items);
        }

        public IMatrix<U> ElementwiseOperation<U, V>(Func<T, V, U> operation, IMatrix<V> matrix)
        {
            //TODO: Check matching shape
            U[,] items = new U[this.Rows, this.Columns];

            for (int i = 0; i < this.Rows; i++)
            {
                for (int j = 0; j < this.Columns; j++)
                {
                    items[i, j] = operation(this.Data[i, j], matrix[i, j]);
                }
            }

            return new Matrix<U>(items);
        }

        public IMatrix<U> ElementwiseOperation<U, V>(Func<T, V, U> operation, V value)
        {
            U[,] items = new U[this.Rows, this.Columns];

            for (int i = 0; i < this.Rows; i++)
            {
                for (int j = 0; j < this.Columns; j++)
                {
                    items[i, j] = operation(this.Data[i, j], value);
                }
            }

            return new Matrix<U>(items);
        }

        public static Matrix<double> SignMatrix(int rows, int cols)
        {
            double[,] items = new double[rows, cols];
            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < cols; j++)
                {
                    items[i, j] = QuasarCode.Library.Tools.Validators.IsEven(i + j) ? 1 : -1;
                }
            }

            return new Matrix<double>(items, enableCasching: false);
        }
    }
}
