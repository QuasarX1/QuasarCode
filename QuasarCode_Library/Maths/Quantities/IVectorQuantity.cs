using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths._Quantities
{
    /// <summary>
    /// 
    /// </summary>
    /// <typeparam name="T">Coordinate system</typeparam>
    public interface IVectorQuantity<T>: IQuantity where T : Coordinates.Systems.ICoordinateSystem
    {
        /// <summary>
        /// 
        /// </summary>
        Matrices.Vectors.Vector<T> Direction { get; set; }//can be null!
    }
}
