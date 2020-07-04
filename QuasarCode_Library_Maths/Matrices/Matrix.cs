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

        public Func<T, T, T> AddItems { get; }
        public Func<T, T, T> SubtractItems { get; }
        public Func<T, T, T> MultiplyItems { get; }
        public Func<T, T, T> DivideItems { get; }
        public Func<T, double, T> MultiplyByDouble { get; }

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

        public Matrix(T[,] data, Func<T, T, T> addItems, Func<T, T, T> subtractItems, Func<T, T, T> multiplyItems, Func<T, T, T> divideItems, Func<T, double, T> multiplyByDouble, bool enableCasching = true)
        {
            this.Data = data;
            this.CaschingEnabled = enableCasching;
            this.AddItems = addItems;
            this.SubtractItems = subtractItems;
            this.MultiplyItems = multiplyItems;
            this.DivideItems = divideItems;
            this.MultiplyByDouble = multiplyByDouble;
        }

        public Matrix(IMatrix<T> matrix, bool enableCasching = true)
        {
            this.Data = (T[,])matrix.GetData().Clone();
            this.CaschingEnabled = enableCasching;
            this.AddItems = matrix.AddItems;
            this.SubtractItems = matrix.SubtractItems;
            this.MultiplyItems = matrix.MultiplyItems;
            this.DivideItems = matrix.DivideItems;
            this.MultiplyByDouble = matrix.MultiplyByDouble;
        }

        protected Matrix(T[,] data, IMatrix<T> matrix, bool enableCasching = true)
        {
            this.Data = data;
            this.CaschingEnabled = enableCasching;
            this.AddItems = matrix.AddItems;
            this.SubtractItems = matrix.SubtractItems;
            this.MultiplyItems = matrix.MultiplyItems;
            this.DivideItems = matrix.DivideItems;
            this.MultiplyByDouble = matrix.MultiplyByDouble;
        }

        object[,] IMatrix.GetData()
        {
            return (object[,])this.Data.Clone();
        }

        public T[,] GetData()
        {
            return (T[,])this.Data.Clone();
        }

        IMatrix<double> IMatrix.Identity()
        {
            return IdentityMatrix.CreateNew(this.Rows);
        }

        public IdentityMatrix Identity()
        {
            return IdentityMatrix.CreateNew(this.Rows);
        }

        IMatrix IMatrix.Transpose()
        {
            return this.Transpose();
        }

        IMatrix<T> IMatrix<T>.Transpose()
        {
            return this.Transpose();
        }

        public Matrix<T> Transpose()
        {
            T[,] items = new T[this.Rows, this.Columns];

            for (int i = 0; i < this.Rows; i++)
            {
                for (int j = 0; j < this.Columns; j++)
                {
                    items[j, i] = this.Data[i, j];
                }
            }

            return new Matrix<T>(items, this);
        }

        IMatrix IMatrix.Minors()
        {
            return this.Minors();
        }

        IMatrix<T> IMatrix<T>.Minors()
        {
            return this.Minors();
        }

        public Matrix<T> Minors()
        {
            if (this.CaschingEnabled && !(this.MinorsCasche is null))
            {
                return this.MinorsCasche.Clone();
            }
            else
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

                        minors[i, j] = new Matrix<T>(componentItems, this).Determinant();
                    }
                }

                if (this.CaschingEnabled)
                {
                    this.MinorsCasche = new Matrix<T>(minors, this);
                    return this.MinorsCasche.Clone();
                }
                else
                {
                    return new Matrix<T>(minors, this);
                }
            }
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

        IMatrix<T> IMatrix<T>.Cofactors()
        {
            return this.Cofactors();
        }

        public Matrix<T> Cofactors()
        {
            if (this.CaschingEnabled && !(this.CofactorsCasche is null))
            {
                return this.CofactorsCasche.Clone();
            }
            else
            {
                if (this.CaschingEnabled)
                {
                    this.CofactorsCasche = this.Minors().ElementwiseOperation(this.MultiplyByDouble, Matrix<double>.SignMatrix(this.Rows, this.Columns));
                    return this.CofactorsCasche.Clone();
                }
                else
                {
                    return this.Minors().ElementwiseOperation(this.MultiplyByDouble, Matrix<double>.SignMatrix(this.Rows, this.Columns));
                }

                //try
                //{
                //    if (this.CaschingEnabled)
                //    {
                //        this.CofactorsCasche = this.Minors().ElementwiseOperation<T, double>((T a, double b) => (dynamic)a * b, Matrix<double>.SignMatrix(this.Rows, this.Columns));
                //        return this.CofactorsCasche.Clone();
                //    }
                //    else
                //    {
                //        return this.Minors().ElementwiseOperation<T, double>((T a, double b) => (dynamic)a * b, Matrix<double>.SignMatrix(this.Rows, this.Columns));
                //    }
                //}
                //catch (ArithmeticException e)//TODO: check the type of exception for invalid type for a * b
                //{
                //    throw new InvalidOperationException("The data type of the matrix was incompatable with multiplication with doubles and therfore cofactors can't be calculated.", e);
                //}
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

                T sum = this.MultiplyItems(this.Data[0, 0], getCofactor(0, 0));
                for (int i = 0; i < this.Columns; i++)
                {
                    sum = this.AddItems(sum, this.MultiplyItems(this.Data[0, i], getCofactor(0, i)));
                }

                return sum;
            }
        }

        IMatrix IMatrix.Adjoint()
        {
            return this.Adjoint();
        }

        IMatrix<T> IMatrix<T>.Adjoint()
        {
            return this.Adjoint();
        }

        public Matrix<T> Adjoint()
        {
            if (this.CaschingEnabled && !(this.AdjointCasche is null))
            {
                return this.AdjointCasche.Clone();
            }
            else
            {
                if (this.CaschingEnabled)
                {
                    this.AdjointCasche = this.Cofactors().Transpose();
                    return this.AdjointCasche.Clone();
                }
                else
                {
                    return this.Cofactors().Transpose();
                }
            }
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
                sum = this.AddItems(sum, this.Data[i, i]);
            }

            return sum;
        }

        IMatrix IMatrix.Inverse()
        {
            return this.Inverse();
        }

        IMatrix<T> IMatrix<T>.Inverse()
        {
            return this.Inverse();
        }

        public Matrix<T> Inverse()
        {
            return this.Adjoint() / this.Determinant();
        }







        IMatrix IMatrix.Add(IMatrix matrix)
        {
            return ((IMatrix)this).ElementwiseOperation((object a, object b) => (dynamic)a + b, matrix);//TODO: catch type? error
        }

        public static IMatrix operator +(Matrix<T> a, IMatrix b)
        {
            return ((IMatrix)a).Add(b);
        }

        public IMatrix<T> Add(IMatrix<T> matrix)
        {
            return this.ElementwiseOperation(this.AddItems, matrix);//TODO: catch type? error
        }

        public static Matrix<T> operator +(Matrix<T> a, IMatrix<T> b)
        {
            return (Matrix<T>)a.Add(b);
        }

        public IMatrix<T> Add(T value)
        {
            return this.ElementwiseOperation(this.AddItems, value);//TODO: catch type? error
        }

        public static Matrix<T> operator +(Matrix<T> a, T b)
        {
            return (Matrix<T>)a.Add(b);
        }



        IMatrix IMatrix.Subtract(IMatrix matrix)
        {
            return ((IMatrix)this).ElementwiseOperation((object a, object b) => (dynamic)a - b, matrix);//TODO: catch type? error
        }

        public static IMatrix operator -(Matrix<T> a, IMatrix b)
        {
            return ((IMatrix)a).Subtract(b);
        }

        public IMatrix<T> Subtract(IMatrix<T> matrix)
        {
            return this.ElementwiseOperation(this.SubtractItems, matrix);//TODO: catch type? error
        }

        public static Matrix<T> operator -(Matrix<T> a, IMatrix<T> b)
        {
            return (Matrix<T>)a.Subtract(b);
        }

        public IMatrix<T> Subtract(T value)
        {
            return this.ElementwiseOperation(this.SubtractItems, value);//TODO: catch type? error
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

            return new OMatrix(items);
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
                    items[i, j] = this.MultiplyItems(this.Data[i, 0], matrix[0, j]);//TODO: catch type
                    for (int l = 1; l < this.Columns; l++)
                    {
                        items[i, j] = this.AddItems(items[i, j], this.MultiplyItems(this.Data[i, l], matrix[l, j]));//TODO: catch type
                    }
                }
            }

            return new Matrix<T>(items, this);
        }

        public static Matrix<T> operator *(Matrix<T> a, IMatrix<T> b)
        {
            return (Matrix<T>)a.Multiply(b);
        }

        public IMatrix<T> Multiply(T value)
        {
            return this.ElementwiseOperation(this.MultiplyItems, value);//TODO: catch type? error
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
            return this.ElementwiseOperation(this.DivideItems, value);
        }

        public static Matrix<T> operator /(Matrix<T> a, T b)
        {
            return (Matrix<T>)a.Divide(b);
        }












        object ICloneable.Clone()
        {
            return this.Clone();
        }

        public Matrix<T> Clone()
        {
            return new Matrix<T>((T[,])this.Data.Clone(), this);
        }

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

            return new OMatrix(items);
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

            return new OMatrix(items);
        }

        IMatrix<U> IMatrix<T>.ElementwiseOperation<U, V>(Func<T, V, U> operation, IMatrix<V> matrix, Func<U, U, U> addItems, Func<U, U, U> subtractItems, Func<U, U, U> multiplyItems, Func<U, U, U> divideItems, Func<U, double, U> multiplyByDouble)
        {
            return this.ElementwiseOperation(operation, matrix, addItems, subtractItems, multiplyItems, divideItems, multiplyByDouble);
        }

        IMatrix<U> IMatrix<T>.ElementwiseOperation<U, V>(Func<T, V, U> operation, V value, Func<U, U, U> addItems, Func<U, U, U> subtractItems, Func<U, U, U> multiplyItems, Func<U, U, U> divideItems, Func<U, double, U> multiplyByDouble)
        {
            return this.ElementwiseOperation(operation, value, addItems, subtractItems, multiplyItems, divideItems, multiplyByDouble);
        }

        IMatrix<T> IMatrix<T>.ElementwiseOperation<V>(Func<T, V, T> operation, IMatrix<V> matrix)
        {
            return this.ElementwiseOperation(operation, matrix);
        }

        IMatrix<T> IMatrix<T>.ElementwiseOperation<V>(Func<T, V, T> operation, V value)
        {
            return this.ElementwiseOperation(operation, value);
        }

        public Matrix<U> ElementwiseOperation<U, V>(Func<T, V, U> operation, IMatrix<V> matrix, Func<U, U, U> addItems, Func<U, U, U> subtractItems, Func<U, U, U> multiplyItems, Func<U, U, U> divideItems, Func<U, double, U> multiplyByDouble)
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

            return new Matrix<U>(items, addItems, subtractItems, multiplyItems, divideItems, multiplyByDouble);
        }

        public Matrix<U> ElementwiseOperation<U, V>(Func<T, V, U> operation, V value, Func<U, U, U> addItems, Func<U, U, U> subtractItems, Func<U, U, U> multiplyItems, Func<U, U, U> divideItems, Func<U, double, U> multiplyByDouble)
        {
            U[,] items = new U[this.Rows, this.Columns];

            for (int i = 0; i < this.Rows; i++)
            {
                for (int j = 0; j < this.Columns; j++)
                {
                    items[i, j] = operation(this.Data[i, j], value);
                }
            }

            return new Matrix<U>(items, addItems, subtractItems, multiplyItems, divideItems, multiplyByDouble);
        }

        public Matrix<T> ElementwiseOperation<V>(Func<T, V, T> operation, IMatrix<V> matrix)
        {
            //TODO: Check matching shape
            T[,] items = new T[this.Rows, this.Columns];

            for (int i = 0; i < this.Rows; i++)
            {
                for (int j = 0; j < this.Columns; j++)
                {
                    items[i, j] = operation(this.Data[i, j], matrix[i, j]);
                }
            }

            return new Matrix<T>(items, this);
        }

        public Matrix<T> ElementwiseOperation<V>(Func<T, V, T> operation, V value)
        {
            T[,] items = new T[this.Rows, this.Columns];

            for (int i = 0; i < this.Rows; i++)
            {
                for (int j = 0; j < this.Columns; j++)
                {
                    items[i, j] = operation(this.Data[i, j], value);
                }
            }

            return new Matrix<T>(items, this);
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

            return new NMatrix(items, enableCasching: false);
        }



        IMatrix IMatrix.RowSwap(int row1, int row2)
        {
            return this.RowSwap(row1, row2);
        }

        IMatrix<T> IMatrix<T>.RowSwap(int row1, int row2)
        {
            return this.RowSwap(row1, row2);
        }

        public Matrix<T> RowSwap(int row1, int row2)
        {
            Matrix<T> result = this.Clone();

            for (int i = 0; i < this.Columns; i++)
            {
                result[row1, i] = this.Data[row2, i];
                result[row2, i] = this.Data[row1, i];
            }

            return result;
        }

        IMatrix IMatrix.ColumnSwap(int column1, int column2)
        {
            return this.ColumnSwap(column1, column2);
        }

        IMatrix<T> IMatrix<T>.ColumnSwap(int column1, int column2)
        {
            return this.ColumnSwap(column1, column2);
        }

        public Matrix<T> ColumnSwap(int column1, int column2)
        {
            Matrix<T> result = this.Clone();

            for (int i = 0; i < this.Rows; i++)
            {
                result[i, column1] = this.Data[i, column2];
                result[i, column2] = this.Data[i, column1];
            }

            return result;
        }

        IMatrix IMatrix.RowMultiply(int targetRow, object multiplier)
        {
            Matrix<T> result = this.Clone();

            for (int i = 0; i < this.Columns; i++)
            {
                result[targetRow, i] = (dynamic)this.Data[targetRow, i] * multiplier;//TODO: type check
            }

            return result;
        }

        IMatrix<T> IMatrix<T>.RowMultiply(int targetRow, T multiplier)
        {
            return this.RowMultiply(targetRow, multiplier);
        }

        public Matrix<T> RowMultiply(int targetRow, T multiplier)
        {
            Matrix<T> result = this.Clone();

            for (int i = 0; i < this.Columns; i++)
            {
                result[targetRow, i] = this.MultiplyItems(this.Data[targetRow, i], multiplier);
            }

            return result;
        }

        IMatrix IMatrix.ColumnMultiply(int targetColumn, object multiplier)
        {
            Matrix<T> result = this.Clone();

            for (int i = 0; i < this.Rows; i++)
            {
                result[i, targetColumn] = (dynamic)this.Data[i, targetColumn] * multiplier;//TODO: type check
            }

            return result;
        }

        IMatrix<T> IMatrix<T>.ColumnMultiply(int targetColumn, T multiplier)
        {
            return this.ColumnMultiply(targetColumn, multiplier);
        }

        public Matrix<T> ColumnMultiply(int targetColumn, T multiplier)
        {
            Matrix<T> result = this.Clone();

            for (int i = 0; i < this.Rows; i++)
            {
                result[i, targetColumn] = this.MultiplyItems(this.Data[i, targetColumn], multiplier);
            }

            return result;
        }

        IMatrix IMatrix.RowSum(int targetRow, int operandRow, object multiplier)
        {
            Matrix<T> result = this.Clone();

            for (int i = 0; i < this.Columns; i++)
            {
                result[targetRow, i] = (dynamic)this.Data[targetRow, i] + (dynamic)this.Data[operandRow, i] * multiplier;//TODO: type check
            }

            return result;
        }

        IMatrix<T> IMatrix<T>.RowSum(int targetRow, int operandRow, T multiplier)
        {
            return this.RowSum(targetRow, operandRow, multiplier);
        }

        public Matrix<T> RowSum(int targetRow, int operandRow, T multiplier)
        {
            Matrix<T> result = this.Clone();

            for (int i = 0; i < this.Columns; i++)
            {
                result[targetRow, i] = this.AddItems(result[targetRow, i], this.MultiplyItems(this.Data[operandRow, i], multiplier));
            }

            return result;
        }

        IMatrix IMatrix.ColumnSum(int targetColumn, int operandColumn, object multiplier)
        {
            Matrix<T> result = this.Clone();

            for (int i = 0; i < this.Rows; i++)
            {
                result[i, targetColumn] += (dynamic)this.Data[i, operandColumn] * multiplier;//TODO: type check
            }

            return result;
        }

        IMatrix<T> IMatrix<T>.ColumnSum(int targetColumn, int operandColumn, T multiplier)
        {
            return this.ColumnSum(targetColumn, operandColumn, multiplier);
        }

        public Matrix<T> ColumnSum(int targetColumn, int operandColumn, T multiplier)
        {
            Matrix<T> result = this.Clone();

            for (int i = 0; i < this.Rows; i++)
            {
                result[i, targetColumn] = this.AddItems(result[i, targetColumn], this.MultiplyItems(this.Data[i, operandColumn], multiplier));
            }

            return result;
        }




        public override string ToString()
        {
            string[,] itemStrings = new string[this.Rows, this.Columns];
            int maxLength = 0;
            for (int i = 0; i < this.Rows; i++)
            {
                for (int j = 0; j < this.Columns; j++)
                {
                    itemStrings[i, j] += this.Data[i, j].ToString();

                    if (itemStrings[i, j].Length > maxLength)
                    {
                        maxLength = itemStrings[i, j].Length;
                    }
                }
            }

            string result = "";

            int width = (maxLength + 1) * this.Columns + 1;
            string topAndBottomLines = "";
            for (int i = 0; i < width; i++)
            {
                if (i == 0 || i == 1 || i == width - 2 || i == width - 1)
                {
                    topAndBottomLines += "-";
                }
                else
                {
                    topAndBottomLines += " ";
                }
            }


            result += topAndBottomLines + "\n";

            for (int i = 0; i < this.Rows; i++)
            {
                result += "|";
                for (int j = 0; j < this.Columns; j++)
                {
                    result += itemStrings[i, j];

                    for (int counter = 0; counter < maxLength - itemStrings[i, j].Length; counter++)
                    {
                        result += " ";
                    }

                    if (j != this.Columns - 1)
                    {
                        result += " ";
                    }
                    else
                    {
                        result += "|";
                    }
                }

                result += "\n";
            }

            result += topAndBottomLines;

            return result;
        }
    }
}