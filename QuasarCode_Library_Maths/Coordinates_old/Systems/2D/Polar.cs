using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems._2D
{
    /// <summary>
    /// Two dimantional polar coordinate system
    /// </summary>
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

        public ICoordinate<Polar> GetCoordinate(params decimal[] ordinates)
        {
            if (ordinates.Length != this.Dimentions)
            {
                throw new ArgumentException("Coordinate creation failed - number of ordinates provided was inapropriate for the number of dimentions in the coordinate system.");
            }

            return new Coordinates._2D.PolarCoordinate(this, ordinates[0], ordinates[1]);
        }


        public event Func<ICoordinateSystem<Polar>, ICoordinate<Polar>[]> ReportPosition;

        public enum AxisNames
        {
            r,
            theta
        }
    }
}
