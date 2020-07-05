using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units.Common
{
    /// <summary> Area </summary>
    public sealed class MetersSquared : CompoundUnit
    {
        public MetersSquared() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = 2 } }) { }
    }

    /// <summary> Volume </summary>
    public sealed class MetersCubed : CompoundUnit
    {
        public MetersCubed() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = 3 } }) { }
    }

    /// <summary> Speed </summary>
    public sealed class MetersPerSecond : CompoundUnit
    {
        public MetersPerSecond() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = 1 },
                                                              new UnitPowerPair { Unit = new Second(), Power = -1 } }) { }
    }

    /// <summary> Acceleration </summary>
    public sealed class MetersPerSecondSquared : CompoundUnit
    {
        public MetersPerSecondSquared() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = 1 },
                                                                     new UnitPowerPair { Unit = new Second(), Power = -2 } }) { }
    }

    /// <summary> Wave Number </summary>
    public sealed class ReciprocalMeter : CompoundUnit
    {
        public ReciprocalMeter() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = -1 } }) { }
    }

    /// <summary> Mass Density </summary>
    public sealed class KilogramsPerMeterCubed : CompoundUnit
    {
        public KilogramsPerMeterCubed() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new Kilogram(), Power = 1 },
                                                                     new UnitPowerPair { Unit = new Meter(), Power = -3 } }) { }
    }

    /// <summary> Specific Volume </summary>
    public sealed class MetersCubedPerKilogram : CompoundUnit
    {
        public MetersCubedPerKilogram() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new Meter(), Power = 3 },
                                                                     new UnitPowerPair { Unit = new Kilogram(), Power = -1 } }) { }
    }

    /// <summary> Current Density </summary>
    public sealed class AmpsPerMeterSquared : CompoundUnit
    {
        public AmpsPerMeterSquared() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new Ampere(), Power = 1 },
                                                                  new UnitPowerPair { Unit = new Meter(), Power = -2 } }) { }
    }

    /// <summary> Magnetic Field Strength </summary>
    public sealed class AmpsPerMeter : CompoundUnit
    {
        public AmpsPerMeter() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new Ampere(), Power = 1 },
                                                           new UnitPowerPair { Unit = new Meter(), Power = -1 } }) { }
    }

    /// <summary> Substance Concentration </summary>
    public sealed class MolesPerMeterCubed : CompoundUnit
    {
        public MolesPerMeterCubed() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new Moles(), Power = 1 },
                                                                 new UnitPowerPair { Unit = new Meter(), Power = -3 } }) { }
    }

    /// <summary> Luminance </summary>
    public sealed class CandelaPerMeterSquared : CompoundUnit
    {
        public CandelaPerMeterSquared() : base(new UnitPowerPair[] { new UnitPowerPair { Unit = new Candela(), Power = 1 },
                                                                     new UnitPowerPair { Unit = new Meter(), Power = -2 } }) { }
    }
}