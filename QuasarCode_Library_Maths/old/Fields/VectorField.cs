using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.old.Coordinates;
using QuasarCode.Library.Maths.old.Coordinates.Systems;
using QuasarCode.Library.Maths.old.Matrices.Vectors;

namespace QuasarCode.Library.Maths.old.Fields
{
    public class VectorField<S, T> : FieldBase<S, T>, IVectorField<S, T> where S : ICoordinateSystem<S> where T : ILocatedVector<S>
    {
        public VectorField(S coordinateSystem, Func<ICoordinate<S>, T> fieldFunction) : base(coordinateSystem, fieldFunction) { }

        IVectorField<S, T> IVectorField<S, T>.Curl()
        {
            throw new NotImplementedException();
        }

        public VectorField<S, T> Curl()
        {
            throw new NotImplementedException();
        }

        IScalarField<S, decimal> IVectorField<S, T>.Divergence()
        {
            throw new NotImplementedException();
        }

        public ScalarField<S> Divergence()
        {
            throw new NotImplementedException();
        }
    }
}
