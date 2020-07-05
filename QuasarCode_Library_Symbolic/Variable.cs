using System;
using System.Collections.Generic;
using System.Text;
using System.Diagnostics;
using System.Linq;

namespace QuasarCode.Library.Symbolic
{
    /// <summary>
    /// Object representing a symbol with an equivalant expression which can be evaluated or displayed
    /// </summary>
    public sealed class Variable : Symbol
    {
        /// <summary>
        /// A list of symbolic operators and operands to be evaluated in order
        /// </summary>
        public List<Tuple<string, Symbol>> Operations { get; private set; }

        /// <summary>
        /// Boolean swich indicating whether or not the variable has been asigned an expression to evaluate
        /// </summary>
        public bool Initialised { get; private set; }

        /// <summary>
        /// The value associated with the symbol. This attempts to evaluate the variable's expression or overites it with a constant
        /// </summary>
        new public decimal Value {
            get
            {
                return this.Evaluate();
            }
            set
            {
                if (!Initialised)
                {
                    this.Initialise(value);
                }
                else
                {
                    Operations.Clear();
                    Operations.Add(new Tuple<string, Symbol>("", new Constant(value)));
                }
            }
        }
        /// <summary>
        /// Assignes the variable an expression taken from the provided symbol. Overites any current expression
        /// </summary>
        /// <param name="value">The variable or constant to set the variable's expression to</param>
        public void SetValue(Symbol value)
        {
            Operations.Clear();
            Operations = GetOperations(value);
            Initialised = true;
        }

        #region Constructors
        /// <summary>
        /// Creates an un-initialised variable with a symbol
        /// </summary>
        /// <param name="symbol"></param>
        public Variable(string symbol)
        {
            this.symbol = symbol;
            this.Operations = new List<Tuple<string, Symbol>>();
            Initialised = false;
        }

        /// <summary>
        /// Creates a variable and asigns it an initial value
        /// </summary>
        /// <param name="symbol"></param>
        /// <param name="initialValue"></param>
        public Variable(string symbol, decimal initialValue)
        {
            this.symbol = symbol;
            this.Operations = new List<Tuple<string, Symbol>>();
            this.Value = initialValue;
            this.Initialised = true;
        }

        /// <summary>
        /// Creates a variable and asigns it an initial value
        /// </summary>
        /// <param name="symbol"></param>
        /// <param name="initialValue"></param>
        private Variable(string symbol, Symbol initialValue)
        {
            this.symbol = symbol;
            if (initialValue is Variable && initialValue.symbol != null && GetOperations(initialValue).Count > 0)
            {
                this.Operations = GetOperations((Variable)initialValue);
            }
            else
            {
                this.Operations = new List<Tuple<string, Symbol>>();
                Operations.Add(new Tuple<string, Symbol>("", initialValue));
            }

            Initialised = true;
        }
        #endregion

        #region Initialisers
        /// <summary>
        /// Initialises an un-initialised variable with a starting value
        /// </summary>
        /// <param name="initialValue"></param>
        /// <returns></returns>
        public Variable Initialise(decimal initialValue)
        {
            if (!this.Initialised)
            {
                Initialised = true;
                Operations.Add(new Tuple<string, Symbol>("", new Constant(initialValue)));
                Initialised = true;
                return this;
            }
            else
            {
                throw new InvalidOperationException("Initialisation failed - the variable has allready been initialised with a value.");
            }
        }

        /// <summary>
        /// Initialises an un-initialised variable with a starting expression
        /// </summary>
        /// <param name="initialValue"></param>
        /// <returns></returns>
        public Variable Initialise(Symbol initialValue)
        {
            if (!this.Initialised)
            {
                if (initialValue is Variable && initialValue.symbol != null)
                {
                this.Operations = GetOperations((Variable)initialValue);
                }
                else
                {
                    this.Operations = new List<Tuple<string, Symbol>>();
                    Operations.Add(new Tuple<string, Symbol>("", initialValue));
                }

                Initialised = true;
                return this;
            }
            else
                {
                throw new InvalidOperationException("Initialisation failed - the variable has allready been initialised with a value.");
            }
        }
        #endregion

