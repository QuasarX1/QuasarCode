using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    public class StandardFormValue : IStandardFormValue
    {
        public double StandardMagnitude { get; protected set; }

        public int StandardPower { get; protected set; }

        public IUnit Unit { get; protected set; }

        public double Magnitude { get { return StandardMagnitude * Math.Pow(10, StandardPower); } }

        public StandardFormValue(double magnitude, IUnit unit)
        {
            this.Unit = unit;
            this.StandardMagnitude = magnitude;
            this.StandardPower = 0;
            this.Normalise();
        }

        public StandardFormValue(IValue value)
        {
            this.Unit = value.Unit;
            this.StandardMagnitude = value.Magnitude;
            this.StandardPower = 0;
            this.Normalise();
        }

        public StandardFormValue(double standardMagnitude, int standardPower, IUnit unit)
        {
            this.Unit = unit;
            this.StandardMagnitude = standardMagnitude;
            this.StandardPower = standardPower;
            this.Normalise();
        }

        private void Normalise()
        {
            if (Math.Abs(this.StandardMagnitude) >= 10)
            {
                while (this.StandardMagnitude >= 10)
                {
                    this.StandardMagnitude /= 10;
                    this.StandardPower += 1;
                }
            }
            else if (Math.Abs(this.StandardMagnitude) < 1 && this.StandardMagnitude != 0)
            {
                while (this.StandardMagnitude < 1)
                {
                    this.StandardMagnitude *= 10;
                    this.StandardPower -= 1;
                }
            }
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

            return new StandardFormValue(magnitude, unit);
        }

        public IValue Mult(IValue v)
        {
            return new StandardFormValue(this.Magnitude * v.Magnitude, this.Unit.Mult(v.Unit));
        }

        public IValue Mult(double v)
        {
            return new StandardFormValue(this.Magnitude * v, this.Unit);
        }

        public IValue Div(IValue v)
        {
            return new StandardFormValue(this.Magnitude / v.Magnitude, this.Unit.Mult(v.Unit));
        }

        public IValue Div(double v)
        {
            return new StandardFormValue(this.Magnitude / v, this.Unit);
        }

        public IValue Pow(int p)
        {
            return new StandardFormValue(Math.Pow(this.Magnitude, p), this.Unit.Pow(p));
        }

        public IValue Round(int digits)
        {
            return new StandardFormValue(Math.Round(this.Magnitude, MidpointRounding.AwayFromZero), this.Unit);
        }

        public static StandardFormValue operator *(StandardFormValue a, IValue b)
        {
            return (StandardFormValue)a.Mult(b);
        }

        public static StandardFormValue operator /(StandardFormValue a, IValue b)
        {
            return (StandardFormValue)a.Div(b);
        }
    }
}
