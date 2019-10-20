using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems._3D
{
    /// <summary>
    /// Three dimantional cartesian coordinate system
    /// </summary>
    public class Cartesian_3D : ICartesianBase<Cartesian_3D>
    {
        public Dictionary<string, IGeneralUnit> Axes { get; }

        public int Dimentions { get { return 3; } }


        public Cartesian_3D(Units xUnit = Units.m, Units yUnit = Units.m, Units zUnit = Units.m)
        {
            Axes = new Dictionary<string, IGeneralUnit> { { "x", (Unit)xUnit }, { "y", (Unit)yUnit }, { "z", (Unit)zUnit } };
        }

        public Cartesian_3D(IGeneralUnit xUnit, IGeneralUnit yUnit, IGeneralUnit zUnit)
        {
            Axes = new Dictionary<string, IGeneralUnit> { { "x", xUnit }, { "y", yUnit }, { "z", zUnit } };
        }

        public ICoordinate<Cartesian_3D> GetCoordinate(params decimal[] ordinates)
        {
            if (ordinates.Length != this.Dimentions)
            {
                throw new ArgumentException("Coordinate creation failed - number of ordinates provided was inapropriate for the number of dimentions in the coordinate system.");
            }

            return new Coordinates._3D.Cartesian_3D_Coordinate(this, ordinates[0], ordinates[1], ordinates[2]);
        }

        public Matrices.Vectors.CartesianVector<Cartesian_3D> i
        {
            get
            {
                return new Matrices.Vectors.CartesianVector<Cartesian_3D>(1, 0, 0);
            }
        }

        public Matrices.Vectors.CartesianVector<Cartesian_3D> j
        {
            get
            {
                return new Matrices.Vectors.CartesianVector<Cartesian_3D>(0, 1, 0);
            }
        }

        public Matrices.Vectors.CartesianVector<Cartesian_3D> k
        {
            get
            {
                return new Matrices.Vectors.CartesianVector<Cartesian_3D>(0, 0, 1);
            }
        }


        public event Func<ICoordinateSystem<Cartesian_3D>, ICoordinate<Cartesian_3D>[]> ReportPosition;

        public enum AxisNames
        {
            x,
            y,
            z
        }
    }
}
