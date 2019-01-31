﻿using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths
{
    /// <summary>
    /// A value in standard form associated with a unit
    /// </summary>
    public interface IStandardValue : IValue
    {
        /// <summary>
        /// The standard form power
        /// </summary>
        int StandardPower { get;  }

        /// <summary>
        /// Provides a string representation of the value with its unit
        /// </summary>
        /// <returns>The value as a string</returns>
        string ToString();
    }
}
