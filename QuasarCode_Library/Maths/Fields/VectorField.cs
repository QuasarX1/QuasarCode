using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates;
using QuasarCode.Library.Maths.Coordinates.Systems;
using QuasarCode.Library.Maths.Matrices.Vectors;

namespace QuasarCode.Library.Maths.Fields
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

        IScalarField<S, decimal> IVectorField<S, T>.Grad()
        {
            throw new NotImplementedException();
        }

        public ScalarField<S> Grad()
        {
            throw new NotImplementedException();
        }
    }
}
