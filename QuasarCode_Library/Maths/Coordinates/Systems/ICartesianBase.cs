using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems
{
    public interface ICartesianBase<T> : ICoordinateSystem<T> where T : ICoordinateSystem<T> { }
}
