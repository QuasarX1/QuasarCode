using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.old.Matrices.Vectors
{
    public interface IVector : IMatrix
    {
        decimal Magnitude { get; set; }

        IVector Direction { get; set; }

        decimal[] ComponentArray { get; }

        string ToString();

        string[] GetComponentStrings();

        decimal this[int row] { get; }
    }

    public interface IVector<T> : IVector where T : QuasarCode.Library.Maths.Coordinates.Systems.ICoordinateSystem<T>
    {
        decimal Dot(IVector<T> vector);

        IVector<T> Cross(IVector<T> vector);

        IVector<T> Add(IVector<T> vector);

        IVector<T> Subtract(IVector<T> vector);

        IVector<T> Multyply(IVector<T> vector);

        IVector<T> Divide(IVector<T> vector);

        IVector<T> AsUnitVector();
    }
}
