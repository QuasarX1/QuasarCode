using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths
{
    /// <summary>
    /// A value associated with a unit
    /// </summary>
    public class Value : IValue
    {
        /// <summary>
        /// The unit
        /// </summary>
        public IGeneralUnit Unit { get; protected set; }

        /// <summary>
        /// The size of the value
        /// </summary>
        public double Magnitude { get; protected set; }

        /// <summary>
        /// Creates a new Value object
        /// </summary>
        /// <param name="size">The size of the value</param>
        /// <param name="unit">The unit</param>
        public Value(double size, IGeneralUnit unit)
        {
            Unit = unit;

            Magnitude = size;
        }

        /// <summary>
        /// Creates a new Value object
        /// </summary>
        /// <param name="size">The size of the value</param>
        /// <param name="unit">The unit</param>
        /// <param name="power">The unit's power</param>
        public Value(double size, Units unit, int power = 1)
        {
            Unit = new Unit(unit, power);

            Magnitude = size;
        }

        /// <summary>
        /// Returns the value's actual magnitude. This should be overrided in child classes to provide the magnitude as a single value for arithmatic operations
        /// </summary>
        /// <returns>The magnitude of the value</returns>
        public virtual double GetMagnitude()
        {
            return Magnitude;
        }

        /// <summary>
        /// Provides a string representation of the value with its unit
        /// </summary>
        /// <returns>The value as a string</returns>
        public override string ToString()
        {
            return Magnitude.ToString() + ((Unit.ToString() != "") ? " " + Unit.ToString() : "");
        }

        /// <summary>
        /// Converts to a StandardValue object with standard form
        /// </summary>
        /// <returns>A new StandardValue object</returns>
        public StandardValue ToStandardValue()
        {
            return new StandardValue(GetMagnitude(), Unit);
        }

        /// <summary>
        /// Adds two Value objects together provided their units are equivilant
        /// </summary>
        /// <param name="a">object 1</param>
        /// <param name="b">object 2</param>
        /// <returns>A new Value object using the unit specified by a</returns>
        public static Value operator +(Value a, Value b)
        {
            if (a.Unit != b.Unit)
            {
                throw new ArithmeticException("Addition of Value objects failed - the units were not equivilant.");
            }

            return new Value(a.GetMagnitude() + b.GetMagnitude(), a.Unit);
        }

        /// <summary>
        /// Subtracts one Value object from annother provided their units are equivilant
        /// </summary>
        /// <param name="a">object 1</param>
        /// <param name="b">object 2</param>
        /// <returns>A new Value object using the unit specified by a</returns>
        public static Value operator -(Value a, Value b)
        {
            if (a.Unit != b.Unit)
            {
                throw new ArithmeticException("Addition of Value objects failed - the units were not equivilant.");
            }

            return new Value(a.GetMagnitude() - b.GetMagnitude(), a.Unit);
        }

        /// <summary>
        /// Multiplies two Value objects
        /// </summary>
        /// <param name="a">object 1</param>
        /// <param name="b">object 2</param>
        /// <returns>A new value object with a new unit</returns>
        public static Value operator *(Value a, Value b)
        {
            return new Value(a.GetMagnitude() * b.GetMagnitude(), new CompoundUnit(a.Unit, b.Unit));
        }

        /// <summary>
        /// Divides one Value object by another
        /// </summary>
        /// <param name="a">object 1</param>
        /// <param name="b">object 2</param>
        /// <returns>A new value object with a new unit</returns>
        public static Value operator /(Value a, Value b)
        {
            UnitPowerPair[] bUnits = b.Unit.GetUnitPairs();
            List<UnitPowerPair> newUnits = new List<UnitPowerPair>();

            // Create a new collection with inverse powers
            foreach (UnitPowerPair pair in bUnits)
            {
                newUnits.Add(new UnitPowerPair {Unit = pair.Unit, Power = 0 - pair.Power });
            }

            return new Value(a.GetMagnitude() / b.GetMagnitude(), new CompoundUnit(a.Unit, new CompoundUnit(newUnits.ToArray())));
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="o"></param>
        /// <returns></returns>
        public override bool Equals(object o)
        {
            try
            {
                return GetMagnitude() == ((IValue)o).GetMagnitude() && Unit == ((IValue)o).Unit;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        public override int GetHashCode()
        {
            return base.GetHashCode();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static bool operator ==(Value a, Value b)
        {
            return a.Equals(b);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static bool operator !=(Value a, Value b)
        {
            return !a.Equals(b);
        }
    }
}
