using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.old.Coordinates.Systems
{
    /// <summary>
    /// Basis for all cartesian coordinate systems from 1D to ND
    /// </summary>
    /// <typeparam name="T">Type of cartesian system</typeparam>
    public interface ICartesianBase<T> : ICoordinateSystem<T> where T : ICoordinateSystem<T> { }
}
