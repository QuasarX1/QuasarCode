using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates
{
    /// <summary>
    /// 
    /// </summary>
    public interface ICoordinate<T> where T : Systems.ICoordinateSystem<T>
    {
        Systems.ICoordinateSystem<T> System { get; }

        decimal[] Ordinates { get; }

        int Dimentions { get; }

        Matrices.Vectors.IVector GetVector();
    }
}
