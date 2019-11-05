using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units.Common
{
    public class Unitless : Value
    {
        public Unitless(double magnitude) : base(magnitude, new None()) { }
    }

    public class Mass : Value
    {
        public Mass(double magnitude) : base(magnitude, new Kilogram()) { }
    }

    public class Distance : Value
    {
        public Distance(double magnitude) : base(magnitude, new Meter()) { }
    }

    public class Time : Value
    {
        public Time(double magnitude) : base(magnitude, new Second()) { }
    }

    public class Angle : Value
    {
        public Angle(double magnitude) : base(magnitude, new Radian()) { }
    }

    public class Current : Value
    {
        public Current(double magnitude) : base(magnitude, new Ampere()) { }
    }

    public class Temperature : Value
    {
        public Temperature(double magnitude) : base(magnitude, new Kelvin()) { }
    }

    public class Quantity : Value
    {
        public Quantity(double magnitude) : base(magnitude, new Moles()) { }
    }

    public class LuminousIntensity : Value
    {
        public LuminousIntensity(double magnitude) : base(magnitude, new Candela()) { }
    }

    public class Area : Value
    {
        public Area(double magnitude) : base(magnitude, new MetersSquared()) { }
    }

    public class Volume : Value
    {
        public Volume(double magnitude) : base(magnitude, new MetersCubed()) { }
    }

    public class Speed : Value
    {
        public Speed(double magnitude) : base(magnitude, new MetersPerSecond()) { }
    }

    public class Acceleration : Value
    {
        public Acceleration(double magnitude) : base(magnitude, new MetersPerSecondSquared()) { }
    }

    public class WaveNumber : Value
    {
        public WaveNumber(double magnitude) : base(magnitude, new ReciprocalMeter()) { }
    }

    public class Density : Value
    {
        public Density(double magnitude) : base(magnitude, new KilogramsPerMeterCubed()) { }
    }

    public class SpecificVolume : Value
    {
        public SpecificVolume(double magnitude) : base(magnitude, new MetersCubedPerKilogram()) { }
    }

    public class CurrentDensity : Value
    {
        public CurrentDensity(double magnitude) : base(magnitude, new AmpsPerMeterSquared()) { }
    }

    public class MagneticFieldStrength : Value
    {
        public MagneticFieldStrength(double magnitude) : base(magnitude, new AmpsPerMeter()) { }
    }

    public class SubstanceConcentration : Value
    {
        public SubstanceConcentration(double magnitude) : base(magnitude, new MolesPerMeterCubed()) { }
    }

    public class Luminance : Value
    {
        public Luminance(double magnitude) : base(magnitude, new CandelaPerMeterSquared()) { }
    }

    public class SolidAngle : Value
    {
        public SolidAngle(double magnitude) : base(magnitude, new Steradian()) { }
    }

    public class Frequency : Value
    {
        public Frequency(double magnitude) : base(magnitude, new Hertz()) { }
    }

    public class Force : Value
    {
        public Force(double magnitude) : base(magnitude, new Newton()) { }
    }

    public class Pressure : Value
    {
        public Pressure(double magnitude) : base(magnitude, new Pascal()) { }
    }

    public class Energy : Value
    {
        public Energy(double magnitude) : base(magnitude, new Joule()) { }
    }

    /// <summary>
    /// Power (also EM Flux)
    /// </summary>
    public class Power : Value
    {
        public Power(double magnitude) : base(magnitude, new Watt()) { }
    }

    public class Charge : Value
    {
        public Charge(double magnitude) : base(magnitude, new Coulomb()) { }
    }

    /// <summary>
    /// Voltage (also Electric Potential)
    /// </summary>
    public class Voltage : Value
    {
        public Voltage(double magnitude) : base(magnitude, new Coulomb()) { }
    }

    public class Capacitance : Value
    {
        public Capacitance(double magnitude) : base(magnitude, new Farad()) { }
    }

    public class Resistance : Value
    {
        public Resistance(double magnitude) : base(magnitude, new Ohm()) { }
    }

    public class Conductance : Value
    {
        public Conductance(double magnitude) : base(magnitude, new Siemens()) { }
    }

    public class MagneticFlux : Value
    {
        public MagneticFlux(double magnitude) : base(magnitude, new Webber()) { }
    }

    public class MagneticFluxDensity : Value
    {
        public MagneticFluxDensity(double magnitude) : base(magnitude, new Tesla()) { }
    }

    public class Inductance : Value
    {
        public Inductance(double magnitude) : base(magnitude, new Henry()) { }
    }

    public class LuminousFlux : Value
    {
        public LuminousFlux(double magnitude) : base(magnitude, new Lumen()) { }
    }

    public class Illuminance : Value
    {
        public Illuminance(double magnitude) : base(magnitude, new Lux()) { }
    }

    public class Activity : Value
    {
        public Activity(double magnitude) : base(magnitude, new Becquerel()) { }
    }

    public class AbsorbedDose : Value
    {
        public AbsorbedDose(double magnitude) : base(magnitude, new Gray()) { }
    }

    public class DoseEquivilant : Value
    {
        public DoseEquivilant(double magnitude) : base(magnitude, new Sievert()) { }
    }

    public class CataliticActivity : Value
    {
        public CataliticActivity(double magnitude) : base(magnitude, new Katal()) { }
    }
}