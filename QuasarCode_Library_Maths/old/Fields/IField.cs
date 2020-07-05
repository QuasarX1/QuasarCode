using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.old.Coordinates;
using QuasarCode.Library.Maths.old.Coordinates.Systems;

namespace QuasarCode.Library.Maths.old.Fields
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
