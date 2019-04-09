using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates.Systems;

namespace QuasarCode.Library.Maths.Fields
{
    public interface IScalarField<S, T> : IField<S, T> where S : ICoordinateSystem<S>
    {
        IScalarField<S, decimal> Grad();
    }
}
