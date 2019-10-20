using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Symbolic
{
    /// <summary>
    /// Object representing a symbol with a constant value
    /// </summary>
    public sealed class Constant : Symbol
    {
        /// <summary>
        /// The constant pi
        /// </summary>
        public static readonly Constant PI = new Constant("\u03C0", (decimal)Math.PI);

        /// <summary>
        /// Euler's number "e"
        /// </summary>
        public static readonly Constant E = new Constant("e", (decimal)Math.E);

        /// <summary>
        /// The golden ratio
        /// </summary>
        public static readonly Constant PHI = new Constant("\u03d5", (1 + (decimal)Math.Sqrt(5)) / 2);

        /// <summary>
        /// Creates a new constant with no symbol from a number
        /// </summary>
        /// <param name="initialValue">The constant's value</param>
        public Constant(decimal initialValue)
        {
            this.symbol = null;
            this.Value = initialValue;
        }

        /// <summary>
        /// Creates a new constant with a symbol and number
        /// </summary>
        /// <param name="symbol">The algebraic letter or symbol to associate with the value</param>
        /// <param name="initialValue">The constant's value</param>
        public Constant(string symbol, decimal initialValue)
        {
            this.symbol = symbol;
            this.Value = initialValue;
        }

        /// <summary>
        /// Gets a string containing the constant's symbol or its value if it has no symbol
        /// </summary>
        /// <param name="expantionDepth">The number of symbol layers to expand before just quoting symbols</param>
        /// <returns></returns>
        public override string GetComponentString(int expantionDepth = 1)
        {
            if (this.symbol != null)
            {
                return this.symbol;
            }
            else
            {
                return Value.ToString();
            }
        }

        /// <summary>
        /// Provides the constant's value
        /// </summary>
        /// <returns></returns>
        public override decimal Evaluate()
        {
            return Value;
        }
    }
}
