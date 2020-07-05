using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

namespace QuasarCode.Library.Symbolic
{
    public class Equasion
    {
        public Variable LHS { get; set; }
        public Variable RHS { get; set; }

        public Equasion(Variable LHS, Variable RHS)
        {
            this.LHS = LHS;
            this.RHS = RHS;
        }

        public void SolveFor(Variable target)
        {
            throw new NotImplementedException("This method does not yet work.");
            Variable value = 0;

            Variable equasionVariable = LHS - RHS;

            while (!target.Initialised)
            {
                bool[] locations = equasionVariable.OperationsContainingSymbol(target);

                for (int i = 0; i < equasionVariable.Operations.Count; i++)
                {
                    if (!locations[i])
                    {
                        //TODO: work out inverse operation (swich statement? declare in Symbol?) and move
                    }

                    //TODO: expand all 1sh layer terms of remaining variables into one variable
                    //equasionVariable = ;
                }
            }
        }

        public static Dictionary<string, Variable> CreateVariables(string[] symbols, decimal[] values)
        {
            return symbols.Zip(values, (string symbol, decimal value) => { return new Variable(symbol, value); }).ToDictionary((Variable item) => { return item.symbol; });
        }

        public override string ToString()
        {
            return LHS.ToString() + " = " + LHS.ToString();
        }
    }
}
