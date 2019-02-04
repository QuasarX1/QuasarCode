using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems._2D
{
    public class Cartesian_2D : ICoordinateSystem<Cartesian_2D>
    {
        public Dictionary<string, IGeneralUnit> Axes { get; }

        public int Dimentions { get { return 2; } }


        public Cartesian_2D(Units xUnit = Units.m, Units yUnit = Units.m)
        {
            Axes = new Dictionary<string, IGeneralUnit> { { "x", (Unit)xUnit }, { "y", (Unit)yUnit } };
        }

        public Cartesian_2D(IGeneralUnit xUnit, IGeneralUnit yUnit)
        {
            Axes = new Dictionary<string, IGeneralUnit> { { "x", xUnit }, { "y", yUnit } };
        }


        public event Func<ICoordinateSystem<Cartesian_2D>, ICoordinate<Cartesian_2D>[]> ReportPosition;

        public enum AxisNames
        {
            x,
            y
        }
    }
}
