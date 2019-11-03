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
    public sealed class Hz : NamedCompoundUnit
    {
        public Hz() : base("Hz", new UnitPowerPair[] { new UnitPowerPair { Unit = new s(), Power = -1 } }) { }
    }

    /// <summary> Force </summary>
    public sealed class N : NamedCompoundUnit
    {
        public N() : base("N", new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = 1 },
                                                     new UnitPowerPair { Unit = new Kg(), Power = 1 },
                                                     new UnitPowerPair { Unit = new s(), Power = -2 } }) { }
    }

    /// <summary> Pressure </summary>
    public sealed class Pa : NamedCompoundUnit
    {
        public Pa() : base("Pa", new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = -1 },
                                                       new UnitPowerPair { Unit = new Kg(), Power = 1 },
                                                       new UnitPowerPair { Unit = new s(), Power = -2 } }) { }
    }

    /// <summary> Energy </summary>
    public sealed class J : NamedCompoundUnit
    {
        public J() : base("J", new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = 2 },
                                                     new UnitPowerPair { Unit = new Kg(), Power = 1 },
                                                     new UnitPowerPair { Unit = new s(), Power = -2 } }) { }
    }

    /// <summary> Power / EM Flux </summary>
    public sealed class W : NamedCompoundUnit
    {
        public W() : base("W", new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = 2 },
                                                     new UnitPowerPair { Unit = new Kg(), Power = 1 },
                                                     new UnitPowerPair { Unit = new s(), Power = -3 } }) { }
    }

    /// <summary> Electric Charge </summary>
    public sealed class C : NamedCompoundUnit
    {
        public C() : base("C", new UnitPowerPair[] { new UnitPowerPair { Unit = new A(), Power = 1 },
                                                     new UnitPowerPair { Unit = new s(), Power = 1 } }) { }
    }

    /// <summary> Electric Potential (Voltage) </summary>
    public sealed class V : NamedCompoundUnit
    {
        public V() : base("V", new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = 2 },
                                                     new UnitPowerPair { Unit = new Kg(), Power = 1 },
                                                     new UnitPowerPair { Unit = new s(), Power = -3 },
                                                     new UnitPowerPair { Unit = new A(), Power = -1 } }) { }
    }

    /// <summary> Capacitance (farad) </summary>
    public sealed class F : NamedCompoundUnit
    {
        public F() : base("F", new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = -2 },
                                                     new UnitPowerPair { Unit = new Kg(), Power = -1 },
                                                     new UnitPowerPair { Unit = new s(), Power = 4 },
                                                     new UnitPowerPair { Unit = new A(), Power = 2 } }) { }
    }

    /// <summary> Resistance </summary>
    public sealed class Ohm : NamedCompoundUnit
    {
        public Ohm() : base("\u03A9", new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = 2 },
                                                            new UnitPowerPair { Unit = new Kg(), Power = 1 },
                                                            new UnitPowerPair { Unit = new s(), Power = -3 },
                                                            new UnitPowerPair { Unit = new A(), Power = -2 } }) { }
    }

    /// <summary> Conductance (siemens) </summary>
    public sealed class S : NamedCompoundUnit
    {
        public S() : base("S", new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = -2 },
                                                     new UnitPowerPair { Unit = new Kg(), Power = -1 },
                                                     new UnitPowerPair { Unit = new s(), Power = 3 },
                                                     new UnitPowerPair { Unit = new A(), Power = 2 } }) { }
    }

    /// <summary> Magnetic Flux (webber) </summary>
    public sealed class Wb : NamedCompoundUnit
    {
        public Wb() : base("Wb", new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = 2 },
                                                       new UnitPowerPair { Unit = new Kg(), Power = 1 },
                                                       new UnitPowerPair { Unit = new s(), Power = -2 },
                                                       new UnitPowerPair { Unit = new A(), Power = -1 } }) { }
    }

    /// <summary> Magnetic Flux Density (tesla) </summary>
    public sealed class T : NamedCompoundUnit
    {
        public T() : base("T", new UnitPowerPair[] { new UnitPowerPair { Unit = new Kg(), Power = 1 },
                                                     new UnitPowerPair { Unit = new s(), Power = -2 },
                                                     new UnitPowerPair { Unit = new A(), Power = -1 } }) { }
    }

    /// <summary> Inductance (henry) </summary>
    public sealed class H : NamedCompoundUnit
    {
        public H() : base("H", new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = 2 },
                                                     new UnitPowerPair { Unit = new Kg(), Power = 1 },
                                                     new UnitPowerPair { Unit = new s(), Power = -2 },
                                                     new UnitPowerPair { Unit = new A(), Power = -2 } }) { }
    }

    /// <summary> Luminous Flux (lumen) </summary>
    public sealed class lm : NamedCompoundUnit
    {
        public lm() : base("lm", new UnitPowerPair[] { new UnitPowerPair { Unit = new cd(), Power = 1 },
                                                     new UnitPowerPair { Unit = new Radian(), Power = 2 } }) { }
    }

    /// <summary> Illuminance (lux) </summary>
    public sealed class lx : NamedCompoundUnit
    {
        public lx() : base("lx", new UnitPowerPair[] { new UnitPowerPair { Unit = new cd(), Power = 1 },
                                                     new UnitPowerPair { Unit = new Radian(), Power = 2 },
                                                     new UnitPowerPair { Unit = new m(), Power = -2 } }) { }
    }

    /// <summary> Radiation Activity (descreat instances) (Becquerel) </summary>
    public sealed class Bq : NamedCompoundUnit
    {
        public Bq() : base("Bq", new UnitPowerPair[] { new UnitPowerPair { Unit = new s(), Power = -1 } }) { }
    }

    /// <summary> Absorbed Dose / Specific Energy (gray) </summary>
    public sealed class Gy : NamedCompoundUnit
    {
        public Gy() : base("Gy", new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = 2 },
                                                     new UnitPowerPair { Unit = new s(), Power = -2 } }) { }
    }

    /// <summary> Dose Equivilant (sievert) </summary>
    public sealed class Sv : NamedCompoundUnit
    {
        public Sv() : base("Sv", new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = 2 },
                                                     new UnitPowerPair { Unit = new s(), Power = -2 } }) { }
    }

    /// <summary> Catalitic Activity (katal) </summary>
    public sealed class kat : NamedCompoundUnit
    {
        public kat() : base("kat", new UnitPowerPair[] { new UnitPowerPair { Unit = new mol(), Power = 1 },
                                                         new UnitPowerPair { Unit = new s(), Power = -1 } }) { }
    }
}
