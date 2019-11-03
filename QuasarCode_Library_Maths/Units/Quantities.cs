using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Units.Common;

namespace QuasarCode.Library.Maths.Units
{
    /// <summary>
    /// Physical quantitys that have units
    /// </summary>
    public enum Quantities
    {
        /// <summary>No assigned quantity</summary>
        None,

        /// <summary>Mesurement of rotation</summary>
        Angle,

        /// <summary>Mesurement of space</summary>
        Length,

        /// <summary>Mesurement of matter</summary>
        Mass,

        /// <summary>Mesurement of change</summary>
        Time,

        /// <summary>Mesurement of electricity</summary>
        ElectricCurrent,

        /// <summary>Mesurement of thermal energy</summary>
        Temperature,

        /// <summary>Mesurement of quantity</summary>
        Quantity,

        /// <summary>Mesurement of change</summary>
        LuminousIntensity
    }

    public abstract class QuantityBase : IQuantity
    {
        public string Name { get; }

        protected QuantityBase(string name)
        {
            this.Name = name;
        }
    }

    public sealed class NoneQuantity : QuantityBase
    {
        public NoneQuantity() : base("None") { }
    }

    public sealed class Angle : QuantityBase
    {
        public Angle() : base("Angle") { }
    }

    public sealed class Length : QuantityBase
    {
        public Length() : base("Length") { }
    }

    public sealed class Mass : QuantityBase
    {
        public Mass() : base("Mass") { }
    }

    public sealed class Time : QuantityBase
    {
        public Time() : base("Time") { }
    }

    public sealed class ElectricCurrent : QuantityBase
    {
        public ElectricCurrent() : base("ElectricCurrent") { }
    }

    public sealed class Temperature : QuantityBase
    {
        public Temperature() : base("Temperature") { }
    }

    public sealed class Quantity : QuantityBase
    {
        public Quantity() : base("Quantity") { }
    }

    public sealed class LuminousIntensity : QuantityBase
    {
        public LuminousIntensity() : base("LuminousIntensity") { }
    }
}