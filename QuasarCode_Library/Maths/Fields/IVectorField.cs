using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates.Systems;
using QuasarCode.Library.Maths.Matrices.Vectors;

namespace QuasarCode.Library.Maths.Fields
{
    public interface IVectorField<S, T> : IField<S, T> where S : ICoordinateSystem<S> where T : ILocatedVector<S>
    {
        IScalarField<S, decimal> Grad();

        IVectorField<S, T> Curl();
    }
}