        /// <summary>
        /// Attempts to evaluate the expression to provide a value
        /// </summary>
        /// <returns></returns>
        public override decimal Evaluate()
        {
            decimal result = 0;
            if (this.Initialised)
            {
                foreach (Tuple<string, Symbol> operation in Operations)
                {
                    switch (operation.Item1)
                    {
                        //- Operators only found at the start of an object
                        case "":
                            result = operation.Item2.Evaluate();
                            break;
                        case "sqrt(":
                            result = (decimal)Math.Sqrt((double)operation.Item2.Evaluate());
                            break;
                        case "sin(":
                            result = (decimal)Math.Sin((double)operation.Item2.Evaluate());
                            break;
                        case "cos(":
                            result = (decimal)Math.Cos((double)operation.Item2.Evaluate());
                            break;
                        case "tan(":
                            result = (decimal)Math.Tan((double)operation.Item2.Evaluate());
                            break;
                        case "sin-1(":
                            result = (decimal)Math.Asin((double)operation.Item2.Evaluate());
                            break;
                        case "cos-1(":
                            result = (decimal)Math.Acos((double)operation.Item2.Evaluate());
                            break;
                        case "tan-1(":
                            result = (decimal)Math.Atan((double)operation.Item2.Evaluate());
                            break;
                        case "abs(":
                            result = (decimal)Math.Abs((double)operation.Item2.Evaluate());
                            break;
                        //- Binary operators
                        case "+":
                            result += operation.Item2.Evaluate();
                            break;
                        case "-":
                            result -= operation.Item2.Evaluate();
                            break;
                        case "*":
                            result *= operation.Item2.Evaluate();
                            break;
                        case "/":
                            result /= operation.Item2.Evaluate();
                            break;
                        case "^":
                            result = (decimal)Math.Pow((double)result, (double)operation.Item2.Evaluate());
                            break;
                        //- Operators only found at the end of an object
                        case ")":
                            break;
                        default:
                            break;
                    }
                }

                return result;
            }
            else
            {
                throw new InvalidOperationException("Evaluation failed - the variable has not yet been initialised with a value.");
            }
            
        }

        /// <summary>
        /// Gets a string containing the components that produce the value
        /// </summary>
        /// <param name="expantionDepth">The number of symbol layers to expand before just quoting symbols</param>
        /// <returns></returns>
        public override string GetComponentString(int expantionDepth = 1)
        {
            string result = "";

            if (expantionDepth > 0 && Operations.Count > 0 && !(Operations.Count == 1 && Operations[0].Item2 is Constant && Operations[0].Item2.symbol == null))
            {
                foreach (Tuple<string, Symbol> operation in Operations)
                {
                    switch (operation.Item1)
                    {
                        case "":
                            result = operation.Item2.GetComponentString(expantionDepth - 1);
                            break;
                        case "sqrt(":
                            result = operation.Item1 + " " + operation.Item2.GetComponentString(expantionDepth - 1);
                            break;
                        case "sin(":
                            result = operation.Item1 + " " + operation.Item2.GetComponentString(expantionDepth - 1);
                            break;
                        case "cos(":
                            result = operation.Item1 + " " + operation.Item2.GetComponentString(expantionDepth - 1);
                            break;
                        case "tan(":
                            result = operation.Item1 + " " + operation.Item2.GetComponentString(expantionDepth - 1);
                            break;
                        case "sin-1(":
                            result = operation.Item1 + " " + operation.Item2.GetComponentString(expantionDepth - 1);
                            break;
                        case "cos-1(":
                            result = operation.Item1 + " " + operation.Item2.GetComponentString(expantionDepth - 1);
                            break;
                        case "tan-1(":
                            result = operation.Item1 + " " + operation.Item2.GetComponentString(expantionDepth - 1);
                            break;
                        case "abs(":
                            result = operation.Item1 + " " + operation.Item2.GetComponentString(expantionDepth - 1);
                            break;
                        case ")":
                            result += " )";
                            break;
                        default:
                            result += " " + operation.Item1 + " " + operation.Item2.GetComponentString(expantionDepth - 1);
                            break;
                    }
                }
            }
            else
            {
                if (this.symbol != null)
                {
                    return this.symbol;
                }
                else
                {
                    return this.GetComponentString(expantionDepth + 1);
                }
            }

            return result;
        }

        /// <summary>
        /// Constructs an algebraic equasion as a string representing the variable and its expression
        /// </summary>
        /// <param name="expantionDepth">The number of symbol layers to expand before just quoting symbols</param>
        /// <returns></returns>
        public string GetEquasionString(int expantionDepth = 1)
        {
            if (this.symbol != null)
            {
                return this.symbol + " = " + GetComponentString(expantionDepth);
            }
            else
            {
                return GetComponentString(expantionDepth);
            }
        }

