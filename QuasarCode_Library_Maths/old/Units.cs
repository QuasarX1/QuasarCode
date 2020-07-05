using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

namespace QuasarCode.Library.Maths.old
{
    /// <summary>
    /// An enumeration of units relating to physical quantities
    /// </summary>
    public enum Units
    {
        /// <summary>
        /// Lack of units
        /// </summary>
        NoUnit,



        /// <summary>
        /// Unit of angle
        /// </summary>
        Degrees,

        /// <summary>
        /// Unit of angle
        /// </summary>
        Radians,



        /// <summary>
        /// Unit of length (SI)
        /// </summary>
        km,

        /// <summary>
        /// Unit of length (SI base)
        /// </summary>
        m,

        /// <summary>
        /// Unit of length (SI)
        /// </summary>
        cm,

        /// <summary>
        /// Unit of length (SI)
        /// </summary>
        mm,

        /// <summary>
        /// Unit of length (SI)
        /// </summary>
        micro_m,

        /// <summary>
        /// Unit of length (SI)
        /// </summary>
        nm,



        /// <summary>
        /// Unit of mass (SI base)
        /// </summary>
        Kg,

        /// <summary>
        /// Unit of mass (SI)
        /// </summary>
        g,

        /// <summary>
        /// Unit of mass (SI)
        /// </summary>
        mg,

        /// <summary>
        /// Unit of mass (Imperial base)
        /// </summary>
        lb,

        /// <summary>
        /// Unit of mass (Imperial)
        /// </summary>
        oz,


        // time, other base quantities?
        /// <summary>
        /// Unit of time (SI)
        /// </summary>
        h,

        /// <summary>
        /// Unit of time (SI)
        /// </summary>
        min,

        /// <summary>
        /// Unit of time (SI base)
        /// </summary>
        s,

        /// <summary>
        /// Unit of time (SI)
        /// </summary>
        ms
    }

    /// <summary>
    /// Extends the Units enum
    /// </summary>
    public static class UnitsMethods
    {
        /// <summary>
        /// Creates a Unit object with a single unit raised to a power
        /// </summary>
        /// <param name="unit">The unit</param>
        /// <param name="power">The power to raise the unit to</param>
        /// <returns></returns>
        public static Unit Pow(this Units unit, int power)
        {
            return new Unit(unit, power);
        }

        /// <summary>
        /// Gets the string representation of the unit
        /// </summary>
        /// <param name="unit">The unit</param>
        /// <returns>String</returns>
        public static string AsString(this Units unit)
        {
            string result;

            switch (unit)
            {
                case Units.NoUnit:
                    result = "No Units";
                    break;
                case Units.Degrees:
                    result = "°";
                    break;
                case Units.Radians:
                    result = "rad.";
                    break;
                case Units.km:
                    result = "km";
                    break;
                case Units.m:
                    result = "m";
                    break;
                case Units.cm:
                    result = "cm";
                    break;
                case Units.mm:
                    result = "mm";
                    break;
                case Units.micro_m:
                    result = "μm";
                    break;
                case Units.nm:
                    result = "nm";
                    break;
                case Units.Kg:
                    result = "Kg";
                    break;
                case Units.g:
                    result = "g";
                    break;
                case Units.mg:
                    result = "mg";
                    break;
                case Units.lb:
                    result = "lb";
                    break;
                case Units.oz:
                    result = "oz";
                    break;
                case Units.h:
                    result = "h";
                    break;
                case Units.min:
                    result = "min";
                    break;
                case Units.s:
                    result = "s";
                    break;
                case Units.ms:
                    result = "ms";
                    break;
                default:
                    result = "";
                    break;
            }

            return result;
        }

