using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems
{
    /// <summary>
    /// Basis for all polar coordinate systems in 2D and 3D
    /// </summary>
    /// <typeparam name="T">Type of polar system</typeparam>
    public interface IPolarBase<T> : ICoordinateSystem<T> where T : ICoordinateSystem<T> { }
}
