using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems._3D
{
    public class SphericalPolar : IPolarBase<SphericalPolar>
    {
        public Dictionary<string, IGeneralUnit> Axes { get; }

        public int Dimentions { get { return 3; } }


        public SphericalPolar(Units xUnit = Units.m, Units yUnit = Units.Radians, Units zUnit = Units.Radians)
        {
            Axes = new Dictionary<string, IGeneralUnit> { { "r", (Unit)xUnit }, { "theta", (Unit)yUnit }, { "phi", (Unit)zUnit } };
        }

        public SphericalPolar(IGeneralUnit xUnit, IGeneralUnit yUnit, IGeneralUnit zUnit)
        {
            Axes = new Dictionary<string, IGeneralUnit> { { "r", xUnit }, { "theta", yUnit }, { "phi", zUnit } };
        }


        public event Func<ICoordinateSystem<SphericalPolar>, ICoordinate<SphericalPolar>[]> ReportPosition;

        public enum AxisNames
        {
            r,
            theta,
            phi
        }
    }
}
