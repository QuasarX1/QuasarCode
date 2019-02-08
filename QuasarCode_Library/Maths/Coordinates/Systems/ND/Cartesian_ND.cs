using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems.ND
{
    public class Cartesian_ND : ICartesianBase<Cartesian_ND>
    {
        public Dictionary<string, IGeneralUnit> Axes { get; }

        public int Dimentions { get; }


        public Cartesian_ND(params Units[] axisUnits)
        {
            Axes = new Dictionary<string, IGeneralUnit>();

            for (int i = 0; i < axisUnits.Length; i++)
            {
                Axes.Add(i.ToString(), (Unit)axisUnits[i]);
            }

            Dimentions = Axes.Count;
        }

        public Cartesian_ND(params IGeneralUnit[] axisUnits)
        {
            Axes = new Dictionary<string, IGeneralUnit>();

            for (int i = 0; i < axisUnits.Length; i++)
            {
                Axes.Add(i.ToString(), axisUnits[i]);
            }

            Dimentions = Axes.Count;
        }


        public event Func<ICoordinateSystem<Cartesian_ND>, ICoordinate<Cartesian_ND>[]> ReportPosition;
    }
}
