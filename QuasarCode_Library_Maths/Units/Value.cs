using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    public class Value : IValue
    {
        public IUnit Unit { get; protected set; }

        public double Magnitude { get; protected set; }

        public Value(double magnitude, IUnit unit)
        {
            this.Unit = unit;
            this.Magnitude = magnitude;
        }

        public IValue As(IUnit unit)
        {
            if (unit != this.Unit)
            {
                throw new ArgumentException("The unit provided was not equivilant to the current unit and therfore the value could not be converted.");
            }

            double magnitude = this.Magnitude;

            foreach (FundamentalUnitPowerPair pair in this.Unit.GetFundamentalUnitPairs())
            {
                magnitude = pair.Unit.ConvertToSystemBase(magnitude, pair.Power);
            }

            foreach (FundamentalUnitPowerPair pair in unit.GetFundamentalUnitPairs())
            {
                magnitude = pair.Unit.ConvertFromSystemBase(magnitude, pair.Power);
            }

            return new Value(magnitude, unit);
        }

        public IValue Mult(IValue v)
        {
            return new Value(this.Magnitude * v.Magnitude, this.Unit.Mult(v.Unit));
        }

        public IValue Mult(double v)
        {
            return new Value(this.Magnitude * v, this.Unit);
        }

        public IValue Div(IValue v)
        {
            return new Value(this.Magnitude / v.Magnitude, this.Unit.Mult(v.Unit));
        }

        public IValue Div(double v)
        {
            return new Value(this.Magnitude / v, this.Unit);
        }

        public IValue Pow(int p)
        {
            return new Value(Math.Pow(this.Magnitude, p), this.Unit.Pow(p));
        }

        public IValue Round(int digits)
        {
            return new Value(Math.Round(this.Magnitude, MidpointRounding.AwayFromZero), this.Unit);
        }

        public IValue Add(IValue v)
        {
            if (this.Unit != v.Unit)
            {
                throw new ArgumentException("The values did not have the same units.");
            }

            return new Value(this.Magnitude + v.Magnitude, this.Unit);
        }

        public IValue Add(double v)
        {
            return new Value(this.Magnitude + v, this.Unit);
        }

        public IValue Sub(IValue v)
        {
            if (this.Unit != v.Unit)
            {
                throw new ArgumentException("The values did not have the same units.");
            }

            return new Value(this.Magnitude - v.Magnitude, this.Unit);
        }

        public IValue Sub(double v)
        {
            return new Value(this.Magnitude - v, this.Unit);
        }

        public static Value operator +(Value a, IValue b)
        {
            return (Value)a.Add(b);
        }

        public static Value operator -(Value a, IValue b)
        {
            return (Value)a.Sub(b);
        }

        public static Value operator *(Value a, IValue b)
        {
            return (Value)a.Mult(b);
        }

        public static Value operator /(Value a, IValue b)
        {
            return (Value)a.Div(b);
        }
    }
}
