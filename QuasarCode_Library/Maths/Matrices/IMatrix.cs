using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Matrices
{
    public interface IMatrix
    {
        int Rows { get; }

        int Columns { get; }

        int[] Shape { get; }

        decimal this[int row, int col] { get; }

        decimal[,] GetData();

        IMatrix Identity();

        IMatrix Transpose();

        IMatrix MinorsMatrix();

        IMatrix CofactorsMatrix();

        decimal Determinant();

        IMatrix AdjointMatrix();

        decimal Dot(IMatrix matrix);

        void Add(IMatrix matrix);
        void Add(decimal value);

        void Subtract(IMatrix matrix);
        void Subtract(decimal value);

        void Multiply(IMatrix matrix);
        void Multiply(decimal value);

        void Divide(IMatrix matrix);
        void Divide(decimal value);
    }
}