        public override string ToString()
        {
            return this.GetComponentString();
        }

        /// <summary>
        /// Returns the contence of a symbol in the format of a variable's operations list
        /// </summary>
        /// <param name="s"></param>
        /// <returns></returns>
        private static List<Tuple<string, Symbol>> GetOperations(Symbol s)
        {
            if (s is Variable)
            {
                return ((Variable)s).Operations;
            }
            else
            {
                return new List<Tuple<string, Symbol>>() { new Tuple<string, Symbol>("", s) };
            }
        }

        public bool ContainsSymbol(Symbol target)
        {
            return (from operation in this.Operations select operation.Item2.GetType() == typeof(Variable) && ((Variable)operation.Item2).ContainsSymbol(target)).Sum((bool result) => { return (result) ? 1 : 0; }) > 0;
        }

        public bool[] OperationsContainingSymbol(Symbol target)
        {
            return (from operation in this.Operations select operation.Item2.GetType() == typeof(Variable) && ((Variable)operation.Item2).ContainsSymbol(target)).ToArray();
        }

        public void SimplifyAndExpandTerms()
        {
            decimal valueTotal = 0;
            for (int i = 0; i < this.Operations.Count; i++)
            {
                try
                {
                    valueTotal += this.Operations[i].Item2.Evaluate();
                    //TODO: THIS WON'T WORK - the whole approach is flawed!
                }
                catch (InvalidOperationException)
                {

                    throw;
                }
            }
        }

        #region Operators
        /// <summary>
        /// Adds two variables
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator +(Variable a, Variable b)
        {
            if (a.symbol == null)
            {
                a.Add(b);
                return a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Add(b);
                return shell;
            }
        }
        /// <summary>
        /// Ads a variable and a symbol
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator +(Variable a, Symbol b)
        {
            if (a.symbol == null)
            {
                a.Add(b);
                return a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Add(b);
                return shell;
            }
        }
        /// <summary>
        /// Adds a symbol and a variable
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator +(Symbol a, Variable b)
        {
            if (a.symbol == null && a is Variable)
            {
                ((Variable)a).Add(b);
                return (Variable)a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Add(b);
                return shell;
            }
        }
        /// <summary>
        /// Adds a variable and a constant produced from a number
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator +(Variable a, decimal b)
        {
            if (a.symbol == null)
            {
                a.Add(new Constant(b));
                return a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Add(new Constant(b));
                return shell;
            }
        }
        /// <summary>
        /// Adds a onstant produced from a number and a variable
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator +(decimal a, Variable b)
        {
            Variable shell = new Variable(null, a);
            shell.Add(b);
            return shell;
        }

        /// <summary>
        /// Adds a symbol to the variable
        /// </summary>
        /// <param name="a"></param>
        private void Add(Symbol a)
        {
            this.Operations.Add(new Tuple<string, Symbol>("+", a));
        }


        /// <summary>
        /// Subtracts one variable from another
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator -(Variable a, Variable b)
        {
            if (a.symbol == null)
            {
                a.Subtract(b);
                return a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Subtract(b);
                return shell;
            }
        }
        /// <summary>
        /// Subtracts a symbol from a variable
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator -(Variable a, Symbol b)
        {
            if (a.symbol == null)
            {
                a.Subtract(b);
                return a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Subtract(b);
                return shell;
            }
        }
        /// <summary>
        /// Subtracts a variable from a symbol
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator -(Symbol a, Variable b)
        {
            if (a.symbol == null && a is Variable)
            {
                ((Variable)a).Add(b);
                return (Variable)a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Add(b);
                return shell;
            }
        }
        /// <summary>
        /// Subtracts a constant produced from a number from a variable
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator -(Variable a, decimal b)
        {
            if (a.symbol == null)
            {
                a.Subtract(new Constant(b));
                return a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Subtract(new Constant(b));
                return shell;
            }
        }
        /// <summary>
        /// Subtracts a variable from a constant produced from a number
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator -(decimal a, Variable b)
        {
            Variable shell = new Variable(null, a);
            shell.Subtract(b);
            return shell;
        }

        /// <summary>
        /// Subtracts a symbol from the variable
        /// </summary>
        /// <param name="a"></param>
        private void Subtract(Symbol a)
        {
            this.Operations.Add(new Tuple<string, Symbol>("-", a));
        }


