using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.old.Coordinates.Systems;
using QuasarCode.Library.Maths.old.Coordinates.Systems._1D;

namespace QuasarCode.Library.Maths.old.Coordinates._1D
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

        public Matrices.Vectors.IVector<Line> GetVector()
        {
            return new Matrices.Vectors.CartesianVector<Line>(Ordinates);
        }

        public void Move(Matrices.Vectors.IVector<Line> vector)
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
            return new LineCoordinate(this.System, this.Ordinates[0]);
        }

        public override string ToString()
        {
            return "(" + Ordinates[0].ToString() + ")";
        }
    }
}