        /// <summary>
        /// Retrives the multiplier used to convert 1 of the relivent system's base unit into the desiered unit. Use 1/return value to go the other way
        /// </summary>
        /// <param name="unit">The desiered unit</param>
        /// <returns>Multiplier to convert the base unit into the desiered one</returns>
        public static double GetBaseMultyplier(this Units unit)
        {
            double result;

            switch (unit)
            {
                case Units.NoUnit:
                    result = 0;
                    break;
                case Units.Degrees:
                    result = 1;
                    break;
                case Units.Radians:
                    result = 1;
                    break;
                case Units.km:
                    result = 1000;
                    break;
                case Units.m:
                    result = 1;
                    break;
                case Units.cm:
                    result = 0.01;
                    break;
                case Units.mm:
                    result = 0.001;
                    break;
                case Units.micro_m:
                    result = 0.000001;
                    break;
                case Units.nm:
                    result = 0.000000001;
                    break;
                case Units.Kg:
                    result = 1;
                    break;
                case Units.g:
                    result = 0.001;
                    break;
                case Units.mg:
                    result = 0.000001;
                    break;
                case Units.lb:
                    result = 1;
                    break;
                case Units.oz:
                    result = 0.0625;// 1/16
                    break;
                case Units.h:
                    result = 3600;
                    break;
                case Units.min:
                    result = 60;
                    break;
                case Units.s:
                    result = 1;
                    break;
                case Units.ms:
                    result = 0.001;
                    break;
                default:
                    result = 0;
                    break;
            }


            return result;
        }

        /// <summary>
        /// Retrives the physical Quantity the provided unit is associated with
        /// </summary>
        /// <param name="unit">The unit</param>
        /// <returns>An option from the Quantities enum</returns>
        public static Quantities GetQuantity(this Units unit)
        {
            Quantities result;

            switch (unit)
            {
                case Units.NoUnit:
                    result = Quantities.None;
                    break;
                case Units.Degrees:
                    result = Quantities.Angle;
                    break;
                case Units.Radians:
                    result = Quantities.Angle;
                    break;
                case Units.km:
                    result = Quantities.Distance;
                    break;
                case Units.m:
                    result = Quantities.Distance;
                    break;
                case Units.cm:
                    result = Quantities.Distance;
                    break;
                case Units.mm:
                    result = Quantities.Distance;
                    break;
                case Units.micro_m:
                    result = Quantities.Distance;
                    break;
                case Units.nm:
                    result = Quantities.Distance;
                    break;
                case Units.Kg:
                    result = Quantities.Mass;
                    break;
                case Units.g:
                    result = Quantities.Mass;
                    break;
                case Units.mg:
                    result = Quantities.Mass;
                    break;
                case Units.lb:
                    result = Quantities.Mass;
                    break;
                case Units.oz:
                    result = Quantities.Mass;
                    break;
                case Units.h:
                    result = Quantities.Time;
                    break;
                case Units.min:
                    result = Quantities.Time;
                    break;
                case Units.s:
                    result = Quantities.Time;
                    break;
                case Units.ms:
                    result = Quantities.Time;
                    break;
                default:
                    result = Quantities.None;
                    break;
            }

            return result;
        }

        /// <summary>
        /// Retrives the unit System the provided unit is associated with
        /// </summary>
        /// <param name="unit">The unit</param>
        /// <returns>An option from the UnitSystems enum</returns>
        public static UnitSystems GetSystem(this Units unit)
        {
            UnitSystems result;

            switch (unit)
            {
                case Units.NoUnit:
                    result = UnitSystems.None;
                    break;
                case Units.Degrees:
                    result = UnitSystems.Degrees;
                    break;
                case Units.Radians:
                    result = UnitSystems.Radians;
                    break;
                case Units.km:
                    result = UnitSystems.SI;
                    break;
                case Units.m:
                    result = UnitSystems.SI;
                    break;
                case Units.cm:
                    result = UnitSystems.SI;
                    break;
                case Units.mm:
                    result = UnitSystems.SI;
                    break;
                case Units.micro_m:
                    result = UnitSystems.SI;
                    break;
                case Units.nm:
                    result = UnitSystems.SI;
                    break;
                case Units.Kg:
                    result = UnitSystems.SI;
                    break;
                case Units.g:
                    result = UnitSystems.SI;
                    break;
                case Units.mg:
                    result = UnitSystems.SI;
                    break;
                case Units.lb:
                    result = UnitSystems.Imperial;
                    break;
                case Units.oz:
                    result = UnitSystems.Imperial;
                    break;
                case Units.h:
                    result = UnitSystems.Time;
                    break;
                case Units.min:
                    result = UnitSystems.Time;
                    break;
                case Units.s:
                    result = UnitSystems.Time;
                    break;
                case Units.ms:
                    result = UnitSystems.Time;
                    break;
                default:
                    result = UnitSystems.None;
                    break;
            }

            return result;
        }