        /// <summary>
        /// Multiplies a variable by another
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator *(Variable a, Variable b)
        {
            if (a.symbol == null)
            {
                a.Multyply(b);
                return a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Multyply(b);
                return shell;
            }
        }
        /// <summary>
        /// Multiplies a variable by a symbol
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator *(Variable a, Symbol b)
        {
            if (a.symbol == null)
            {
                a.Multyply(b);
                return a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Multyply(b);
                return shell;
            }
        }
        /// <summary>
        /// Multiplies a symbol by a variable
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator *(Symbol a, Variable b)
        {
            if (a.symbol == null && a is Variable)
            {
                ((Variable)a).Multyply(b);
                return (Variable)a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Multyply(b);
                return shell;
            }
        }
        /// <summary>
        /// Multiplies a variable by a constant produced from a number
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator *(Variable a, decimal b)
        {
            if (a.symbol == null)
            {
                a.Multyply(new Constant(b));
                return a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Multyply(new Constant(b));
                return shell;
            }
        }
        /// <summary>
        /// Multiplies a constant produced from a number by a variable
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator *(decimal a, Variable b)
        {
            Variable shell = new Variable(null, a);
            shell.Multyply(b);
            return shell;
        }

        /// <summary>
        /// Multiplies the variable by a symbol
        /// </summary>
        /// <param name="a"></param>
        private void Multyply(Symbol a)
        {
            this.Operations.Add(new Tuple<string, Symbol>("*", a));
        }


        /// <summary>
        /// Divides a variable by another
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator /(Variable a, Variable b)
        {
            if (a.symbol == null)
            {
                a.Divide(b);
                return a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Divide(b);
                return shell;
            }
        }
        /// <summary>
        /// Divides a variable by a symbol
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator /(Variable a, Symbol b)
        {
            if (a.symbol == null)
            {
                a.Divide(b);
                return a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Divide(b);
                return shell;
            }
        }
        /// <summary>
        /// Divides a symbol by a variable
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator /(Symbol a, Variable b)
        {
            if (a.symbol == null && a is Variable)
            {
                ((Variable)a).Divide(b);
                return (Variable)a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Divide(b);
                return shell;
            }
        }
        /// <summary>
        /// Divides a variable by a constant produced from a number
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator /(Variable a, decimal b)
        {
            if (a.symbol == null)
            {
                a.Divide(new Constant(b));
                return a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Divide(new Constant(b));
                return shell;
            }
        }
        /// <summary>
        /// Divides a constant produced from a number by a variable
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator /(decimal a, Variable b)
        {
            Variable shell = new Variable(null, a);
            shell.Divide(b);
            return shell;
        }

        /// <summary>
        /// Divides the variable by a symbol
        /// </summary>
        /// <param name="a"></param>
        private void Divide(Symbol a)
        {
            this.Operations.Add(new Tuple<string, Symbol>("/", a));
        }


        /// <summary>
        /// Raises one variable to the power of another
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator ^(Variable a, Variable b)
        {
            if (a.symbol == null)
            {
                a.Pow(b);
                return a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Pow(b);
                return shell;
            }
        }
        /// <summary>
        /// Raises a variable to the power of a symbol
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator ^(Variable a, Symbol b)
        {
            if (a.symbol == null)
            {
                a.Pow(b);
                return a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Pow(b);
                return shell;
            }
        }
        /// <summary>
        /// Raises a symbol to the power of a variable
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator ^(Symbol a, Variable b)
        {
            if (a.symbol == null && a is Variable)
            {
                ((Variable)a).Pow(b);
                return (Variable)a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Pow(b);
                return shell;
            }
        }
        /// <summary>
        /// Raises a variable to the power of a constant produced from a number
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator ^(Variable a, decimal b)
        {
            if (a.symbol == null)
            {
                a.Pow(new Constant(b));
                return a;
            }
            else
            {
                Variable shell = new Variable(null, a);
                shell.Pow(new Constant(b));
                return shell;
            }
        }
        /// <summary>
        /// Raises a constant produced from a number to the power of a variable
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static Variable operator ^(decimal a, Variable b)
        {
            Variable shell = new Variable(null, a);
            shell.Pow(b);
            return shell;
        }

        /// <summary>
        /// Raises the variable to the power of a symbol
        /// </summary>
        /// <param name="a"></param>
        private void Pow(Symbol a)
        {
            this.Operations.Add(new Tuple<string, Symbol>("^", a));
        }


