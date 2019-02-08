using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems
{
    public interface IPolarBase<T> : ICoordinateSystem<T> where T : ICoordinateSystem<T> { }
}
