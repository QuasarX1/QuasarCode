using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units.Common
{
    /// <summary> No Units </summary>
    public sealed class None : SingleUnitBase
    {
        public None() : base(Quantities.None, Systems.None, 1, "") { }
    }

    /// <summary> Metric Ton </summary>
    public sealed class MetricTon : SingleUnitBase
    {
        public MetricTon() : base(Quantities.Mass, Systems.SI, 0.001, "MetricTons") { }
    }

    /// <summary> Kilogram </summary>
    public sealed class Kg : SingleUnitBase
    {
        public Kg() : base(Quantities.Mass, Systems.SI, 1, "Kg") { }
    }

    /// <summary> Gram </summary>
    public sealed class g : SingleUnitBase
    {
        public g() : base(Quantities.Mass, Systems.SI, 1000, "g") { }
    }

    /// <summary> Milligram </summary>
    public sealed class mg : SingleUnitBase
    {
        public mg() : base(Quantities.Mass, Systems.SI, 1000000, "mg") { }
    }

    /// <summary> Kilometer </summary>
    public sealed class km : SingleUnitBase
    {
        public km() : base(Quantities.Length, Systems.SI, 0.001, "km") { }
    }

    /// <summary> Metrer </summary>
    public sealed class m : SingleUnitBase
    {
        public m() : base(Quantities.Length, Systems.SI, 1, "m") { }
    }

    /// <summary> Centimeter </summary>
    public sealed class cm : SingleUnitBase
    {
        public cm() : base(Quantities.Length, Systems.SI, 100, "cm") { }
    }

    /// <summary> Millimeter </summary>
    public sealed class mm : SingleUnitBase
    {
        public mm() : base(Quantities.Length, Systems.SI, 1000, "mm") { }
    }

    /// <summary> Micrometer </summary>
    public sealed class micron : SingleUnitBase
    {
        public micron() : base(Quantities.Length, Systems.SI, 1000000, "\u00B5m") { }
    }

    /// <summary> Nanometer </summary>
    public sealed class nm : SingleUnitBase
    {
        public nm() : base(Quantities.Length, Systems.SI, 1000000000, "nm") { }
    }

    /// <summary> Nanometer </summary>
    public sealed class Angstrom : SingleUnitBase
    {
        public Angstrom() : base(Quantities.Length, Systems.SI, 10000000000, "\u00C5") { }
    }

    /// <summary> Hour </summary>
    public sealed class h : SingleUnitBase
    {
        public h() : base(Quantities.Time, Systems.SI, 3600, "h") { }
    }

    /// <summary> Minute </summary>
    public sealed class Minute : SingleUnitBase
    {
        public Minute() : base(Quantities.Time, Systems.SI, 60, "mins") { }
    }

    /// <summary> Second </summary>
    public sealed class s : SingleUnitBase
    {
        public s() : base(Quantities.Time, Systems.SI, 1, "s") { }
    }

    /// <summary> Degree </summary>
    public sealed class Degrees : SingleUnitBase
    {
        public Degrees() : base(Quantities.Angle, Systems.SI, Math.PI / 180, "\u00B0") { }
    }

    /// <summary> Radian </summary>
    public sealed class Radian : SingleUnitBase
    {
        public Radian() : base(Quantities.Angle, Systems.SI, 1, "Rad.") { }
    }

    /// <summary> Ampere (Amp) </summary>
    public sealed class A : SingleUnitBase
    {
        public A() : base(Quantities.ElectricCurrent, Systems.SI, 1, "A") { }
    }

    /// <summary> Kelvin </summary>
    public sealed class K : SingleUnitBase
    {
        public K() : base(Quantities.Temperature, Systems.SI, 1, "K") { }
    }

    /// <summary> Celcius </summary>
    public sealed class Celcius : SingleUnitBase
    {
        public Celcius() : base(Quantities.Temperature, Systems.SI, (double value) => value + 273.25, (double value) => value - 273.25, "K") { }
    }

    /// <summary> Mole </summary>
    public sealed class mol : SingleUnitBase
    {
        public mol() : base(Quantities.Quantity, Systems.SI, 1, "mol") { }
    }

    /// <summary> Candela </summary>
    public sealed class cd : SingleUnitBase
    {
        public cd() : base(Quantities.LuminousIntensity, Systems.SI, 1, "cd") { }
    }
}
