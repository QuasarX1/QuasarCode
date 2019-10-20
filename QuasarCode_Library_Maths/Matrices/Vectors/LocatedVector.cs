using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

namespace QuasarCode.Library.Maths.Matrices.Vectors
{
    //public class LocatedVector<T> : ILocatedVector<T>, IVector<T> where T : Coordinates.Systems.ICoordinateSystem<T>
    //{
    //    protected IVector UnderlyingVector;

    //    public double[] ComponentArray { get { return UnderlyingVector.ComponentArray; } }

    //    public double Magnitude { get { return UnderlyingVector.Magnitude; } set { UnderlyingVector.Magnitude = value; }  }

    //    public Coordinates.ICoordinate<T> Location { get; }

    //    public LocatedVector(Coordinates.ICoordinate<T> location)
    //    {
    //        Location = location;
    //    }

    //    new public string ToString()
    //    {
    //        string[] components = UnderlyingVector.GetComponentStrings();

    //        string result = "";

    //        for (int i = 0; i < Components.Length; i++)
    //        {
    //            if (Components[i] != 0)
    //            {
    //                result += components[i] + " " + Location.System.Axes.ElementAt(i).Value.ToString() + ", ";
    //            }
    //        }

    //        result = result.Remove(result.Length - 2);

    //        return result;
    //    }

    //    public string[] GetComponentStrings()
    //    {
    //        string[] components = UnderlyingVector.GetComponentStrings();

    //        for (int i = 0; i < Components.Length; i++)
    //        {
    //            if (Components[i] != 0)
    //            {
    //                components[i] += components[i] + " " + Location.System.Axes.ElementAt(i).Value.ToString();
    //            }
    //        }

    //        return components;
    //    }
    //}
}
