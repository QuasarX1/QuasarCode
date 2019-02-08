﻿using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates.Systems;
using QuasarCode.Library.Maths.Coordinates.Systems.ND;


namespace QuasarCode.Library.Maths.Coordinates.ND
{
    public class Cartesian_ND_Coordinate : ICoordinate<Cartesian_ND>
    {
        public ICoordinateSystem<Cartesian_ND> System { get; }

        public decimal[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public Cartesian_ND_Coordinate(ICoordinateSystem<Cartesian_ND> coordinateSystem, params decimal[] ordinates)
        {
            System = coordinateSystem;

            Ordinates = ordinates;
        }

        public Matrices.Vectors.IVector GetVector()
        {
            return new Matrices.Vectors.CartesianVector<Cartesian_ND>(Ordinates);
        }
    }
}
