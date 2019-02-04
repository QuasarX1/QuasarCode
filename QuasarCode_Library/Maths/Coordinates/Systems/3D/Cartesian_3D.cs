using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems._3D
{
    public class Cartesian_3D : ICoordinateSystem<Cartesian_3D>
    {
        public Dictionary<string, IGeneralUnit> Axes { get; }

        public int Dimentions { get { return 3; } }


        public Cartesian_3D(Units xUnit = Units.m, Units yUnit = Units.m, Units zUnit = Units.m)
        {
            Axes = new Dictionary<string, IGeneralUnit> { { "x", (Unit)xUnit }, { "y", (Unit)yUnit }, { "z", (Unit)zUnit } };
        }

        public Cartesian_3D(IGeneralUnit xUnit, IGeneralUnit yUnit, IGeneralUnit zUnit)
        {
            Axes = new Dictionary<string, IGeneralUnit> { { "x", xUnit }, { "y", yUnit }, { "z", zUnit } };
        }


        public event Func<ICoordinateSystem<Cartesian_3D>, ICoordinate<Cartesian_3D>[]> ReportPosition;

        public enum AxisNames
        {
            x,
            y,
            z
        }
    }
}
