using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems._3D
{
    public class CylindricalPolar : ICoordinateSystem<CylindricalPolar>
    {
        public Dictionary<string, IGeneralUnit> Axes { get; }

        public int Dimentions { get { return 3; } }


        public CylindricalPolar(Units xUnit = Units.m, Units yUnit = Units.Radians, Units zUnit = Units.m)
        {
            Axes = new Dictionary<string, IGeneralUnit> { { "r", (Unit)xUnit }, { "theta", (Unit)yUnit }, { "z", (Unit)zUnit } };
        }

        public CylindricalPolar(IGeneralUnit xUnit, IGeneralUnit yUnit, IGeneralUnit zUnit)
        {
            Axes = new Dictionary<string, IGeneralUnit> { { "r", xUnit }, { "theta", yUnit }, { "z", zUnit } };
        }


        public event Func<ICoordinateSystem<CylindricalPolar>, ICoordinate<CylindricalPolar>[]> ReportPosition;

        public enum AxisNames
        {
            r,
            theta,
            z
        }
    }
}
