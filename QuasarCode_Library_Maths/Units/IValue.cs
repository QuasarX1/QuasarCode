using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    /// <summary>
    /// A value associated with a unit
    /// </summary>
    public interface IValue
    {
        /// <summary>
        /// The unit
        /// </summary>
        IUnit Unit { get; }

        /// <summary>
        /// The size of the value
        /// </summary>
        double Magnitude { get; }

        /// <summary>
        /// Converts the value to one with an equivilant unit
        /// </summary>
        /// <param name="unit">The new value's units</param>
        /// <returns>The corisponding IValue object</returns>
        IValue As(IUnit unit);

        /// <summary>
        /// Raises a value to a power
        /// </summary>
        /// <param name="p">The power</param>
        /// <returns>A new value</returns>
        IValue Pow(int p);

        /// <summary>
        /// Adds two values
        /// </summary>
        /// <param name="v">The value to add</param>
        /// <returns>IUnit</returns>
        IValue Add(IValue v);

        /// <summary>
        /// Adds a value and a double
        /// </summary>
        /// <param name="v">The double to add</param>
        /// <returns>IUnit</returns>
        IValue Add(double v);

        /// <summary>
        /// Subtracts one value from annother
        /// </summary>
        /// <param name="v">The value to subtract</param>
        /// <returns>IUnit</returns>
        IValue Sub(IValue v);

        /// <summary>
        ///Subtracts a double from a value
        /// </summary>
        /// <param name="v">The double to subtract</param>
        /// <returns>IUnit</returns>
        IValue Sub(double v);

        /// <summary>
        /// Multiplies a value by annother
        /// </summary>
        /// <param name="v">The value to multyply by</param>
        /// <returns>IUnit</returns>
        IValue Mult(IValue v);

        /// <summary>
        /// Multiplies a value by a double
        /// </summary>
        /// <param name="v">The double to multyply by</param>
        /// <returns>IUnit</returns>
        IValue Mult(double v);

        /// <summary>
        /// Divides a value by annother
        /// </summary>
        /// <param name="v">The value to divide this by</param>
        /// <returns>IUnit</returns>
        IValue Div(IValue v);

        /// <summary>
        /// Divides a value by a double
        /// </summary>
        /// <param name="v">The double to divide this by</param>
        /// <returns>IUnit</returns>
        IValue Div(double v);

        /// <summary>
        /// Rounds the value to the provided number of decimal places provided
        /// </summary>
        /// <param name="digits">The number of decimal places to round to.</param>
        /// <returns>A new IValue instance with the rounded value</returns>
        IValue Round(int digits);
    }
}