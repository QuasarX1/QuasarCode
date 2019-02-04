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

        double[] Ordinates { get; }

        int Dimentions { get; }

        Vector<T> GetVector();
    }
}
