using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.old.Coordinates.Systems._3D
{
    /// <summary>
    /// Three dimantional polar coordinate system in a spherical shape
    /// </summary>
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

        public ICoordinate<SphericalPolar> GetCoordinate(params decimal[] ordinates)
        {
            if (ordinates.Length != this.Dimentions)
            {
                throw new ArgumentException("Coordinate creation failed - number of ordinates provided was inapropriate for the number of dimentions in the coordinate system.");
            }

            return new Coordinates._3D.SphericalPolarCoordinate(this, ordinates[0], ordinates[1], ordinates[2]);
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
