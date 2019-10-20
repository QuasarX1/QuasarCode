using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.old.Coordinates.Systems.ND
{
    /// <summary>
    /// Multi-dimantional cartesian coordinate system
    /// </summary>
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

        public ICoordinate<Cartesian_ND> GetCoordinate(params decimal[] ordinates)
        {
            if (ordinates.Length != this.Dimentions)
            {
                throw new ArgumentException("Coordinate creation failed - number of ordinates provided was inapropriate for the number of dimentions in the coordinate system.");
            }

            return new Coordinates.ND.Cartesian_ND_Coordinate(this, ordinates);
        }


        public event Func<ICoordinateSystem<Cartesian_ND>, ICoordinate<Cartesian_ND>[]> ReportPosition;
    }
}
