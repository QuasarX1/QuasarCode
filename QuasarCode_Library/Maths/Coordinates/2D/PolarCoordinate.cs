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

        public Matrices.Vectors.IVector<Polar> GetVector()
        {
            throw new NotImplementedException();
            //return new Matrices.Vectors.PolarVector<Polar>(Ordinates);
        }

        public void Move(Matrices.Vectors.IVector<Polar> vector)
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
            return new PolarCoordinate(this.System, this.Ordinates[0], this.Ordinates[1]);
        }

        public override string ToString()
        {
            return "(" + Ordinates[0].ToString() + ", " + Ordinates[1].ToString() + ")";
        }
    }
}
