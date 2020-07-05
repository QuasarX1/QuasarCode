using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.old.Coordinates;
using QuasarCode.Library.Maths.old.Coordinates.Systems;
using QuasarCode.Library.Maths.old.Matrices.Vectors;

namespace QuasarCode.Library.Maths.old.Fields
{
    public class ScalarField<S> : FieldBase<S, decimal>, IScalarField<S, decimal> where S : ICoordinateSystem<S>
    {
        public ScalarField(S coordinateSystem, Func<ICoordinate<S>, decimal> fieldFunction) : base(coordinateSystem, fieldFunction) { }

        IScalarField<S, decimal> IScalarField<S, decimal>.Grad()
        {
            throw new NotImplementedException();
        }

        public ScalarField<S> Grad()
        {
            throw new NotImplementedException();
        }
    }
}