        /// <summary>
        /// Square roots a variable
        /// </summary>
        /// <param name="a"></param>
        /// <returns></returns>
        public static Variable sqrt(Variable a)
        {
            if (a.symbol == null)
            {
                a.sqrt();
                return a;
            }
            else
            {
                Variable result = new Variable(null);
                result.Initialised = true;

                result.Operations.Add(new Tuple<string, Symbol>("sqrt(", a));
                result.Operations.Add(new Tuple<string, Symbol>(")", null));

                return result;
            }
        }
        /// <summary>
        /// Square roots a symbol
        /// </summary>
        /// <param name="a"></param>
        /// <returns></returns>
        public static Variable sqrt(Symbol a)
        {
            if (a.symbol == null && a is Variable)
            {
                ((Variable)a).sqrt();
                return (Variable)a;
            }
            else
            {
                Variable result = new Variable(null);
                result.Initialised = true;

                result.Operations.Add(new Tuple<string, Symbol>("sqrt(", a));
                result.Operations.Add(new Tuple<string, Symbol>(")", null));

                return result;
            }
        }
        /// <summary>
        /// Square roots a constant produced from a number
        /// </summary>
        /// <param name="a"></param>
        /// <returns></returns>
        public static Variable sqrt(decimal a)
        {
            return new Variable(null, (decimal)Math.Sqrt((double)a));
        }

        /// <summary>
        /// Square roots the variable
        /// </summary>
        public void sqrt()
        {
            Variable inside = new Variable(null);
            inside.Initialised = true;
            inside.Operations = this.Operations;
            this.Operations = new List<Tuple<string, Symbol>>() { new Tuple<string, Symbol>("sqrt(", inside) };
            Operations.Add(new Tuple<string, Symbol>(")", null));
        }


        /// <summary>
        /// Applies the sin function to a variable
        /// </summary>
        /// <param name="a"></param>
        /// <returns></returns>
        public static Variable sin(Variable a)
        {
            if (a.symbol == null)
            {
                a.sin();
                return a;
            }
            else
            {
                Variable result = new Variable(null);
                result.Initialised = true;

                result.Operations.Add(new Tuple<string, Symbol>("sin(", a));
                result.Operations.Add(new Tuple<string, Symbol>(")", null));

                return result;
            }
        }
        /// <summary>
        /// Applies the sin function to a symbol
        /// </summary>
        /// <param name="a"></param>
        /// <returns></returns>
        public static Variable sin(Symbol a)
        {
            if (a.symbol == null && a is Variable)
            {
                ((Variable)a).sin();
                return (Variable)a;
            }
            else
            {
                Variable result = new Variable(null);
                result.Initialised = true;

                result.Operations.Add(new Tuple<string, Symbol>("sin(", a));
                result.Operations.Add(new Tuple<string, Symbol>(")", null));

                return result;
            }
        }
        /// <summary>
        /// Applies the sin function to a constant produced from a number
        /// </summary>
        /// <param name="a"></param>
        /// <returns></returns>
        public static Variable sin(decimal a)
        {
            return new Variable(null, (decimal)Math.Sin((double)a));
        }

        /// <summary>
        /// Applies the sin function to the variable
        /// </summary>
        public void sin()
        {
            Variable inside = new Variable(null);
            inside.Initialised = true;
            inside.Operations = this.Operations;
            this.Operations = new List<Tuple<string, Symbol>>() { new Tuple<string, Symbol>("sin(", inside) };
            Operations.Add(new Tuple<string, Symbol>(")", null));
        }


        /// <summary>
        /// Applies the cosine function to a variable
        /// </summary>
        /// <param name="a"></param>
        /// <returns></returns>
        public static Variable cos(Variable a)
        {
            if (a.symbol == null)
            {
                a.cos();
                return a;
            }
            else
            {
                Variable result = new Variable(null);
                result.Initialised = true;

                result.Operations.Add(new Tuple<string, Symbol>("cos(", a));
                result.Operations.Add(new Tuple<string, Symbol>(")", null));

                return result;
            }
        }
        /// <summary>
        /// Applies the cosin function to a symbol
        /// </summary>
        /// <param name="a"></param>
        /// <returns></returns>
        public static Variable cos(Symbol a)
        {
            if (a.symbol == null && a is Variable)
            {
                ((Variable)a).cos();
                return (Variable)a;
            }
            else
            {
                Variable result = new Variable(null);
                result.Initialised = true;

                result.Operations.Add(new Tuple<string, Symbol>("cos(", a));
                result.Operations.Add(new Tuple<string, Symbol>(")", null));

                return result;
            }
        }
        /// <summary>
        /// Applies the cosin function to a constant produced from a number
        /// </summary>
        /// <param name="a"></param>
        /// <returns></returns>
        public static Variable cos(decimal a)
        {
            return new Variable(null, (decimal)Math.Cos((double)a));
        }

