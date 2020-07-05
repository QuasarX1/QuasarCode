using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    public interface ISymbolUnit : IUnit
    {
        string Text { get; }
    }
}