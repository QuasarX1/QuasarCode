using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.old.Coordinates
{
    /// <summary>
    /// 
    /// </summary>
    public interface ICoordinate<T> : ICloneable where T : Systems.ICoordinateSystem<T>
    {
        Systems.ICoordinateSystem<T> System { get; }

        decimal[] Ordinates { get; }

        int Dimentions { get; }

        Matrices.Vectors.IVector<T> GetVector();

        void Move(Matrices.Vectors.IVector<T> vector);

        string ToString();
    }
}
