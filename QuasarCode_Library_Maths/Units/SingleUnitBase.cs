using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    public abstract class SingleUnitBase : UnitBase, ISingleUnit
    {
        public IQuantity Quantity { get; protected set; }
        public ISystem System { get; protected set; }
        public string Text { get; protected set; }

        private readonly Func<double, int, double> UnderlyingConvertToSystemBase;
        private readonly Func<double, int, double> UnderlyingConvertFromSystemBase;

        protected SingleUnitBase(Quantities quantity, Systems system, double systemBaseMultyplier, string text)
        {
            switch (quantity)
            {
                case Quantities.None:
                    this.Quantity = new NoneQuantity();
                    break;
                case Quantities.Angle:
                    this.Quantity = new Angle();
                    break;
                case Quantities.Length:
                    this.Quantity = new Length();
                    break;
                case Quantities.Mass:
                    this.Quantity = new Mass();
                    break;
                case Quantities.Time:
                    this.Quantity = new Time();
                    break;
                case Quantities.ElectricCurrent:
                    this.Quantity = new ElectricCurrent();
                    break;
                case Quantities.Temperature:
                    this.Quantity = new Temperature();
                    break;
                case Quantities.Quantity:
                    this.Quantity = new Quantity();
                    break;
                case Quantities.LuminousIntensity:
                    this.Quantity = new LuminousIntensity();
                    break;
                default:
                    break;
            }

            switch (system)
            {
                case Systems.None:
                    this.System = new NoneSystem();
                    break;
                case Systems.SI:
                    this.System = new SI();
                    break;
                case Systems.Imperial:
                    this.System = new Imperial();
                    break;
                default:
                    break;
            }

            this.UnderlyingConvertToSystemBase = (double value, int power) => value / Math.Pow(systemBaseMultyplier, power);
            this.UnderlyingConvertFromSystemBase = (double value, int power) => value * Math.Pow(systemBaseMultyplier, power);
            this.Text = text;
        }

        protected SingleUnitBase(Quantities quantity, Systems system, Func<double, int, double> toBaseDeligate, Func<double, int, double> fromBaseDeligate, string text)
        {
            switch (quantity)
            {
                case Quantities.None:
                    this.Quantity = new NoneQuantity();
                    break;
                case Quantities.Angle:
                    this.Quantity = new Angle();
                    break;
                case Quantities.Length:
                    this.Quantity = new Length();
                    break;
                case Quantities.Mass:
                    this.Quantity = new Mass();
                    break;
                case Quantities.Time:
                    this.Quantity = new Time();
                    break;
                case Quantities.ElectricCurrent:
                    this.Quantity = new ElectricCurrent();
                    break;
                case Quantities.Temperature:
                    this.Quantity = new Temperature();
                    break;
                case Quantities.Quantity:
                    this.Quantity = new Quantity();
                    break;
                case Quantities.LuminousIntensity:
                    this.Quantity = new LuminousIntensity();
                    break;
                default:
                    break;
            }

            switch (system)
            {
                case Systems.None:
                    this.System = new NoneSystem();
                    break;
                case Systems.SI:
                    this.System = new SI();
                    break;
                case Systems.Imperial:
                    this.System = new Imperial();
                    break;
                default:
                    break;
            }

            this.UnderlyingConvertToSystemBase = toBaseDeligate;
            this.UnderlyingConvertFromSystemBase = fromBaseDeligate;
            this.Text = text;
        }

        protected SingleUnitBase(IQuantity quantity, ISystem system, double systemBaseMultyplier, string text)
        {
            this.Quantity = quantity;
            this.System = system;
            this.UnderlyingConvertToSystemBase = (double value, int power) => value / Math.Pow(systemBaseMultyplier, power);
            this.UnderlyingConvertFromSystemBase = (double value, int power) => value * Math.Pow(systemBaseMultyplier, power);
            this.Text = text;
        }

        protected SingleUnitBase(IQuantity quantity, ISystem system, Func<double, int, double> toBaseDeligate, Func<double, int, double> fromBaseDeligate, string text)
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

        public double ConvertToSystemBase(double value, int power = 1)
        {
            return UnderlyingConvertToSystemBase(value, power);
        }

        public double ConvertFromSystemBase(double value, int power = 1)
        {
            return UnderlyingConvertFromSystemBase(value, power);
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