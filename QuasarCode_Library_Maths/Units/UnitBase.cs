using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    public abstract class UnitBase : IUnit
    {
        public abstract FundamentalUnitPowerPair[] GetFundamentalUnitPairs();
        public abstract UnitPowerPair[] GetUnitPairs();
        public abstract IUnit Pow(int p);
        public abstract object Clone();

        public IUnit Mult(IUnit u)
        {
            List<UnitPowerPair>  items = new List<UnitPowerPair>(this.GetUnitPairs());
            items.AddRange(u.GetUnitPairs());
            return CompoundUnit.NewCompoundUnit(items.ToArray());
        }

        public IUnit Div(IUnit u)
        {
            List<UnitPowerPair> items = new List<UnitPowerPair>(this.GetUnitPairs());

            foreach (UnitPowerPair pair in u.GetUnitPairs())
            {
                UnitPowerPair newPair = new UnitPowerPair { Unit = pair.Unit, Power = -pair.Power };
                items.Add(newPair);
            }

            return CompoundUnit.NewCompoundUnit(items.ToArray());
        }

        public static IUnit operator *(UnitBase a, IUnit b)
        {
            return a.Mult(b);
        }

        public static IUnit operator /(UnitBase a, IUnit b)
        {
            return a.Div(b);
        }

        public override string ToString()
        {
            string result = "";

            foreach (FundamentalUnitPowerPair pair in GetFundamentalUnitPairs())
            {
                result += pair.Unit.ToString();
                foreach (char character in pair.Power.ToString())
                {
                    if (character == '-')
                    {
                        result += QuasarCode.Library.Tools.StringLiterals.Superscript_Minus;
                    }
                    else
                    {
                        result += Tools.StringLiterals.SuperscriptInt[Convert.ToInt32(character)];
                    }
                }

                result += " ";
            }

            return result.Trim();
        }
    }
}
