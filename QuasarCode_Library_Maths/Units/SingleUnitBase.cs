using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    public abstract class SingleUnitBase : UnitBase, ISingleUnit
    {
        public Quantities Quantity { get; protected set; }
        public Systems System { get; protected set; }
        public double SystemBaseMultyplier { get; protected set; }
        public string Text { get; protected set; }

        protected SingleUnitBase(Quantities quantity, Systems system, double systemBaseMultyplier, string text)
        {
            this.Quantity = quantity;
            this.System = system;
            this.SystemBaseMultyplier = systemBaseMultyplier;
            this.Text = text;
        }

        public override UnitPowerPair[] GetUnitPairs()
        {
            return new UnitPowerPair[] { new UnitPowerPair { Unit = this, Power = 1 } };
        }

        public override IUnit Pow(int p)
        {
            return CompoundUnit.NewCompoundUnit(new UnitPowerPair[] { new UnitPowerPair { Unit = this, Power = p } });
        }

        public override string ToString()
        {
            return Text;
        }
    }
}
