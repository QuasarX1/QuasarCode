using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Units;
using QuasarCode.Library.Maths.Units.Common;

namespace QuasarCode.Library.Maths.Matrices.Vectors
{
    public class Vector<T> : Matrix<T>, IVector<T>
    {
        public int Length { get { return this.GetData().Length; } }

        public bool ColumnFormat { get { return this.GetData().GetLength(1) > 1; } }

        public T this[int index]
        {
            get { return ((Matrix<T>)this)[(this.ColumnFormat) ? 0 : index, (this.ColumnFormat) ? index : 0]; }
        }

        protected static T[,] FormatVectorData(T[] data, bool columnFormat)
        {
            T[,] formattedData = new T[(columnFormat) ? 1 : data.Length, (columnFormat) ? data.Length : 1];
            for (int i = 0; i < data.Length; i++)
            {
                formattedData[(columnFormat) ? 0 : i, (columnFormat) ? i : 0] = data[i];
            }

            return formattedData;
        }

        public static Vector<T> NewVector(T[] data, Func<T, T, T> addItems, Func<T, T, T> subtractItems, Func<T, T, T> multiplyItems, Func<T, T, T> divideItems, Func<T, double, T> multiplyByDouble, bool enableCasching = true)
        {
            return new Vector<T>(Vector<T>.FormatVectorData(data, ), addItems, subtractItems, multiplyItems, divideItems, multiplyByDouble, enableCasching);
        }

        protected Vector(T[,] data, Func<T, T, T> addItems, Func<T, T, T> subtractItems, Func<T, T, T> multiplyItems, Func<T, T, T> divideItems, Func<T, double, T> multiplyByDouble, bool enableCasching = true) : base(data, addItems, subtractItems, multiplyItems, divideItems, multiplyByDouble, enableCasching) { }

        public static Vector<T> NewVector(IVector<T> vector, bool enableCasching = true) { return new Vector<T>(vector, enableCasching); }

        public Vector(IVector<T> vector, bool enableCasching = true) : base(vector, enableCasching) { }

        protected static Vector<T> NewVector(T[] data, IVector<T> vector, bool enableCasching = true)
        {
            T[,] formattedData = new T[1, data.Length];
            for (int i = 0; i < data.Length; i++)
            {
                formattedData[0, i] = data[i];
            }

            return new Vector<T>(formattedData, vector, enableCasching);
        }

        protected Vector(T[,] data, IVector<T> vector, bool enableCasching = true) : base(data, vector, enableCasching) { }

        public T[] GetVectorData()
        {
            T[] result = new T[this.Length];
            for (int i = 0; i < this.Length; i++)
            {
                result[i] = this[i];
            }

            return result;
        }

        IVector<T> IVector<T>.Transpose()
        {
            return new Vector<T>(((Matrix<T>)this).Transpose().GetData(), this, this.CaschingEnabled);
        }

        public T ScalarProduct(IVector<T> vector)
        {
            throw new NotImplementedException();
        }

        public T VectorProduct(IVector<T> vector)
        {
            throw new NotImplementedException();
        }

        public IVector<T> Add(IVector<T> vector)
        {
            return new Vector<T>(((Matrix<T>)this).Add(vector).GetData(), this, this.CaschingEnabled);
        }

        public IVector<T> Subtract(IVector<T> vector)
        {
            return new Vector<T>(((Matrix<T>)this).Subtract(vector).GetData(), this, this.CaschingEnabled);
        }

        public IVector<U> ElementwiseOperation<U, V>(Func<T, V, U> operation, IVector<V> vector, Func<U, U, U> addItems, Func<U, U, U> subtractItems, Func<U, U, U> multiplyItems, Func<U, U, U> divideItems, Func<U, double, U> multiplyByDouble)
        {
            return new Vector<U>(((Matrix<T>)this).ElementwiseOperation(operation, vector, addItems, subtractItems, multiplyItems, divideItems, multiplyByDouble).GetData(), addItems, subtractItems, multiplyItems, divideItems, multiplyByDouble);
        }

        new public IVector<U> ElementwiseOperation<U, V>(Func<T, V, U> operation, V value, Func<U, U, U> addItems, Func<U, U, U> subtractItems, Func<U, U, U> multiplyItems, Func<U, U, U> divideItems, Func<U, double, U> multiplyByDouble)
        {
            return new Vector<U>(((Matrix<T>)this).ElementwiseOperation(operation, value, addItems, subtractItems, multiplyItems, divideItems, multiplyByDouble).GetData(), addItems, subtractItems, multiplyItems, divideItems, multiplyByDouble);
        }

        public IVector<T> ElementwiseOperation<V>(Func<T, V, T> operation, IVector<V> vector)
        {
            return new Vector<T>(((Matrix<T>)this).ElementwiseOperation(operation, vector).GetData(), this);
        }

        new public IVector<T> ElementwiseOperation<V>(Func<T, V, T> operation, V value)
        {
            return new Vector<T>(((Matrix<T>)this).ElementwiseOperation(operation, value).GetData(), this);
        }
    }
}