﻿using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

namespace QuasarCode.Library.Maths.Coordinates.Systems
{
    /// <summary>
    /// 
    /// </summary>
    public class Cartesian: ICoordinateSystem
    {
        public Type[] Axis { get; set; }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="dimentions"></param>
        public Cartesian(int dimentions)
        {
            List<Type> axis = new List<Type>();

            for (int i = 0; i < dimentions; i++)
            {
                axis.Add(typeof(Quantities.Base.Length<Cartesian>));
            }
        }
    }
}
