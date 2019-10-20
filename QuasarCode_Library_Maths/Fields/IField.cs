using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates;
using QuasarCode.Library.Maths.Coordinates.Systems;

namespace QuasarCode.Library.Maths.Fields
{
    public interface IField<S, T> where S : ICoordinateSystem<S>
    {
        S System { get; }

        T AtLoc(params decimal[] coordinate);

        T AtLoc(ICoordinate<S> coordinate);

        T CalculateAtLoc(params decimal[] coordinate);

        T CalculateAtLoc(ICoordinate<S> coordinate);

        void ClearCasche();
    }
}
