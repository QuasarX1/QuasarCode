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
    public sealed class Kilogram : SingleUnitBase
    {
        public Kilogram() : base(Quantities.Mass, Systems.SI, 1, "Kg") { }
    }

    /// <summary> Gram </summary>
    public sealed class Gram : SingleUnitBase
    {
        public Gram() : base(Quantities.Mass, Systems.SI, 1000, "g") { }
    }

    /// <summary> Milligram </summary>
    public sealed class Milligram : SingleUnitBase
    {
        public Milligram() : base(Quantities.Mass, Systems.SI, 1000000, "mg") { }
    }

    /// <summary> Kilometer </summary>
    public sealed class Kilometer : SingleUnitBase
    {
        public Kilometer() : base(Quantities.Length, Systems.SI, 0.001, "km") { }
    }

    /// <summary> Metrer </summary>
    public sealed class Meter : SingleUnitBase
    {
        public Meter() : base(Quantities.Length, Systems.SI, 1, "m") { }
    }

    /// <summary> Centimeter </summary>
    public sealed class Centimeter : SingleUnitBase
    {
        public Centimeter() : base(Quantities.Length, Systems.SI, 100, "cm") { }
    }

    /// <summary> Millimeter </summary>
    public sealed class Millimeter : SingleUnitBase
    {
        public Millimeter() : base(Quantities.Length, Systems.SI, 1000, "mm") { }
    }

    /// <summary> Micrometer </summary>
    public sealed class Micrometer : SingleUnitBase
    {
        public Micrometer() : base(Quantities.Length, Systems.SI, 1000000, "\u00B5m") { }
    }

    /// <summary> Nanometer </summary>
    public sealed class Nanometer : SingleUnitBase
    {
        public Nanometer() : base(Quantities.Length, Systems.SI, 1000000000, "nm") { }
    }

    /// <summary> Nanometer </summary>
    public sealed class Angstrom : SingleUnitBase
    {
        public Angstrom() : base(Quantities.Length, Systems.SI, 10000000000, "\u00C5") { }
    }

    /// <summary> Hour </summary>
    public sealed class Hour : SingleUnitBase
    {
        public Hour() : base(Quantities.Time, Systems.SI, 3600, "h") { }
    }

    /// <summary> Minute </summary>
    public sealed class Minute : SingleUnitBase
    {
        public Minute() : base(Quantities.Time, Systems.SI, 60, "mins") { }
    }

    /// <summary> Second </summary>
    public sealed class Second : SingleUnitBase
    {
        public Second() : base(Quantities.Time, Systems.SI, 1, "s") { }
    }

    /// <summary> Degree </summary>
    public sealed class Degree : SingleUnitBase
    {
        public Degree() : base(Quantities.Angle, Systems.SI, Math.PI / 180, "\u00B0") { }
    }

    /// <summary> Radian </summary>
    public sealed class Radian : SingleUnitBase
    {
        public Radian() : base(Quantities.Angle, Systems.SI, 1, "Rad.") { }
    }

    /// <summary> Ampere (Amp) </summary>
    public sealed class Ampere : SingleUnitBase
    {
        public Ampere() : base(Quantities.ElectricCurrent, Systems.SI, 1, "A") { }
    }

    /// <summary> Kelvin </summary>
    public sealed class Kelvin : SingleUnitBase
    {
        public Kelvin() : base(Quantities.Temperature, Systems.SI, 1, "K") { }
    }

    /// <summary> Celcius </summary>
    public sealed class Celcius : SingleUnitBase//TODO: is this conversion correct???
    {
        public Celcius() : base(Quantities.Temperature, Systems.SI, (double value, int power) => (power == 1) ? value + 273.25 : value, (double value, int power) => (power == 1) ? value - 273.25 : value, "K") { }
    }

    /// <summary> Mole </summary>
    public sealed class Moles : SingleUnitBase
    {
        public Moles() : base(Quantities.Quantity, Systems.SI, 1, "mol") { }
    }

    /// <summary> Candela </summary>
    public sealed class Candela : SingleUnitBase
    {
        public Candela() : base(Quantities.LuminousIntensity, Systems.SI, 1, "cd") { }
    }
}