        /// <summary>
        /// Calculates the conversion multiplier needed to convert between two Units
        /// </summary>
        /// <param name="currentUnit">The starting unit</param>
        /// <param name="newUnit">The target unit</param>
        /// <returns>Multyplier as a double</returns>
        public static double GetUnitConversion(Units currentUnit, Units newUnit)
        {
            Quantities currentQuantity = currentUnit.GetQuantity();
            Quantities newQuantity = newUnit.GetQuantity();
            
            double conversion;

            if (currentQuantity == newQuantity)
            {
                // The units can be converted between

                UnitSystems currentSystem = currentUnit.GetSystem();
                UnitSystems newSystem = newUnit.GetSystem();

                if (currentSystem == newSystem)
                {
                    // Same system - convert from current unit to base to new unit
                    // new * 1/current
                    conversion = newUnit.GetBaseMultyplier() / currentUnit.GetBaseMultyplier();
                }
                else
                {
                    // Systems are different - convert to system base -> convert to new system -> convert to new unit

                    Units currentSystemBaseUnit = currentQuantity.GetSystemBaseUnit(currentSystem);
                    Units newSystemBaseUnit = newQuantity.GetSystemBaseUnit(newSystem);

                    conversion = GetUnitConversion(currentUnit, currentQuantity.GetSystemBaseUnit(currentSystem));

                    Dictionary<Units, double> conversions = currentQuantity.GetSystemConversions();

                    conversion *= conversions[newQuantity.GetSystemBaseUnit(newSystem)] / conversions[currentQuantity.GetSystemBaseUnit(currentSystem)];

                    conversion *= GetUnitConversion(newQuantity.GetSystemBaseUnit(newSystem), newUnit);
                }

                return conversion;
            }
            else
            {
                // The units refer to different quantities so can't be converted
                throw new ArgumentException("Unit conversion failed - the units provided are for different quantities and therfore can't be converted.");
            }
        }

        /// <summary>
        /// Gets the conversion multiplier applied to the current value needed to associate the value with a different unit
        /// </summary>
        /// <param name="currentUnit">The current units</param>
        /// <param name="newUnit">The units to convert to</param>
        /// <returns>A multiplier as a double. current * multiplier = new</returns>
        public static double GetUnitConversion(IGeneralUnit currentUnit, IGeneralUnit newUnit)
        {
            double conversion = 1;

            CompoundUnit currentCompound = new CompoundUnit(currentUnit);
            CompoundUnit newCompound = new CompoundUnit(newUnit);

            List<UnitPowerPair> currentValues = currentCompound.Values.OrderBy(new Func<UnitPowerPair, Quantities>((UnitPowerPair pair) => pair.Unit.GetQuantity())).ToList();
            List<UnitPowerPair> newValues = newCompound.Values.OrderBy(new Func<UnitPowerPair, Quantities>((UnitPowerPair pair) => pair.Unit.GetQuantity())).ToList();

            if (currentValues.Count == newValues.Count)
            {
                for (int i = 0; i < currentValues.Count; i++)
                {
                    if (currentValues[i].Power == newValues[i].Power)
                    {
                        conversion *= Math.Pow(GetUnitConversion(currentValues[i].Unit, newValues[i].Unit), currentValues[i].Power);
                    }
                    else
                    {
                        // The units have different powers and therfore aren't convertable
                        throw new ArgumentException("Unit conversion failed - the units provided had different powers so they don't represent the same physical quantity and therfore can't be converted.");
                    }
                }
            }
            else
            {
                // Pre convert all units to their system's base unit
                for (int i = 0; i < currentValues.Count; i++)
                {
                    Units preConvertedUnit = currentValues[i].Unit.GetQuantity().GetSystemBaseUnit(currentValues[i].Unit.GetSystem());
                    conversion *= Math.Pow(GetUnitConversion(currentValues[i].Unit, preConvertedUnit), currentValues[i].Power);

                    currentValues[i] = new UnitPowerPair { Unit = preConvertedUnit, Power = currentValues[i].Power };
                }

                for (int i = 0; i < newValues.Count; i++)
                {
                    Units preConvertedUnit = newValues[i].Unit.GetQuantity().GetSystemBaseUnit(newValues[i].Unit.GetSystem());
                    conversion *= Math.Pow(GetUnitConversion(newValues[i].Unit, preConvertedUnit), newValues[i].Power);

                    newValues[i] = new UnitPowerPair { Unit = preConvertedUnit, Power = newValues[i].Power };
                }

                conversion *= GetUnitConversion(new CompoundUnit(currentValues.ToArray()), new CompoundUnit(newValues.ToArray()));
            }

            return conversion;
        }
    }

