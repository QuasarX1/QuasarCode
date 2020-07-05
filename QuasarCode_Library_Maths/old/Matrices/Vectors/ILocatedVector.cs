using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.old.Matrices.Vectors
{
    public interface ILocatedVector<T> : IVector<T> where T : Coordinates.Systems.ICoordinateSystem<T>
    {
        Coordinates.ICoordinate<T> Location { get; }
    }
}
