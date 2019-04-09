using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Symbolic
{
    /// <summary>
    /// Basis for symbolic objects
    /// </summary>
    public abstract class Symbol
    {
        /// <summary>
        /// The mathmatical symbol for the value
        /// </summary>
        public string symbol { get; protected set; }

        /// <summary>
        /// The value associated with the symbol
        /// </summary>
        public decimal Value { get; protected set; }

        /// <summary>
        /// Array of all valid operators as strings
        /// </summary>
        public static readonly string[] Operators = new string[] { "+", "-", "*", "/", "^", "sqrt(", ")", "sin(", "cos(", "tan(", "abs("};

        /// <summary>
        /// Gets a string containing the components that produce the value
        /// </summary>
        /// <param name="expantionDepth">The number of symbol layers to expand before just quoting symbols</param>
        /// <returns></returns>
        public abstract string GetComponentString(int expantionDepth = 1);

        /// <summary>
        /// Attempts to evaluate the expression to provide a value
        /// </summary>
        /// <returns></returns>
        public abstract decimal Evaluate();
    }
}
