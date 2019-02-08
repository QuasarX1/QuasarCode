using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates.Systems;
using QuasarCode.Library.Maths.Coordinates.Systems._2D;

namespace QuasarCode.Library.Maths.Coordinates._2D
{
    public class PolarCoordinate : ICoordinate<Polar>
    {
        public ICoordinateSystem<Polar> System { get; }

        public decimal[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public PolarCoordinate(ICoordinateSystem<Polar> coordinateSystem, decimal r, decimal theta)
        {
            System = coordinateSystem;

            Ordinates = new decimal[] { r, theta };
        }

        public Matrices.Vectors.IVector GetVector()
        {
            throw new NotImplementedException();
            //return new Matrices.Vectors.PolarVector<Polar>(Ordinates);
        }
    }
}