    /// <summary>
    /// Physical quantitys that have units
    /// </summary>
    public enum Quantities
    {
        /// <summary>No assigned quantity</summary>
        None,

        /// <summary></summary>
        Angle,

        /// <summary></summary>
        Distance,

        /// <summary></summary>
        Mass,

        /// <summary></summary>
        Time
    }

    /// <summary>
    /// Extends the Quantities enum
    /// </summary>
    public static class QuantitiesMethods
    {
        /// <summary>
        /// Array of relitive size between base quantities in a given system. The system is at the index of its enum integer value
        /// </summary>
        private static Dictionary<Units, double>[] conversions = new Dictionary<Units, double>[]
            {
                // None
                new Dictionary<Units, double> { { Units.NoUnit, 1 } },
                // Angle
                new Dictionary<Units, double> { { Units.Degrees, 1 }, { Units.Radians, Math.PI/180 } },
                // Distance
                new Dictionary<Units, double> { { Units.m, 1 } },
                // Mass
                new Dictionary<Units, double> { { Units.Kg, 1 }, { Units.lb, 0.45359237 } },
                // Time
                new Dictionary<Units, double> { { Units.s, 1 } }
            };

        /// <summary>
        /// Gets the base unit for a quantity in a system
        /// </summary>
        /// <param name="quantity">The quantity</param>
        /// /// <param name="system">The unisystemt</param>
        /// <returns>The quantity's base unit in the system</returns>
        public static Units GetSystemBaseUnit(this Quantities quantity, UnitSystems system)
        {
            Units result;

            switch (quantity)
            {
                case Quantities.None:
                    switch (system)
                    {
                        case UnitSystems.None:
                            result = Units.NoUnit;
                            break;
                        default:
                            throw new ArgumentException("The quantity dosen't exist in the specified system.");
                    }
                    break;
                case Quantities.Angle:
                    switch (system)
                    {
                        case UnitSystems.Degrees:
                            result = Units.Degrees;
                            break;
                        case UnitSystems.Radians:
                            result = Units.Radians;
                            break;
                        default:
                            throw new ArgumentException("The quantity dosen't exist in the specified system.");
                    }
                    break;
                case Quantities.Distance:
                    switch (system)
                    {
                        case UnitSystems.SI:
                            result = Units.m;
                            break;
                        default:
                            throw new ArgumentException("The quantity dosen't exist in the specified system.");
                    }
                    break;
                case Quantities.Mass:
                    switch (system)
                    {
                        case UnitSystems.SI:
                            result = Units.Kg;
                            break;
                        case UnitSystems.Imperial:
                            result = Units.lb;
                            break;
                        default:
                            throw new ArgumentException("The quantity dosen't exist in the specified system.");
                    }
                    break;
                case Quantities.Time:
                    switch (system)
                    {
                        case UnitSystems.Time:
                            result = Units.s;
                            break;
                        default:
                            throw new ArgumentException("The quantity dosen't exist in the specified system.");
                    }
                    break;
                default:
                    throw new ArgumentException("The quantity dosen't exist.");
            }

            return result;
        }

        /// <summary>
        /// Gets a dictionary of relitive values for the base quantities in a unit system. The SI unit normaly takes a value of 1
        /// </summary>
        /// <param name="currentQuantity"></param>
        /// <returns></returns>
        public static Dictionary<Units, double> GetSystemConversions(this Quantities currentQuantity)
        {
            return conversions[(int)currentQuantity];
        }
    }

    /// <summary>
    /// The systems of mesurement with avalable units
    /// </summary>
    public enum UnitSystems
    {
        /// <summary>No present system</summary>
        None,

        /// <summary>SI or Metric</summary>
        SI,

        /// <summary></summary>
        Imperial,

        /// <summary></summary>
        Degrees,

        /// <summary></summary>
        Radians,

        /// <summary></summary>
        Time
    }
}
