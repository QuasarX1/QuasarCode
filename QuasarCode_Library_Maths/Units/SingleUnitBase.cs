using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    public abstract class SingleUnitBase : UnitBase, ISingleUnit
    {
        public Quantities Quantity { get; protected set; }
        public Systems System { get; protected set; }
        public string Text { get; protected set; }

        private Func<double, double> UnderlyingConvertToSystemBase;
        private Func<double, double> UnderlyingConvertFromSystemBase;

        protected SingleUnitBase(Quantities quantity, Systems system, double systemBaseMultyplier, string text)
        {
            this.Quantity = quantity;
            this.System = system;
            this.UnderlyingConvertToSystemBase = (double value) => value / systemBaseMultyplier;
            this.UnderlyingConvertFromSystemBase = (double value) => value * systemBaseMultyplier;
            this.Text = text;
        }

        protected SingleUnitBase(Quantities quantity, Systems system, Func<double, double> toBaseDeligate, Func<double, double> fromBaseDeligate, string text)
        {
            this.Quantity = quantity;
            this.System = system;
            this.UnderlyingConvertToSystemBase = toBaseDeligate;
            this.UnderlyingConvertFromSystemBase = fromBaseDeligate;
            this.Text = text;
        }

        public override FundamentalUnitPowerPair[] GetFundamentalUnitPairs()
        {
            return new FundamentalUnitPowerPair[] { new FundamentalUnitPowerPair { Unit = this, Power = 1 } };
        }

        public override UnitPowerPair[] GetUnitPairs()
        {
            return new UnitPowerPair[] { new UnitPowerPair { Unit = this, Power = 1 } };
        }

        public double ConvertToSystemBase(double value)
        {
            return UnderlyingConvertToSystemBase(value);
        }

        public double ConvertFromSystemBase(double value)
        {
            return UnderlyingConvertFromSystemBase(value);
        }

        public override IUnit Pow(int p)
        {
            return CompoundUnit.NewCompoundUnit(new UnitPowerPair[] { new UnitPowerPair { Unit = this, Power = p } });
        }

        public override string ToString()
        {
            return Text;
        }

        public override object Clone()
        {
            try
            {
                return Activator.CreateInstance(this.GetType());
            }
            catch (MissingMemberException e)
            {
                throw new InvalidOperationException("The object could not be cloned as the unit object type " +
                    "did not declare a public constructor with no arguments.\nIn order to clone this " +
                    "object, the \"Clone\" method should be overriden in a child class.", e);
            }
        }
    }
}
