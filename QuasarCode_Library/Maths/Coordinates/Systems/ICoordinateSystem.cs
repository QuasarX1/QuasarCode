using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems
{
    public interface ICoordinateSystem
    {
        Dictionary<string, IGeneralUnit> Axes { get; }

        int Dimentions { get; }
    }

    public interface ICoordinateSystem<T> : ICoordinateSystem where T : ICoordinateSystem<T>
    {
        event Func<ICoordinateSystem<T>, ICoordinate<T>[]> ReportPosition;
    }
}
