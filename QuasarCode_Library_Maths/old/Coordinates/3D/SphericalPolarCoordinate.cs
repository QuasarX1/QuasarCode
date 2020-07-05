using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.old.Coordinates.Systems;
using QuasarCode.Library.Maths.old.Coordinates.Systems._3D;


namespace QuasarCode.Library.Maths.old.Coordinates._3D
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

        public Matrices.Vectors.IVector<SphericalPolar> GetVector()
        {
            throw new NotImplementedException();
            //return new Matrices.Vectors.PolarVector<SphericalPolar>(Ordinates);
        }

        public void Move(Matrices.Vectors.IVector<SphericalPolar> vector)
        {
            if (vector.Rows != this.Dimentions)
            {
                throw new ArgumentException("The vector provided has the wrong number of dimentions.");
            }

            decimal[] result = GetVector().Add(vector).ComponentArray;

            for (int i = 0; i < Dimentions; i++)
            {
                Ordinates[i] = result[i];
            }
        }

        new public object Clone()
        {
            return new SphericalPolarCoordinate(this.System, this.Ordinates[0], this.Ordinates[1], this.Ordinates[2]);
        }

        public override string ToString()
        {
            return "(" + Ordinates[0].ToString() + ", " + Ordinates[1].ToString() + ", " + Ordinates[2].ToString() + ")";
        }
    }
}
