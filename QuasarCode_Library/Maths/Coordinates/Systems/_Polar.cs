using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems
{
    /// <summary>
    /// 
    /// </summary>
    public class _Polar : ICoordinateSystem
    {
        /// <summary>
        /// 
        /// </summary>
        public Type[] Axis { get; set; }

        /// <summary>
        /// 
        /// </summary>
        public _Polar()
        {
            //Axis = new Type[2] { Quantities.Base.Length<Polar>, Quantities.Base.Angle<Polar> }
        }
    }
}
