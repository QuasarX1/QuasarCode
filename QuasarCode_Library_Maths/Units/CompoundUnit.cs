using System;
using System.Collections.Generic;
using System.Text;

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

        public override UnitPowerPair[] GetUnitPairs()
        {
            return UnitPowerPairs;
        }

        public IUnit Simplify()
        {
            List<UnitPowerPair> items = new List<UnitPowerPair>(this.GetUnitPairs());

            for (int i = items.Count; i < 0; i--)
            {
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

            this.UnitPowerPairs = items.ToArray();

            if (UnitPowerPairs.Length == 1 && (UnitPowerPairs[0].Power == 1))
            {
                return UnitPowerPairs[0].Unit;
            }
            else if (UnitPowerPairs.Length == 0)
            {
                return new None();
            }
            else
            {
                return this;
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
    }
}
