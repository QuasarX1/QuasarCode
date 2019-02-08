using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates.Systems;
using QuasarCode.Library.Maths.Coordinates.Systems._1D;

namespace QuasarCode.Library.Maths.Coordinates._1D
{
    public class LineCoordinate : ICoordinate<Line>
    {
        public ICoordinateSystem<Line> System { get; }

        public decimal[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public LineCoordinate(ICoordinateSystem<Line> coordinateSystem, decimal x)
        {
            System = coordinateSystem;

            Ordinates = new decimal[] { x };
        }

        public Matrices.Vectors.IVector GetVector()
        {
            return new Matrices.Vectors.CartesianVector<Line>(Ordinates);
        }
    }
}
