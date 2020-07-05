using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Units;
using QuasarCode.Library.Maths.Units.Common;

namespace QuasarCode.Library.Maths.Matrices.Vectors
{
    public interface IVector<T> : IMatrix<T>
    {
        int Length { get; }
        bool ColumnFormat { get; }
        T this[int index] { get; }

        T[] GetVectorData();

        new IVector<T> Transpose();

        T ScalarProduct(IVector<T> vector);

        T VectorProduct(IVector<T> vector);

        IVector<T> Add(IVector<T> vector);

        IVector<T> Subtract(IVector<T> vector);

        IVector<U> ElementwiseOperation<U, V>(Func<T, V, U> operation, IVector<V> vector, Func<U, U, U> addItems, Func<U, U, U> subtractItems, Func<U, U, U> multiplyItems, Func<U, U, U> divideItems, Func<U, double, U> multiplyByDouble);
        new IVector<U> ElementwiseOperation<U, V>(Func<T, V, U> operation, V value, Func<U, U, U> addItems, Func<U, U, U> subtractItems, Func<U, U, U> multiplyItems, Func<U, U, U> divideItems, Func<U, double, U> multiplyByDouble);
        IVector<T> ElementwiseOperation<V>(Func<T, V, T> operation, IVector<V> vector);
        new IVector<T> ElementwiseOperation<V>(Func<T, V, T> operation, V value);
    }
}