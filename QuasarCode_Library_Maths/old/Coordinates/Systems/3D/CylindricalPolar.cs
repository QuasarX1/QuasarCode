using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.old.Coordinates.Systems._3D
{
    /// <summary>
    /// Three dimantional polar coordinate system in a cylinder shape
    /// </summary>
    public class CylindricalPolar : IPolarBase<CylindricalPolar>
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

        public ICoordinate<CylindricalPolar> GetCoordinate(params decimal[] ordinates)
        {
            if (ordinates.Length != this.Dimentions)
            {
                throw new ArgumentException("Coordinate creation failed - number of ordinates provided was inapropriate for the number of dimentions in the coordinate system.");
            }

            return new Coordinates._3D.CylindricalPolarCoordinate(this, ordinates[0], ordinates[1], ordinates[2]);
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
