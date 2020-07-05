using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Matrices
{
    public partial interface IMatrix : ICloneable
    {
        int Rows { get; }
        int Columns { get; }
        int[] Shape { get; }

        object this[int row, int column] { get; }

        object[,] GetData();

        IMatrix<double> Identity();

        IMatrix Transpose();

        IMatrix Minors();

        IMatrix Cofactors();

        object Determinant();

        IMatrix Adjoint();

        object Trace();

        IMatrix Inverse();

        IMatrix Add(IMatrix matrix);

        IMatrix Subtract(IMatrix matrix);

        IMatrix Multiply(IMatrix matrix);

        IMatrix Divide(IMatrix matrix);

        IMatrix ElementwiseOperation(Func<object, object, object> operation, IMatrix matrix);
        IMatrix ElementwiseOperation(Func<object, object, object> operation, object value);

        IMatrix RowSwap(int row1, int row2);
        IMatrix ColumnSwap(int column1, int column2);

        IMatrix RowMultiply(int targetRow, object multiplier);
        IMatrix ColumnMultiply(int targetColumn, object multiplier);

        IMatrix RowSum(int targetRow, int operandRow, object multiplier);
        IMatrix ColumnSum(int targetColumn, int operandColumn, object multiplier);
    }

    public interface IMatrix<T> : IMatrix
    {
        Func<T, T, T> AddItems { get; }
        Func<T, T, T> SubtractItems { get; }
        Func<T, T, T> MultiplyItems { get; }
        Func<T, T, T> DivideItems { get; }
        Func<T, double, T> MultiplyByDouble { get; }

        new T this[int row, int column] { get; }

        new T[,] GetData();

        new IMatrix<T> Transpose();

        new IMatrix<T> Minors();
        T Minor(int row, int column);

        new IMatrix<T> Cofactors();
        T Cofactor(int row, int column);

        new T Determinant();

        new IMatrix<T> Adjoint();

        new T Trace();

        new IMatrix<T> Inverse();

        IMatrix<T> Add(IMatrix<T> matrix);
        IMatrix<T> Add(T value);

        IMatrix<T> Subtract(IMatrix<T> matrix);
        IMatrix<T> Subtract(T value);

        IMatrix<T> Multiply(IMatrix<T> matrix);
        IMatrix<T> Multiply(T value);

        IMatrix<T> Divide(IMatrix<T> matrix);
        IMatrix<T> Divide(T value);

        IMatrix<U> ElementwiseOperation<U, V>(Func<T, V, U> operation, IMatrix<V> matrix, Func<U, U, U> addItems, Func<U, U, U> subtractItems, Func<U, U, U> multiplyItems, Func<U, U, U> divideItems, Func<U, double, U> multiplyByDouble);
        IMatrix<U> ElementwiseOperation<U, V>(Func<T, V, U> operation, V value, Func<U, U, U> addItems, Func<U, U, U> subtractItems, Func<U, U, U> multiplyItems, Func<U, U, U> divideItems, Func<U, double, U> multiplyByDouble);
        IMatrix<T> ElementwiseOperation<V>(Func<T, V, T> operation, IMatrix<V> matrix);
        IMatrix<T> ElementwiseOperation<V>(Func<T, V, T> operation, V value);

        new IMatrix<T> RowSwap(int row1, int row2);
        new IMatrix<T> ColumnSwap(int column1, int column2);

        IMatrix<T> RowMultiply(int targetRow, T multiplier);
        IMatrix<T> ColumnMultiply(int targetColumn, T multiplier);

        IMatrix<T> RowSum(int targetRow, int operandRow, T multiplier);
        IMatrix<T> ColumnSum(int targetColumn, int operandColumn, T multiplier);
    }
}