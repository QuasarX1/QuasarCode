using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems._1D
{
    public class Line : ICoordinateSystem<Line>
    {
        public Dictionary<string, IGeneralUnit> Axes { get; }

        public int Dimentions { get { return 1; } }


        public Line(Units xUnit = Units.m)
        {
            Axes = new Dictionary<string, IGeneralUnit> { { "x", (Unit)xUnit } };
        }

        public Line(IGeneralUnit xUnit)
        {
            Axes = new Dictionary<string, IGeneralUnit> { { "x", xUnit } };
        }


        public event Func<ICoordinateSystem<Line>, ICoordinate<Line>[]> ReportPosition;

        public enum AxisNames
        {
            x
        }
    }
}