        /// <summary>
        /// Applies the cosin function to the variable
        /// </summary>
        public void cos()
        {
            Variable inside = new Variable(null);
            inside.Initialised = true;
            inside.Operations = this.Operations;
            this.Operations = new List<Tuple<string, Symbol>>() { new Tuple<string, Symbol>("sqrt(", inside) };
            Operations.Add(new Tuple<string, Symbol>(")", null));
        }


        /// <summary>
        /// Applies the tangent function to a variable
        /// </summary>
        /// <param name="a"></param>
        /// <returns></returns>
        public static Variable tan(Variable a)
        {
            if (a.symbol == null)
            {
                a.tan();
                return a;
            }
            else
            {
                Variable result = new Variable(null);
                result.Initialised = true;

                result.Operations.Add(new Tuple<string, Symbol>("tan(", a));
                result.Operations.Add(new Tuple<string, Symbol>(")", null));

                return result;
            }
        }
        /// <summary>
        /// Applies the tangent function to a symbol
        /// </summary>
        /// <param name="a"></param>
        /// <returns></returns>
        public static Variable tan(Symbol a)
        {
            if (a.symbol == null && a is Variable)
            {
                ((Variable)a).tan();
                return (Variable)a;
            }
            else
            {
                Variable result = new Variable(null);
                result.Initialised = true;

                result.Operations.Add(new Tuple<string, Symbol>("tan(", a));
                result.Operations.Add(new Tuple<string, Symbol>(")", null));

                return result;
            }
        }
        /// <summary>
        /// Applies the tangent function to a constant produced from a number
        /// </summary>
        /// <param name="a"></param>
        /// <returns></returns>
        public static Variable tan(decimal a)
        {
            return new Variable(null, (decimal)Math.Tan((double)a));
        }

        /// <summary>
        /// Applies the tangent function to the variable
        /// </summary>
        public void tan()
        {
            Variable inside = new Variable(null);
            inside.Initialised = true;
            inside.Operations = this.Operations;
            this.Operations = new List<Tuple<string, Symbol>>() { new Tuple<string, Symbol>("tan(", inside) };
            Operations.Add(new Tuple<string, Symbol>(")", null));
        }


        /// <summary>
        /// Makes value of a variable positive
        /// </summary>
        /// <param name="a"></param>
        /// <returns></returns>
        public static Variable abs(Variable a)
        {
            if (a.symbol == null)
            {
                a.abs();
                return a;
            }
            else
            {
                Variable result = new Variable(null);
                result.Initialised = true;

                result.Operations.Add(new Tuple<string, Symbol>("abs(", a));
                result.Operations.Add(new Tuple<string, Symbol>(")", null));

                return result;
            }
        }
        /// <summary>
        /// Makes value of a symbol positive
        /// </summary>
        /// <param name="a"></param>
        /// <returns></returns>
        public static Variable abs(Symbol a)
        {
            if (a.symbol == null && a is Variable)
            {
                ((Variable)a).abs();
                return (Variable)a;
            }
            else
            {
                Variable result = new Variable(null);
                result.Initialised = true;

                result.Operations.Add(new Tuple<string, Symbol>("abs(", a));
                result.Operations.Add(new Tuple<string, Symbol>(")", null));

                return result;
            }
        }
        /// <summary>
        /// Makes value of a constant produced from a number positive
        /// </summary>
        /// <param name="a"></param>
        /// <returns></returns>
        public static Variable abs(decimal a)
        {
            return new Variable(null, (decimal)Math.Abs((double)a));
        }

        /// <summary>
        /// Makes value of the variable positive
        /// </summary>
        public void abs()
        {
            Variable inside = new Variable(null);
            inside.Initialised = true;
            inside.Operations = this.Operations;
            this.Operations = new List<Tuple<string, Symbol>>() { new Tuple<string, Symbol>("abs(", inside) };
            Operations.Add(new Tuple<string, Symbol>(")", null));
        }
        #endregion

        public static implicit operator Variable(decimal value)
        {
            return new Variable(null, value);
        }
    }
}