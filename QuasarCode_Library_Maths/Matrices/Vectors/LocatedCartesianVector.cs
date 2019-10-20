using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Matrices.Vectors
{
    public class LocatedCartesianVector<T> : CartesianVector<T>, ILocatedVector<T> where T : Coordinates.Systems.ICartesianBase<T>
    {
        public Coordinates.ICoordinate<T> Location { get; }

        public LocatedCartesianVector(Coordinates.ICoordinate<T> location, CartesianVector<T> vector) : base(vector)
        {
            Location = location;
        }

        public LocatedCartesianVector(Coordinates.ICoordinate<T> location, params decimal[] components) : base(components)
        {
            Location = location;
        }

        public LocatedCartesianVector(Coordinates.ICoordinate<T> location, Coordinates.ICoordinate<T> point1, Coordinates.ICoordinate<T> point2) : base(point1, point2)
        {
            Location = location;
        }
    }
}
