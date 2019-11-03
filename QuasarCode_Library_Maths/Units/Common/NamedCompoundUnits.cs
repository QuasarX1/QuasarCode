using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units.Common
{
    /// <summary> Solid Angle </summary>
    public sealed class Steradian : NamedCompoundUnit
    {
        public Steradian() : base("sr", new UnitPowerPair[] { new UnitPowerPair { Unit = new Radian(), Power = 2 } }) { }
    }

    /// <summary> Frequency </summary>
    public sealed class Hertz : NamedCompoundUnit
    {
        public Hertz() : base("Hz", new UnitPowerPair[] { new UnitPowerPair { Unit = new Second(), Power = -1 } }) { }
    }

    /// <summary> Force </summary>
    public sealed class Newton : NamedCompoundUnit
    {
        public Newton() : base("N", new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = 1 },
                                                     new UnitPowerPair { Unit = new Kilogram(), Power = 1 },
                                                     new UnitPowerPair { Unit = new Second(), Power = -2 } }) { }
    }

    /// <summary> Pressure </summary>
    public sealed class Pascal : NamedCompoundUnit
    {
        public Pascal() : base("Pa", new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = -1 },
                                                       new UnitPowerPair { Unit = new Kilogram(), Power = 1 },
                                                       new UnitPowerPair { Unit = new Second(), Power = -2 } }) { }
    }

    /// <summary> Energy </summary>
    public sealed class Joule : NamedCompoundUnit
    {
        public Joule() : base("J", new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = 2 },
                                                     new UnitPowerPair { Unit = new Kilogram(), Power = 1 },
                                                     new UnitPowerPair { Unit = new Second(), Power = -2 } }) { }
    }

    /// <summary> Power / EM Flux </summary>
    public sealed class Watt : NamedCompoundUnit
    {
        public Watt() : base("W", new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = 2 },
                                                     new UnitPowerPair { Unit = new Kilogram(), Power = 1 },
                                                     new UnitPowerPair { Unit = new Second(), Power = -3 } }) { }
    }

    /// <summary> Electric Charge </summary>
    public sealed class Coulomb : NamedCompoundUnit
    {
        public Coulomb() : base("C", new UnitPowerPair[] { new UnitPowerPair { Unit = new Ampere(), Power = 1 },
                                                     new UnitPowerPair { Unit = new Second(), Power = 1 } }) { }
    }

    /// <summary> Electric Potential (Voltage) </summary>
    public sealed class Volt : NamedCompoundUnit
    {
        public Volt() : base("V", new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = 2 },
                                                     new UnitPowerPair { Unit = new Kilogram(), Power = 1 },
                                                     new UnitPowerPair { Unit = new Second(), Power = -3 },
                                                     new UnitPowerPair { Unit = new Ampere(), Power = -1 } }) { }
    }

    /// <summary> Capacitance </summary>
    public sealed class Farad : NamedCompoundUnit
    {
        public Farad() : base("F", new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = -2 },
                                                     new UnitPowerPair { Unit = new Kilogram(), Power = -1 },
                                                     new UnitPowerPair { Unit = new Second(), Power = 4 },
                                                     new UnitPowerPair { Unit = new Ampere(), Power = 2 } }) { }
    }

    /// <summary> Resistance </summary>
    public sealed class Ohm : NamedCompoundUnit
    {
        public Ohm() : base("\u03A9", new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = 2 },
                                                            new UnitPowerPair { Unit = new Kilogram(), Power = 1 },
                                                            new UnitPowerPair { Unit = new Second(), Power = -3 },
                                                            new UnitPowerPair { Unit = new Ampere(), Power = -2 } }) { }
    }

    /// <summary> Conductance </summary>
    public sealed class Siemens : NamedCompoundUnit
    {
        public Siemens() : base("S", new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = -2 },
                                                     new UnitPowerPair { Unit = new Kilogram(), Power = -1 },
                                                     new UnitPowerPair { Unit = new Second(), Power = 3 },
                                                     new UnitPowerPair { Unit = new Ampere(), Power = 2 } }) { }
    }

    /// <summary> Magnetic Flux </summary>
    public sealed class Webber : NamedCompoundUnit
    {
        public Webber() : base("Wb", new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = 2 },
                                                       new UnitPowerPair { Unit = new Kilogram(), Power = 1 },
                                                       new UnitPowerPair { Unit = new Second(), Power = -2 },
                                                       new UnitPowerPair { Unit = new Ampere(), Power = -1 } }) { }
    }

    /// <summary> Magnetic Flux Density </summary>
    public sealed class Tesla : NamedCompoundUnit
    {
        public Tesla() : base("T", new UnitPowerPair[] { new UnitPowerPair { Unit = new Kilogram(), Power = 1 },
                                                     new UnitPowerPair { Unit = new Second(), Power = -2 },
                                                     new UnitPowerPair { Unit = new Ampere(), Power = -1 } }) { }
    }

    /// <summary> Inductance </summary>
    public sealed class Henry : NamedCompoundUnit
    {
        public Henry() : base("H", new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = 2 },
                                                     new UnitPowerPair { Unit = new Kilogram(), Power = 1 },
                                                     new UnitPowerPair { Unit = new Second(), Power = -2 },
                                                     new UnitPowerPair { Unit = new Ampere(), Power = -2 } }) { }
    }

    /// <summary> Luminous Flux </summary>
    public sealed class Lumen : NamedCompoundUnit
    {
        public Lumen() : base("lm", new UnitPowerPair[] { new UnitPowerPair { Unit = new Candela(), Power = 1 },
                                                     new UnitPowerPair { Unit = new Radian(), Power = 2 } }) { }
    }

    /// <summary> Illuminance </summary>
    public sealed class Lux : NamedCompoundUnit
    {
        public Lux() : base("lx", new UnitPowerPair[] { new UnitPowerPair { Unit = new Candela(), Power = 1 },
                                                     new UnitPowerPair { Unit = new Radian(), Power = 2 },
                                                     new UnitPowerPair { Unit = new Meter(), Power = -2 } }) { }
    }

    /// <summary> Radiation Activity (descreat instances) </summary>
    public sealed class Becquerel : NamedCompoundUnit
    {
        public Becquerel() : base("Bq", new UnitPowerPair[] { new UnitPowerPair { Unit = new Second(), Power = -1 } }) { }
    }

    /// <summary> Absorbed Dose / Specific Energy </summary>
    public sealed class Gray : NamedCompoundUnit
    {
        public Gray() : base("Gy", new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = 2 },
                                                     new UnitPowerPair { Unit = new Second(), Power = -2 } }) { }
    }

    /// <summary> Dose Equivilant </summary>
    public sealed class Sievert : NamedCompoundUnit
    {
        public Sievert() : base("Sv", new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = 2 },
                                                     new UnitPowerPair { Unit = new Second(), Power = -2 } }) { }
    }

    /// <summary> Catalitic Activity </summary>
    public sealed class Katal : NamedCompoundUnit
    {
        public Katal() : base("kat", new UnitPowerPair[] { new UnitPowerPair { Unit = new Moles(), Power = 1 },
                                                         new UnitPowerPair { Unit = new Second(), Power = -1 } }) { }
    }
}
