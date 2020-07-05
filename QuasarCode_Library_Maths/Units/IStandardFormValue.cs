using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    public interface IStandardFormValue : IValue
    {
        double StandardMagnitude { get; }
        int StandardPower { get; }
    }
}