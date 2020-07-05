using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units.Common
{
    public sealed class PI : Value
    {
        public PI() : base(Math.PI, new None()) { }
    }

    public sealed class E : Value
    {
        public E() : base(Math.E, new None()) { }
    }

    public sealed class g : Value
    {
        public g() : base(9.80665, new MetersPerSecondSquared()) { }
    }

    public sealed class c : StandardFormValue
    {
        public c() : base(2.99792458, 8, new MetersPerSecond()) { }
    }

    public sealed class e : StandardFormValue
    {
        public e() : base(1.602176565, -19, new Coulomb()) { }
    }

    public sealed class G : StandardFormValue
    {
        public G() : base(6.67384, -11, CompoundUnit.NewCompoundUnit(new UnitPowerPair { Unit = new Newton(), Power = 1 }, new UnitPowerPair { Unit = new Meter(), Power = 2 }, new UnitPowerPair { Unit = new Kilogram(), Power = -2 })) { }
    }

    public sealed class h : StandardFormValue
    {
        public h() : base(6.62606957, -34, CompoundUnit.NewCompoundUnit(new UnitPowerPair { Unit = new Joule(), Power = 1 }, new UnitPowerPair { Unit = new Second(), Power = 1 })) { }
    }

    public sealed class k : StandardFormValue
    {
        public k() : base(1.3806488, -23, CompoundUnit.NewCompoundUnit(new UnitPowerPair { Unit = new Joule(), Power = 1 }, new UnitPowerPair { Unit = new Kelvin(), Power = -1 })) { }
    }

    public sealed class AvagadrosNumber : StandardFormValue
    {
        public AvagadrosNumber() : base(6.02214129, 23, new None()) { }
    }

    public sealed class R : Value
    {
        public R() : base(8.3144621, CompoundUnit.NewCompoundUnit(new UnitPowerPair { Unit = new Joule(), Power = 1 }, new UnitPowerPair { Unit = new Moles(), Power = -1 }, new UnitPowerPair { Unit = new Kelvin(), Power = -1 })) { }
    }

    public sealed class ElectronMass : StandardFormValue
    {
        public ElectronMass() : base(9.10938291, -31, new Kilogram()) { }
    }

    public sealed class ProtonMass : StandardFormValue
    {
        public ProtonMass() : base(1.672621777, -27, new Kilogram()) { }
    }

    public sealed class NeutronMass : StandardFormValue
    {
        public NeutronMass() : base(1.674927351, -27, new Kilogram()) { }
    }

    public sealed class PermeabilityOfFreeSpace : StandardFormValue
    {
        public PermeabilityOfFreeSpace() : base(4 * Math.PI, -7, CompoundUnit.NewCompoundUnit(new UnitPowerPair { Unit = new Webber(), Power = 1 }, new UnitPowerPair { Unit = new Ampere(), Power = -1 }, new UnitPowerPair { Unit = new Meter(), Power = -1 })) { }
    }

    public sealed class PermittivityOfFreeSpace : StandardFormValue
    {
        public PermittivityOfFreeSpace() : base(8.854187817, -12, CompoundUnit.NewCompoundUnit(new UnitPowerPair { Unit = new Coulomb(), Power = 2 }, new UnitPowerPair { Unit = new Newton(), Power = -1 }, new UnitPowerPair { Unit = new Meter(), Power = -2 })) { }
    }
}
