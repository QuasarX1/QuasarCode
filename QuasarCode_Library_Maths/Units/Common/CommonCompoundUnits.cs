using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units.Common
{
    /// <summary> Area </summary>
    public class MetersSquared : CompoundUnit
    {
        public MetersSquared() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = 2 } }) { }
    }

    /// <summary> Volume </summary>
    public class MetersCubed : CompoundUnit
    {
        public MetersCubed() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = 3 } }) { }
    }

    /// <summary> Speed </summary>
    public class MetersPerSecond : CompoundUnit
    {
        public MetersPerSecond() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = 1 },
                                                              new UnitPowerPair { Unit = new s(), Power = -1 } }) { }
    }

    /// <summary> Acceleration </summary>
    public class MetersPerSecondSquared : CompoundUnit
    {
        public MetersPerSecondSquared() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = 1 },
                                                                     new UnitPowerPair { Unit = new s(), Power = -2 } }) { }
    }

    /// <summary> Wave Number </summary>
    public class ReciprocalMeter : CompoundUnit
    {
        public ReciprocalMeter() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = -1 } }) { }
    }

    /// <summary> Mass Density </summary>
    public class KilogramsPerMeterCubed : CompoundUnit
    {
        public KilogramsPerMeterCubed() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new Kg(), Power = 1 },
                                                                     new UnitPowerPair { Unit = new m(), Power = -3 } }) { }
    }

    /// <summary> Specific Volume </summary>
    public class MetersCubedPerKilogram : CompoundUnit
    {
        public MetersCubedPerKilogram() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new m(), Power = 3 },
                                                                     new UnitPowerPair { Unit = new Kg(), Power = -1 } }) { }
    }

    /// <summary> Current Density </summary>
    public class AmpsPerMeterSquared : CompoundUnit
    {
        public AmpsPerMeterSquared() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new A(), Power = 1 },
                                                                  new UnitPowerPair { Unit = new m(), Power = -2 } }) { }
    }

    /// <summary> Magnetic Field Strength </summary>
    public class AmpsPerMeter : CompoundUnit
    {
        public AmpsPerMeter() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new A(), Power = 1 },
                                                           new UnitPowerPair { Unit = new m(), Power = -1 } }) { }
    }

    /// <summary> Substance Concentration </summary>
    public class MolesPerMeterCubed : CompoundUnit
    {
        public MolesPerMeterCubed() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new mol(), Power = 1 },
                                                                 new UnitPowerPair { Unit = new m(), Power = -3 } }) { }
    }

    /// <summary> Luminance </summary>
    public class CandelaPerMeterSquared : CompoundUnit
    {
        public CandelaPerMeterSquared() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new cd(), Power = 1 },
                                                                     new UnitPowerPair { Unit = new m(), Power = -2 } }) { }
    }
}
