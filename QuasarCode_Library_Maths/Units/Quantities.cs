﻿using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    /// <summary>
    /// Physical quantitys that have units
    /// </summary>
    public enum Quantities
    {
        /// <summary>No assigned quantity</summary>
        None,

        /// <summary>Mesurement of rotation</summary>
        Angle,

        /// <summary>Mesurement of space</summary>
        Length,

        /// <summary>Mesurement of matter</summary>
        Mass,

        /// <summary>Mesurement of change</summary>
        Time,

        /// <summary>Mesurement of electricity</summary>
        ElectricCurrent,

        /// <summary>Mesurement of thermal energy</summary>
        Temperature,

        /// <summary>Mesurement of quantity</summary>
        Quantity,

        /// <summary>Mesurement of change</summary>
        LuminousIntensity
    }
}