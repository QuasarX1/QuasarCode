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
    }

    public interface IMatrix<T> : IMatrix
    {
        
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

        IMatrix<U> ElementwiseOperation<U, V>(Func<T, V, U> operation, IMatrix<V> matrix);
        IMatrix<U> ElementwiseOperation<U, V>(Func<T, V, U> operation, V value);
    }
}