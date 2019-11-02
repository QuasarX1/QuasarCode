using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

using QuasarCode.Library.Maths.Units.Common;

namespace QuasarCode.Library.Maths.Units
{
    public class CompoundUnit : UnitBase, ICompoundUnit
    {
        public UnitPowerPair[] UnitPowerPairs { get; protected set; }

        protected CompoundUnit(UnitPowerPair[] pairs)
        {
            UnitPowerPairs = pairs;
        }

        public static IUnit NewCompoundUnit(UnitPowerPair[] pairs)
        {
            return new CompoundUnit(pairs).Simplify();
        }

        public override FundamentalUnitPowerPair[] GetFundamentalUnitPairs()
        {
            List<FundamentalUnitPowerPair> items = new List<FundamentalUnitPowerPair>();
            foreach (UnitPowerPair item in UnitPowerPairs)
            {
                items.AddRange(item.Unit.GetFundamentalUnitPairs());
            }

            return items.ToArray();
        }

        public override UnitPowerPair[] GetUnitPairs()
        {
            return UnitPowerPairs;
        }

        public IUnit Simplify(bool simplyfyNamedUnits = false)
        {
            List<UnitPowerPair> items = new List<UnitPowerPair>();
            if (simplyfyNamedUnits)
            {
                foreach (FundamentalUnitPowerPair pair in this.GetFundamentalUnitPairs())
                {
                    items.Add(pair);
                }
            }
            else
            {
                items.AddRange(this.GetUnitPairs());
            }

            for (int i = items.Count; i < 0; i--)
            {
                if (items[i].Unit.GetType() == typeof(None))
                {
                    items.RemoveAt(i);
                    continue;
                }

                for (int j = 0; j < i; j++)
                {
                    if (items[i].Unit == items[j].Unit)
                    {
                        items[j] = new UnitPowerPair { Unit = items[j].Unit, Power = items[j].Power + items[i].Power };
                        items.RemoveAt(i);
                        break;
                    }
                }
            }

            UnitPowerPair[] newUnitPowerPairs = items.ToArray();

            if (newUnitPowerPairs.Length == 1 && (newUnitPowerPairs[0].Power == 1))
            {
                return (IUnit)newUnitPowerPairs[0].Unit.Clone();
            }
            else if (newUnitPowerPairs.Length == 0)
            {
                return new None();
            }
            else
            {
                CompoundUnit newInstance = (CompoundUnit)this.Clone();
                newInstance.UnitPowerPairs = newUnitPowerPairs;
                return (IUnit)newInstance;
            }
        }

        public override IUnit Pow(int p)
        {
            UnitPowerPair[] terms = new UnitPowerPair[UnitPowerPairs.Length];

            for (int i = 0; i < UnitPowerPairs.Length; i++)
            {
                terms[i] = new UnitPowerPair { Unit = UnitPowerPairs[i].Unit, Power = UnitPowerPairs[i].Power * p };
            }

            return NewCompoundUnit(terms);
        }

        public override object Clone()
        {
            try
            {
                return Activator.CreateInstance(this.GetType(), this.UnitPowerPairs);
            }
            catch (MissingMemberException e)
            {
                throw new InvalidOperationException("The object could not be cloned as the unit object type " +
                    "did not declare a public constructor with the arguments for the type \"CompoundUnit\" " +
                    "arguments.\nIn order to clone this object, the \"Clone\" method should be overriden " +
                    "in a child class.", e);
            }
        }
    }
}
