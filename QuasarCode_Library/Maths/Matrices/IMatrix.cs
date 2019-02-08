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

        IMatrix Identity();

        IMatrix Transpose();

        IMatrix MinorsMatrix();

        IMatrix CofactorsMatrix();

        decimal Determinant();

        IMatrix AdjointMatrix();

        decimal Dot(IMatrix matrix);
    }
}
