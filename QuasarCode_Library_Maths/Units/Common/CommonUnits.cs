using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units.Common
{
    public class None : SingleUnitBase
    {
        public None() : base(Quantities.None, Systems.None, 1, "") { }
    }

    public class MetricTon : SingleUnitBase
    {
        public MetricTon() : base(Quantities.Mass, Systems.SI, 0.001, "MetricTons") { }
    }

    public class Kg : SingleUnitBase
    {
        public Kg() : base(Quantities.Mass, Systems.SI, 1, "Kg") { }
    }

    public class g : SingleUnitBase
    {
        public g() : base(Quantities.Mass, Systems.SI, 1000, "g") { }
    }

    public class mg : SingleUnitBase
    {
        public mg() : base(Quantities.Mass, Systems.SI, 1000000, "mg") { }
    }

    public class km : SingleUnitBase
    {
        public km() : base(Quantities.Distance, Systems.SI, 0.001, "km") { }
    }

    public class m : SingleUnitBase
    {
        public m() : base(Quantities.Distance, Systems.SI, 1, "m") { }
    }

    public class cm : SingleUnitBase
    {
        public cm() : base(Quantities.Distance, Systems.SI, 100, "cm") { }
    }

    public class mm : SingleUnitBase
    {
        public mm() : base(Quantities.Distance, Systems.SI, 1000, "mm") { }
    }

    public class micron : SingleUnitBase
    {
        public micron() : base(Quantities.Distance, Systems.SI, 1000000, "\u00B5m") { }
    }

    public class nm : SingleUnitBase
    {
        public nm() : base(Quantities.Distance, Systems.SI, 1000000000, "nm") { }
    }

    public class h : SingleUnitBase
    {
        public h() : base(Quantities.Time, Systems.SI, 3600, "h") { }
    }

    public class Minute : SingleUnitBase
    {
        public Minute() : base(Quantities.Time, Systems.SI, 60, "mins") { }
    }

    public class s : SingleUnitBase
    {
        public s() : base(Quantities.Time, Systems.SI, 1, "s") { }
    }

    public class Degrees : SingleUnitBase
    {
        public Degrees() : base(Quantities.Angle, Systems.SI, Math.PI / 180, "\u00B0") { }
    }

    public class Radian : SingleUnitBase
    {
        public Radian() : base(Quantities.Angle, Systems.SI, 1, "Rad.") { }
    }
}
