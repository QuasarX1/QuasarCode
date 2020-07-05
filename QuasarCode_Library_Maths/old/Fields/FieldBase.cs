using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.old.Coordinates;
using QuasarCode.Library.Maths.old.Coordinates.Systems;
using QuasarCode.Library.Maths.old.Matrices.Vectors;

namespace QuasarCode.Library.Maths.old.Fields
{
    public partial class FieldBase<S, T> : IField<S, T> where S : ICoordinateSystem<S>
    {
        public S System { get; }

        public Func<ICoordinate<S>, T> Function { get; }

        protected Dictionary<ICoordinate<S>, T> Casche = new Dictionary<ICoordinate<S>, T>();

        public FieldBase(S coordinateSystem, Func<ICoordinate<S>, T> fieldFunction)
        {
            System = coordinateSystem;

            Function = fieldFunction;
        }

        public T AtLoc(params decimal[] coordinate)
        {
            return AtLoc(System.GetCoordinate(coordinate));
        }

        public T AtLoc(ICoordinate<S> coordinate)
        {
            if (coordinate.Dimentions != System.Dimentions)
            {
                throw new ArgumentException("Value retrival failed - number of ordinates provided was inapropriate for the number of dimentions in the coordinate system.");
            }

            if (Casche.ContainsKey(coordinate))
            {
                return Casche[coordinate];
            }
            else
            {
                T result = CalculateAtLoc(coordinate);
                Casche.Add((ICoordinate<S>)coordinate.Clone(), result);
                return result;
            }
        }

        public T CalculateAtLoc(params decimal[] coordinate)
        {
            return CalculateAtLoc(System.GetCoordinate(coordinate));
        }

        public T CalculateAtLoc(ICoordinate<S> coordinate)
        {
            return Function(coordinate);
        }

        public void ClearCasche()
        {
            Casche.Clear();
        }
    }
}
