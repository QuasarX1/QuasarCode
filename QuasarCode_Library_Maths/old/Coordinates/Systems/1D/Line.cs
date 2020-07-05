using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.old.Coordinates.Systems._1D
{
    /// <summary>
    /// One dimentional cartesian coordinate system
    /// </summary>
    public class Line : ICartesianBase<Line>
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

        public ICoordinate<Line> GetCoordinate(params decimal[] ordinates)
        {
            if (ordinates.Length != this.Dimentions)
            {
                throw new ArgumentException("Coordinate creation failed - number of ordinates provided was inapropriate for the number of dimentions in the coordinate system.");
            }

            return new Coordinates._1D.LineCoordinate(this, ordinates[0]);
        }

        public Matrices.Vectors.CartesianVector<Line> i
        {
            get
            {
                return new Matrices.Vectors.CartesianVector<Line>(1);
            }
        }


        public event Func<ICoordinateSystem<Line>, ICoordinate<Line>[]> ReportPosition;

        public enum AxisNames
        {
            x
        }
    }
}
