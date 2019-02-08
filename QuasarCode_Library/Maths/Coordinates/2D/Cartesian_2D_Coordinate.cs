using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates.Systems;
using QuasarCode.Library.Maths.Coordinates.Systems._2D;

namespace QuasarCode.Library.Maths.Coordinates._2D
{
    public class Cartesian_2D_Coordinate : ICoordinate<Cartesian_2D>
    {
        public ICoordinateSystem<Cartesian_2D> System { get; }

        public decimal[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public Cartesian_2D_Coordinate(ICoordinateSystem<Cartesian_2D> coordinateSystem, decimal x, decimal y)
        {
            System = coordinateSystem;

            Ordinates = new decimal[] { x, y };
        }

        public Matrices.Vectors.IVector GetVector()
        {
            return new Matrices.Vectors.CartesianVector<Cartesian_2D>(Ordinates);
        }
    }
}
