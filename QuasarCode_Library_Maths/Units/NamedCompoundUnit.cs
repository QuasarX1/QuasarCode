using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    public class NamedCompoundUnit : CompoundUnit, INamedCompoundUnit
    {
        public string Text { get; protected set; }

        public NamedCompoundUnit(string text, UnitPowerPair[] pairs) : base(pairs)
        {
            this.Text = text;
        }

        public override UnitPowerPair[] GetUnitPairs()
        {
            return new UnitPowerPair[] { new UnitPowerPair { Unit = this, Power = 1 } };
        }

        public override string ToString()
        {
            return Text;
        }

        public override object Clone()
        {
            try
            {
                return Activator.CreateInstance(this.GetType(), this.Text, this.UnitPowerPairs);
            }
            catch (MissingMemberException e)
            {
                throw new InvalidOperationException("The object could not be cloned as the unit object type " +
                    "did not declare a public constructor with the arguments for the type \"NamedCompoundUnit\" " +
                    "arguments.\nIn order to clone this object, the \"Clone\" method should be overriden " +
                    "in a child class.", e);
            }
        }
    }
}
