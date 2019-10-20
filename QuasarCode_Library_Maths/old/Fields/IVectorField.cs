using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.old.Coordinates.Systems;
using QuasarCode.Library.Maths.old.Matrices.Vectors;

namespace QuasarCode.Library.Maths.old.Fields
{
    public interface IVectorField<S, T> : IField<S, T> where S : ICoordinateSystem<S> where T : ILocatedVector<S>
    {
        IScalarField<S, decimal> Divergence();

        IVectorField<S, T> Curl();
    }
}
