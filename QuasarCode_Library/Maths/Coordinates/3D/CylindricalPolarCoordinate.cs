using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates.Systems;
using QuasarCode.Library.Maths.Coordinates.Systems._3D;


namespace QuasarCode.Library.Maths.Coordinates._3D
{
    public class CylindricalPolarCoordinate : ICoordinate<CylindricalPolar>
    {
        public ICoordinateSystem<CylindricalPolar> System { get; }

        public decimal[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public CylindricalPolarCoordinate(ICoordinateSystem<CylindricalPolar> coordinateSystem, decimal r, decimal theta, decimal z)
        {
            System = coordinateSystem;

            Ordinates = new decimal[] { r, theta, z };
        }

        public Matrices.Vectors.IVector GetVector()
        {
            throw new NotImplementedException();
            //return new Matrices.Vectors.PolarVector<CylindricalPolar>(Ordinates);
        }
    }
}
