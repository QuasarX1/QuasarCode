using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    public class SystemConversion
    {
        public IQuantity ForQuantity { get; }

        public ISystem FromSystem { get; }

        public ISystem ToSystem { get; }

        private Func<double, double> conversionDeligate;

        public SystemConversion(IQuantity quantity, ISystem fromSystem, ISystem toSystem, Func<double, double> conversion)
        {
            this.ForQuantity = quantity;
            this.FromSystem = fromSystem;
            this.ToSystem = toSystem;
            conversionDeligate = conversion;
        }

        public double Convert(double value)
        {
            return this.conversionDeligate(value);
        }
    }
}