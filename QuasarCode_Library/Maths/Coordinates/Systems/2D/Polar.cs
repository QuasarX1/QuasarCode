using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems._2D
{
    public class Polar : IPolarBase<Polar>
    {
        public Dictionary<string, IGeneralUnit> Axes { get; }

        public int Dimentions { get { return 2; } }


        public Polar(Units xUnit = Units.m, Units yUnit = Units.Radians)
        {
            Axes = new Dictionary<string, IGeneralUnit> { { "r", (Unit)xUnit }, { "theta", (Unit)yUnit } };
        }

        public Polar(IGeneralUnit xUnit, IGeneralUnit yUnit)
        {
            Axes = new Dictionary<string, IGeneralUnit> { { "r", xUnit }, { "theta", yUnit } };
        }


        public event Func<ICoordinateSystem<Polar>, ICoordinate<Polar>[]> ReportPosition;

        public enum AxisNames
        {
            r,
            theta
        }
    }
}
