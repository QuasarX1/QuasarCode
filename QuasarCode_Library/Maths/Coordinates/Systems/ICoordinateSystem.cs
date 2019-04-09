using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Coordinates.Systems
{
    /// <summary>
    /// A Coordinate System
    /// </summary>
    public interface ICoordinateSystem
    {
        /// <summary>
        /// Dictionary of units asociated with each axis
        /// </summary>
        Dictionary<string, IGeneralUnit> Axes { get; }

        /// <summary>
        /// The total number of dimentions in the system
        /// </summary>
        int Dimentions { get; }
    }

    /// <summary>
    /// A Coordinate System
    /// </summary>
    /// <typeparam name="T">Type of coordinate system</typeparam>
    public interface ICoordinateSystem<T> : ICoordinateSystem where T : ICoordinateSystem<T>
    {
        /// <summary>
        /// Creates a coordinate of the type that belongs to the coordinate system type
        /// </summary>
        /// <param name="ordinates">The ordinates that make up the coordinate</param>
        /// <returns></returns>
        ICoordinate<T> GetCoordinate(params decimal[] ordinates);

        /// <summary>
        /// Asks all subscribers to return their current position in the coordinate system
        /// </summary>
        event Func<ICoordinateSystem<T>, ICoordinate<T>[]> ReportPosition;
    }
}
