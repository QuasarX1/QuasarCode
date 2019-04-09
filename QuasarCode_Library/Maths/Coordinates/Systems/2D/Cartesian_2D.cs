using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems._2D
{
    /// <summary>
    /// Two dimantional cartesian coordinate system
    /// </summary>
    public class Cartesian_2D : ICartesianBase<Cartesian_2D>
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

        public ICoordinate<Cartesian_2D> GetCoordinate(params decimal[] ordinates)
        {
            if (ordinates.Length != this.Dimentions)
            {
                throw new ArgumentException("Coordinate creation failed - number of ordinates provided was inapropriate for the number of dimentions in the coordinate system.");
            }

            return new Coordinates._2D.Cartesian_2D_Coordinate(this, ordinates[0], ordinates[1]);
        }

        public Matrices.Vectors.CartesianVector<Cartesian_2D> i
        {
            get
            {
                return new Matrices.Vectors.CartesianVector<Cartesian_2D>(1, 0);
            }
        }

        public Matrices.Vectors.CartesianVector<Cartesian_2D> j
        {
            get
            {
                return new Matrices.Vectors.CartesianVector<Cartesian_2D>(0, 1);
            }
        }


        public event Func<ICoordinateSystem<Cartesian_2D>, ICoordinate<Cartesian_2D>[]> ReportPosition;

        public enum AxisNames
        {
            x,
            y
        }
    }
}
