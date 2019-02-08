using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates.Systems;
using QuasarCode.Library.Maths.Coordinates.Systems._3D;


namespace QuasarCode.Library.Maths.Coordinates._3D
{
    public class SphericalPolarCoordinate : ICoordinate<SphericalPolar>
    {
        public ICoordinateSystem<SphericalPolar> System { get; }

        public decimal[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public SphericalPolarCoordinate(ICoordinateSystem<SphericalPolar> coordinateSystem, decimal r, decimal theta, decimal phi)
        {
            System = coordinateSystem;

            Ordinates = new decimal[] { r, theta, phi };
        }

        public Matrices.Vectors.IVector GetVector()
        {
            throw new NotImplementedException();
            //return new Matrices.Vectors.PolarVector<SphericalPolar>(Ordinates);
        }
    }
}
