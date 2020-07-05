using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

namespace QuasarCode.Library.Maths.Units
{
    /// <summary>
    /// A unit paired with a power
    /// </summary>
    public struct UnitPowerPair
    {
        /// <summary>
        /// The unit
        /// </summary>
        public ISymbolUnit Unit;

        /// <summary>
        /// The power
        /// </summary>
        public int Power;

        public FundamentalUnitPowerPair[] GetFundementals()
        {
            int currentPower = this.Power;// Needed as the LINQ statement needs a local variable

            return new List<FundamentalUnitPowerPair>(
                                                        from item
                                                        in Unit.GetFundamentalUnitPairs()
                                                        select new FundamentalUnitPowerPair { Unit = item.Unit, Power = item.Power * currentPower }
                                                      ).ToArray();
        }

        public static implicit operator FundamentalUnitPowerPair(UnitPowerPair instance)
        {
            return new UnitPowerPair { Unit = instance.Unit, Power = instance.Power };
        }

        public static explicit operator FundamentalUnitPowerPair[](UnitPowerPair instance)
        {
            return instance.GetFundementals();
        }

        public static bool operator ==(UnitPowerPair a, UnitPowerPair b)
        {
            FundamentalUnitPowerPair[] aFundementals = (FundamentalUnitPowerPair[])a;
            FundamentalUnitPowerPair[] bFundementals = (FundamentalUnitPowerPair[])b;

            if (aFundementals.Length != bFundementals.Length)
            {
                return false;
            }

            foreach (FundamentalUnitPowerPair pair in aFundementals)
            {
                for (int i = 0; i < bFundementals.Length; i++)
                {
                    if (pair == bFundementals[i])
                    {
                        bFundementals = (FundamentalUnitPowerPair[])bFundementals.TakeWhile(new Func<FundamentalUnitPowerPair, int, bool>((FundamentalUnitPowerPair item, int index) => index != i));
                        continue;
                    }
                    else
                    {
                        return false;
                    }
                }
            }

            return bFundementals.Length == 0;
        }

        public static bool operator !=(UnitPowerPair a, UnitPowerPair b)
        {
            return !(a == b);
        }

        
    }
}