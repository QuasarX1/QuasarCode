using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems
{
    public interface ICoordinateSystem
    {
        Type[] Axis { get; set; }
    }
}
