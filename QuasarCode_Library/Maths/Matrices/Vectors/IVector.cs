using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Matrices.Vectors
{
    public interface IVector : IMatrix
    {
        decimal Magnitude { get; set; }

        decimal[] ComponentArray { get; }

        string ToString();

        string[] GetComponentStrings();

        decimal Dot(IVector vector);

        IVector Cross(IVector vector);

        decimal this[int row] { get; }
    }
}
