using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems
{
    /// <summary>
    /// 
    /// </summary>
    public class Polar : ICoordinateSystem
    {
        /// <summary>
        /// 
        /// </summary>
        public Type[] Axis { get; set; }

        /// <summary>
        /// 
        /// </summary>
        public Polar()
        {
            //Axis = new Type[2] { Quantities.Base.Length<Polar>, Quantities.Base.Angle<Polar> }
        }
    }
}
