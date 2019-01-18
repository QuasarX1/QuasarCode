using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems
{
    public class Polar : ICoordinateSystem
    {
        public Type[] Axis { get; set; }

        public Polar()
        {
            Axis = new Type[2] { Quantities.Base.Length<Polar>, Quantities.Base.Angle<Polar> }
        }
    }
}
