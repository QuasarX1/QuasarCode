using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Units.Common;

namespace QuasarCode.Library.Maths.Units
{
    /// <summary>
    /// The systems of mesurement with avalable units
    /// </summary>
    public enum Systems
    {
        /// <summary>No present system</summary>
        None,

        /// <summary>SI or Metric</summary>
        SI,

        /// <summary>Imperial (Old)</summary>
        Imperial
    }

    public abstract class SystemBase : ISystem
    {
        public string Name { get; protected set; }
        public Dictionary<Tuple<IQuantity, ISystem, ISystem>, SystemConversion> Conversions { get; protected set; }
        public Dictionary<IQuantity, ISingleUnit> BaseUnits { get; protected set; }

        protected SystemBase(string name, ISingleUnit[] baseUnits, params SystemConversion[] conversions)
        {
            this.Name = name;

            BaseUnits = new Dictionary<IQuantity, ISingleUnit>();
            foreach (ISingleUnit unit in baseUnits)
            {
                BaseUnits.TryAdd(unit.Quantity, unit);
            }

            Conversions = new Dictionary<Tuple<IQuantity, ISystem, ISystem>, SystemConversion>();
            foreach (SystemConversion conversion in conversions)
            {
                Conversions.TryAdd(new Tuple<IQuantity, ISystem, ISystem>(conversion.ForQuantity, conversion.FromSystem, conversion.ToSystem), conversion);
            }

            if (this.GetType() != typeof(NoneSystem))
            {
                Conversions.TryAdd(new Tuple<IQuantity, ISystem, ISystem>(new NoneQuantity(), this, this),
                    new SystemConversion(new NoneQuantity(), this, this, (double value) => value));

                Conversions.TryAdd(new Tuple<IQuantity, ISystem, ISystem>(new Angle(), this, this),
                    new SystemConversion(new Angle(), this, this, (double value) => value));

                Conversions.TryAdd(new Tuple<IQuantity, ISystem, ISystem>(new Length(), this, this),
                    new SystemConversion(new Length(), this, this, (double value) => value));

                Conversions.TryAdd(new Tuple<IQuantity, ISystem, ISystem>(new Mass(), this, this),
                    new SystemConversion(new Mass(), this, this, (double value) => value));

                Conversions.TryAdd(new Tuple<IQuantity, ISystem, ISystem>(new Time(), this, this),
                    new SystemConversion(new Time(), this, this, (double value) => value));

                Conversions.TryAdd(new Tuple<IQuantity, ISystem, ISystem>(new ElectricCurrent(), this, this),
                    new SystemConversion(new ElectricCurrent(), this, this, (double value) => value));

                Conversions.TryAdd(new Tuple<IQuantity, ISystem, ISystem>(new Temperature(), this, this),
                    new SystemConversion(new Temperature(), this, this, (double value) => value));

                Conversions.TryAdd(new Tuple<IQuantity, ISystem, ISystem>(new Quantity(), this, this),
                    new SystemConversion(new Quantity(), this, this, (double value) => value));

                Conversions.TryAdd(new Tuple<IQuantity, ISystem, ISystem>(new LuminousIntensity(), this, this),
                    new SystemConversion(new LuminousIntensity(), this, this, (double value) => value));
            }
        }
    }

    public sealed class NoneSystem : SystemBase
    {
        public NoneSystem() : base("None", new ISingleUnit[] { new None() }) { }
    }

    public sealed class SI : SystemBase//TODO: add imperial conversions
    {
        public SI() : base("SI",
            new ISingleUnit[] { new Radian(), new Meter(), new Kilogram(), new Second(), new Ampere(), new Kelvin(), new Moles(), new Candela() }) { }
    }

    public sealed class Imperial : SystemBase//TODO: add imperial units and conversions
    {
        public Imperial() : base("Imperial",
            new ISingleUnit[] { }) { }
    }
}