from abc import abstractmethod
from decimal import Decimal
import math
from typing import Iterable, TypeVar, Generic

import numpy as np

from ._Rect import IRect, GenericRect, Rect, DiscreteRect

T = TypeVar("T")
class IRect3D(Generic[T]):
    """
    Interface for a 3D rectangle (cuboid) type.

    Use the following static classmethods on an implementation to create an instance:
        - create_from_size(x, y, z, width, height, depth)
        - create_from_centre(x, y, z, width, height, depth)
        - create_from_limits(x_min, x_max, y_min, y_max, z_min, z_max)
    """

    @classmethod
    @abstractmethod
    def create_from_size(cls, x: T, y: T, z: T, width: T, height: T, depth: T) -> "IRect3D[T]":
        """
        Creates an IRect3D instance using the specified position of the bottom-left-near corner and size.

        Parameters:
            T x:
                The x-coordinate of the bottom-left corner of the near plane.
            T y:
                The y-coordinate of the bottom-left corner of the near plane.
            T z:
                The z-coordinate of the near plane.
            T width:
                The width of the X-Y plane.
            T height:
                The height of the X-Y plane.
            T depth:
                The depth of the far plane from the near plane.

        Returns:
            IRect3D[T] -> A new IRect3D instance defined by the given position and size.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @classmethod
    @abstractmethod
    def create_from_centre(cls, x: T, y: T, z: T, width: T, height: T, depth: T) -> "IRect3D[T]":
        """
        Create a IRect3D instance using the centre coordinates and dimensions.

        Parameters:
            T x:
                The x-coordinate of the centre of the volume.
            T y:
                The y-coordinate of the centre of the volume.
            T z:
                The z-coordinate of the centre of the volume.
            T width:
                The width of the X-Y plane.
            T height:
                The height of the X-Y plane.
            T depth:
                The depth of the far plane from the near plane.

        Returns:
            IRect3D[T] -> Instance centred on (x, y, z) with the specified width, height, and depth.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @classmethod
    @abstractmethod
    def create_from_limits(cls, x_min: T, x_max: T, y_min: T, y_max: T, z_min: T, z_max: T) -> "IRect3D[T]":
        """
        Create a IRect3D instance from the specified boundary limits.
        This is the same as the constructor parameters and is implemented for consistency.

        Parameters:
            T x_min:
                The minimum x-coordinate of the rectangle.
            T x_max:
                The maximum x-coordinate of the rectangle.
            T y_min:
                The minimum y-coordinate of the rectangle.
            T y_max:
                The maximum y-coordinate of the rectangle.
            T z_min:
                The minimum z-coordinate of the rectangle.
            T z_max:
                The maximum z-coordinate of the rectangle.

        Returns:
            IRect3D[T] -> A new instance of the Rect3D class defined by the given limits.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @classmethod
    @abstractmethod
    def create_from_data(cls, x_data: Iterable[T], y_data: Iterable[T], z_data: Iterable[T]) -> "IRect3D[T]":
        """
        Create a IRect3D instance that encompasses the provided data.

        Parameters:
            Iterable[T] x_data:
                X-coordinates.
            Iterable[T] y_data:
                Y-coordinates.
            Iterable[T] z_data:
                Z-coordinates.

        Returns:
            IRect3D[T] -> A new instance of the Rect3D class that encompasses the data.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def x(self) -> T:
        """
        The x-coordinate of the bottom-left corner of the X-Y plane.

        Returns:
            T -> The x-coordinate of the X-Y plane's bottom-left corner.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @x.setter
    @abstractmethod
    def _(self, value: T) -> None:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def y(self) -> T:
        """
        The y-coordinate of the bottom-left corner of the X-Y plane.

        Returns:
            T -> The y-coordinate of the X-Y plane's bottom-left corner.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @y.setter
    @abstractmethod
    def _(self, value: T) -> None:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def z(self) -> T:
        """
        The z-coordinate of the near plane.

        Returns:
            T -> The z-coordinate of the near plane.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @z.setter
    @abstractmethod
    def _(self, value: T) -> None:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def x1(self) -> T:
        """
        The x-coordinate of the top-right corner of the X-Y plane.

        Returns:
            T -> The x-coordinate of the X-Y plane's top-right corner.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @x1.setter
    @abstractmethod
    def _(self, value: T) -> None:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def y1(self) -> T:
        """
        The y-coordinate of the top-right corner of the X-Y plane.

        Returns:
            T -> The y-coordinate of the X-Y plane's top-right corner.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @y1.setter
    @abstractmethod
    def _(self, value: T) -> None:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def z1(self) -> T:
        """
        The z-coordinate of the far plane.

        Returns:
            T -> The z-coordinate of the far plane.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @z1.setter
    @abstractmethod
    def _(self, value: T) -> None:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def range(self) -> tuple[tuple[T, T], tuple[T, T], tuple[T, T]]:
        """
        The limits of the cuboid in the form ((x_min, x_max), (y_min, y_max), (z_min, z_max)).
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def width(self) -> T:
        """
        The width of the X-Y plane.

        Returns:
            T -> The width of the X-Y plane.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def height(self) -> T:
        """
        The height of the X-Y plane.

        Returns:
            T -> The height of the X-Y plane.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def depth(self) -> T:
        """
        The depth between the far to near planes.

        Returns:
            T -> The depth between the far to near planes.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def centre(self) -> tuple[T, T, T]:
        """
        The coordinates of the center of the cuboid.

        Returns:
            tuple[T, T, T] -> (x, y, z)
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def volume(self) -> T:
        """
        The volume of the cuboid.

        Returns:
            T -> The volume of the cuboid.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def plane_x_y(self) -> IRect[T]:
        """
        The X-Y plane of the cuboid (normal vector pointing in the Z direction).
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def plane_y_x(self) -> IRect[T]:
        """
        The Y-X plane of the cuboid (normal vector pointing in the -Z direction).
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def plane_x_z(self) -> IRect[T]:
        """
        The X-Z plane of the cuboid (normal vector pointing in the Y direction).
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def plane_z_x(self) -> IRect[T]:
        """
        The Z-X plane of the cuboid (normal vector pointing in the -Y direction).
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def plane_y_z(self) -> IRect[T]:
        """
        The Y-Z plane of the cuboid (normal vector pointing in the -X direction).
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    @abstractmethod
    def plane_z_y(self) -> IRect[T]:
        """
        The Z-Y plane of the cuboid (normal vector pointing in the X direction).
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def get_plane(self, axis_index: int = 2, flip: bool = False) -> IRect[T]:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __copy__(self) -> "IRect3D[T]":
        """
        Create a shallow copy of the cuboid.

        Returns:
            GenericIRect3D[T] -> A new instance of the GenericIRect3D class with the same properties.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __eq__(self, value) -> bool:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __ne__(self, value) -> bool:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __gt__(self, value) -> bool:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __ge__(self, value) -> bool:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __lt__(self, value) -> bool:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __le__(self, value) -> bool:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __add__(self, value: "IRect3D[T]") -> "IRect3D[T]":
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __iadd__(self, value: "IRect3D[T]") -> "IRect3D[T]":
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __sub__(self, value: "IRect3D[T]") -> "IRect3D[T]":
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __isub__(self, value: "IRect3D[T]") -> "IRect3D[T]":
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __mul__(self, value: float) -> "IRect3D[T]":
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __imul__(self, value: float) -> "IRect3D[T]":
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __div__(self, value: float) -> "IRect3D[T]":
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __idiv__(self, value: float) -> "IRect3D[T]":
        raise NotImplementedError("This method must be implemented by subclasses.")



class GenericRect3D(IRect3D[T]):
    """
    A 3D rectangle (cuboid) that supports coordinates using integers or floating point values.

    Parameters:
        T x_min:
            X-coordinate of the bottom-left corner of the X-Y plane.
        T x_max:
            X-coordinate of the top-right corner of the X-Y plane.
        T y_min:
            Y-coordinate of the bottom-left corner of the X-Y plane.
        T y_max:
            Y-coordinate of the top-right corner of the X-Y plane.
        T z_min:
            Z-coordinate of the near plane.
        T z_max:
            Z-coordinate of the far plane.

    Use the following classmethods to create an instance:
        - create_from_size(x, y, z, width, height, depth)
        - create_from_centre(x, y, z, width, height, depth)
        - create_from_limits(x_min, x_max, y_min, y_max, z_min, z_max)
    """

    def __init__(self, x_min: T, x_max: T, y_min: T, y_max: T, z_min: T, z_max: T) -> None:
        self.__x_min = x_min
        self.__x_max = x_max
        self.__y_min = y_min
        self.__y_max = y_max
        self.__z_min = z_min
        self.__z_max = z_max

    @classmethod
    def create_from_size(cls, x: T, y: T, z: T, width: T, height: T, depth: T) -> "GenericRect3D[T]":
        """
        Creates a GenericRect3D instance using the specified position of the bottom-left-near corner and size.

        Parameters:
            T x:
                The x-coordinate of the bottom-left corner of the near plane.
            T y:
                The y-coordinate of the bottom-left corner of the near plane.
            T z:
                The z-coordinate of the near plane.
            T width:
                The width of the X-Y plane.
            T height:
                The height of the X-Y plane.
            T depth:
                The depth of the far plane from the near plane.

        Returns:
            GenericRect3D[T] -> A new GenericRect3D instance defined by the given position and size.
        """
        return cls(x, x + width, y, y + height, z, z + depth)

    @classmethod
    def create_from_centre(cls, x: T, y: T, z: T, width: T, height: T, depth: T) -> "GenericRect3D[T]":
        """
        Create a GenericRect3D instance using the centre coordinates and dimensions.

        Parameters:
            T x:
                The x-coordinate of the centre of the volume.
            T y:
                The y-coordinate of the centre of the volume.
            T z:
                The z-coordinate of the centre of the volume.
            T width:
                The width of the X-Y plane.
            T height:
                The height of the X-Y plane.
            T depth:
                The depth of the far plane from the near plane.

        Returns:
            GenericRect3D[T] -> Instance centred on (x, y, z) with the specified width, height, and depth.
        """
        return cls(x - width / 2, x + width / 2, y - height / 2, y + height / 2, z - depth / 2, z + depth / 2)

    @classmethod
    def create_from_limits(cls, x_min: T, x_max: T, y_min: T, y_max: T, z_min: T, z_max: T) -> "GenericRect3D[T]":
        """
        Create a GenericRect3D instance from the specified boundary limits.
        This is the same as the constructor parameters and is implemented for consistency.

        Parameters:
            T x_min:
                The minimum x-coordinate of the rectangle.
            T x_max:
                The maximum x-coordinate of the rectangle.
            T y_min:
                The minimum y-coordinate of the rectangle.
            T y_max:
                The maximum y-coordinate of the rectangle.
            T z_min:
                The minimum z-coordinate of the rectangle.
            T z_max:
                The maximum z-coordinate of the rectangle.

        Returns:
            GenericRect3D[T] -> A new instance of the Rect3D class defined by the given limits.
        """
        return cls(x_min, x_max, y_min, y_max, z_min, z_max)

    @classmethod
    def create_from_data(cls, x_data: Iterable[T], y_data: Iterable[T], z_data: Iterable[T]) -> "GenericRect3D[T]":
        """
        Create a GenericRect3D instance that encompasses the provided data.

        Parameters:
            Iterable[T] x_data:
                X-coordinates.
            Iterable[T] y_data:
                Y-coordinates.
            Iterable[T] z_data:
                Z-coordinates.

        Returns:
            GenericRect3D[T] -> A new instance of the Rect3D class that encompasses the data.
        """
        return cls(min(x_data), max(x_data), min(y_data), max(y_data), min(z_data), max(z_data))

    @property
    def x(self) -> T:
        """
        The x-coordinate of the bottom-left corner of the X-Y plane.

        Returns:
            T -> The x-coordinate of the X-Y plane's bottom-left corner.
        """
        return self.__x_min

    @x.setter
    def _(self, value: T) -> None:
        self.__x_min = value

    @property
    def y(self) -> T:
        """
        The y-coordinate of the bottom-left corner of the X-Y plane.

        Returns:
            T -> The y-coordinate of the X-Y plane's bottom-left corner.
        """
        return self.__y_min

    @y.setter
    def _(self, value: T) -> None:
        self.__y_min = value

    @property
    def z(self) -> T:
        """
        The z-coordinate of the near plane.

        Returns:
            T -> The z-coordinate of the near plane.
        """
        return self.__z_min
    
    @z.setter
    def _(self, value: T) -> None:
        self.__z_min = value

    @property
    def x1(self) -> T:
        """
        The x-coordinate of the top-right corner of the X-Y plane.

        Returns:
            T -> The x-coordinate of the X-Y plane's top-right corner.
        """
        return self.__x_max

    @x1.setter
    def _(self, value: T) -> None:
        self.__x_max = value

    @property
    def y1(self) -> T:
        """
        The y-coordinate of the top-right corner of the X-Y plane.

        Returns:
            T -> The y-coordinate of the X-Y plane's top-right corner.
        """
        return self.__y_max

    @y1.setter
    def _(self, value: T) -> None:
        self.__y_max = value

    @property
    def z1(self) -> T:
        """
        The z-coordinate of the far plane.

        Returns:
            T -> The z-coordinate of the far plane.
        """
        return self.__z_max
    
    @z1.setter
    def _(self, value: T) -> None:
        self.__z_max = value

    @property
    def range(self) -> tuple[tuple[T, T], tuple[T, T], tuple[T, T]]:
        """
        The limits of the cuboid in the form ((x_min, x_max), (y_min, y_max), (z_min, z_max)).
        """
        return (self.__x_min, self.__x_max), (self.__y_min, self.__y_max), (self.__z_min, self.__z_max)

    @property
    def width(self) -> T:
        """
        The width of the X-Y plane.

        Returns:
            T -> The width of the X-Y plane.
        """
        return self.__x_max - self.__x_min

    @property
    def height(self) -> T:
        """
        The height of the X-Y plane.
        
        Returns:
            T -> The height of the X-Y plane.
        """
        return self.__y_max - self.__y_min

    @property
    def depth(self) -> T:
        """
        The depth between the far to near planes.

        Returns:
            T -> The depth between the far to near planes.
        """
        return self.__z_max - self.__z_min

    @property
    def centre(self) -> tuple[T, T, T]:
        """
        The coordinates of the center of the cuboid.

        Returns:
            tuple[T, T, T] -> (x, y, z)
        """
        return ((self.__x_max + self.__x_min) / 2, (self.__y_max + self.__y_min) / 2, (self.__z_max + self.__z_min) / 2)

    @property
    def volume(self) -> T:
        """
        The volume of the cuboid.

        Returns:
            T -> The volume of the cuboid.
        """
        return self.width * self.height * self.depth

    @property
    def plane_x_y(self) -> GenericRect[T]:
        return GenericRect.create_from_limits(self.x, self.x1, self.y, self.y1)

    @property
    def plane_y_x(self) -> GenericRect[T]:
        return GenericRect.create_from_limits(self.y, self.y1, self.x, self.x1)

    @property
    def plane_x_z(self) -> GenericRect[T]:
        return GenericRect.create_from_limits(self.x, self.x1, self.z, self.z1)

    @property
    def plane_z_x(self) -> GenericRect[T]:
        return GenericRect.create_from_limits(self.z, self.z1, self.x, self.x1)

    @property
    def plane_y_z(self) -> GenericRect[T]:
        return GenericRect.create_from_limits(self.y, self.y1, self.z, self.z1)

    @property
    def plane_z_y(self) -> GenericRect[T]:
        return GenericRect.create_from_limits(self.z, self.z1, self.y, self.y1)

    def get_plane(self, axis_index: int = 2, flip: bool = False) -> GenericRect[T]:
        match axis_index:
            case 0:
                return self.plane_z_y if not flip else self.plane_y_z
            case 1:
                return self.plane_x_z if not flip else self.plane_z_x
            case 2:
                return self.plane_x_y if not flip else self.plane_y_x
            case _:
                raise ValueError("Axis must be 0 (X-Y), 1 (Y-Z), or 2 (X-Z).")

    def __copy__(self) -> "GenericRect3D[T]":
        """
        Create a shallow copy of the cuboid.

        Returns:
            GenericRect3D[T] -> A new instance of the GenericRect3D class with the same properties.
        """
        return GenericRect3D(self.__x_min, self.__x_max, self.__y_min, self.__y_max, self.__z_min, self.__z_max)

    def __str__(self) -> str:
        return f"Cuboid(x: {self.__x_min} -> {self.__x_max}, y: {self.__y_min} -> {self.__y_max}, z: {self.__z_min} -> {self.__z_max})"

    def __repr__(self) -> str:
        return "GenericRect3D: " + self.__str__()

    def __eq__(self, value):
        if isinstance(value, GenericRect3D):
            return self.__x_min == value.__x_min and self.__x_max == value.__x_max and self.__y_min == value.__y_min and self.__y_max == value.__y_max and self.__z_min == value.__z_min and self.__z_max == value.__z_max
        return False

    def __ne__(self, value) -> bool:
        return not self.__eq__(value)

    def __gt__(self, value) -> bool:
        if isinstance(value, IRect3D):
            return self.volume > value.volume
        elif isinstance(value, (int, float, Decimal, np.integer, np.floating)):
            return self.volume > value
        return False

    def __ge__(self, value) -> bool:
        if isinstance(value, IRect3D):
            return self.volume >= value.volume
        elif isinstance(value, (int, float, Decimal, np.integer, np.floating)):
            return self.volume >= value
        return False

    def __lt__(self, value) -> bool:
        if isinstance(value, IRect3D):
            return self.volume < value.volume
        elif isinstance(value, (int, float, Decimal, np.integer, np.floating)):
            return self.volume < value
        return False

    def __le__(self, value) -> bool:
        if isinstance(value, IRect3D):
            return self.volume <= value.volume
        elif isinstance(value, (int, float, Decimal, np.integer, np.floating)):
            return self.volume <= value
        return False

    def __add__(self, value: IRect3D[T]) -> "GenericRect3D[T]":
        return type(self).create_from_size(
            self.__x_min + value.x,
            self.__y_min + value.y,
            self.__z_min + value.z,
            self.width + value.width,
            self.height + value.height,
            self.depth + value.depth
        )

    def __iadd__(self, value: IRect3D[T]) -> "GenericRect3D[T]":
        current_width = self.width
        current_height = self.height
        current_depth = self.depth
        self.__x_min += value.x
        self.__y_min += value.y
        self.__z_min += value.z
        self.__x_max = self.__x_min + current_width + value.width
        self.__y_max = self.__y_min + current_height + value.height
        self.__z_max = self.__z_min + current_depth + value.depth
        return self

    def __sub__(self, value: IRect3D[T]) -> "GenericRect3D[T]":
        return type(self).create_from_size(
            self.__x_min - value.x,
            self.__y_min - value.y,
            self.__z_min - value.z,
            self.width - value.width,
            self.height - value.height,
            self.depth - value.depth
        )

    def __isub__(self, value: IRect3D[T]) -> "GenericRect3D[T]":
        current_width = self.width
        current_height = self.height
        current_depth = self.depth
        self.__x_min -= value.x
        self.__y_min -= value.y
        self.__z_min -= value.z
        self.__x_max = self.__x_min + current_width - value.width
        self.__y_max = self.__y_min + current_height - value.height
        self.__z_max = self.__z_min + current_depth - value.depth
        return self

    def __mul__(self, value: float) -> "GenericRect3D[T]":
        return type(self).create_from_size(
            self.__x_min,
            self.__y_min,
            self.__z_min,
            self.width * value,
            self.height * value,
            self.depth * value
        )

    def __imul__(self, value: float) -> "GenericRect3D[T]":
        self.__x_max = self.__x_min + (self.width * value)
        self.__y_max = self.__y_min + (self.height * value)
        self.__z_max = self.__z_min + (self.depth * value)
        return self

    def __div__(self, value: float) -> "GenericRect3D[T]":
        return type(self).create_from_size(
            self.__x_min,
            self.__y_min,
            self.__z_min,
            self.width / value,
            self.height / value,
            self.depth / value
        )

    def __idiv__(self, value: float) -> "GenericRect3D[T]":
        self.__x_max = self.__x_min + (self.width / value)
        self.__y_max = self.__y_min + (self.height / value)
        self.__z_max = self.__z_min + (self.depth / value)
        return self



class Rect3D(GenericRect3D[float]):
    """
    A 3D rectangle (cuboid).

    Parameters:
        float x_min:
            X-coordinate of the bottom-left corner of the X-Y plane.
        float x_max:
            X-coordinate of the top-right corner of the X-Y plane.
        float y_min:
            Y-coordinate of the bottom-left corner of the X-Y plane.
        float y_max:
            Y-coordinate of the top-right corner of the X-Y plane.
        float z_min:
            Z-coordinate of the near plane.
        float z_max:
            Z-coordinate of the far plane.

    Use the following classmethods to create an instance:
        - create_from_size(x, y, z, width, height, depth)
        - create_from_centre(x, y, z, width, height, depth)
        - create_from_limits(x_min, x_max, y_min, y_max, z_min, z_max)
    """

    @classmethod
    def create_from_size(cls, x: float, y: float, z: float, width: float, height: float, depth: float) -> "Rect3D":
        """
        Creates a Rect3D instance using the specified position of the bottom-left-near corner and size.

        Parameters:
            float x:
                The x-coordinate of the bottom-left corner of the near plane.
            float y:
                The y-coordinate of the bottom-left corner of the near plane.
            float z:
                The z-coordinate of the near plane.
            float width:
                The width of the X-Y plane.
            float height:
                The height of the X-Y plane.
            float depth:
                The depth of the far plane from the near plane.

        Returns:
            Rect3D -> A new Rect3D instance defined by the given position and size.
        """
        return super().create_from_size(x, width, y, height, z, depth)

    @classmethod
    def create_from_centre(cls, x: float, y: float, z: float, width: float, height: float, depth: float) -> "Rect3D":
        """
        Create a Rect3D instance using the centre coordinates and dimensions.

        Parameters:
            float x:
                The x-coordinate of the centre of the volume.
            float y:
                The y-coordinate of the centre of the volume.
            float z:
                The z-coordinate of the centre of the volume.
            float width:
                The width of the X-Y plane.
            float height:
                The height of the X-Y plane.
            float depth:
                The depth of the far plane from the near plane.

        Returns:
            Rect3D -> Instance centred on (x, y, z) with the specified width, height, and depth.
        """
        return super().create_from_centre(x, y, z, width, height, depth)

    @classmethod
    def create_from_limits(cls, x_min: float, x_max: float, y_min: float, y_max: float, z_min: float, z_max: float) -> "Rect3D":
        """
        Create a Rect3D instance from the specified boundary limits.
        This is the same as the constructor parameters and is implemented for consistency.

        Parameters:
            float x_min:
                The minimum x-coordinate of the rectangle.
            float x_max:
                The maximum x-coordinate of the rectangle.
            float y_min:
                The minimum y-coordinate of the rectangle.
            float y_max:
                The maximum y-coordinate of the rectangle.
            float z_min:
                The minimum z-coordinate of the rectangle.
            float z_max:
                The maximum z-coordinate of the rectangle.

        Returns:
            Rect3D -> A new instance of the Rect3D class defined by the given limits.
        """
        return super().create_from_limits(x_min, x_max, y_min, y_max, z_min, z_max)

    @classmethod
    def create_from_data(cls, x_data: Iterable[float], y_data: Iterable[float], z_data: Iterable[float]) -> "Rect3D":
        """
        Create a Rect3D instance that encompasses the provided data.

        Parameters:
            Iterable[T] x_data:
                X-coordinates.
            Iterable[T] y_data:
                Y-coordinates.
            Iterable[T] z_data:
                Z-coordinates.

        Returns:
            Rect3D -> A new instance of the Rect3D class that encompasses the data.
        """
        return super().create_from_data(x_data, y_data, z_data)

    @property
    def x(self) -> float:
        """
        The x-coordinate of the bottom-left corner of the X-Y plane.

        Returns:
            float -> The x-coordinate of the X-Y plane's bottom-left corner.
        """
        return GenericRect3D.x.fget(self)

    @x.setter
    def _(self, value: float) -> None:
        return GenericRect3D.x.fset(self, value)

    @property
    def y(self) -> float:
        """
        The y-coordinate of the bottom-left corner of the X-Y plane.

        Returns:
            float -> The y-coordinate of the X-Y plane's bottom-left corner.
        """
        return GenericRect3D.y.fget(self)

    @y.setter
    def _(self, value: float) -> None:
        return GenericRect3D.y.fset(self, value)

    @property
    def z(self) -> float:
        """
        The z-coordinate of the near plane.

        Returns:
            float -> The z-coordinate of the near plane.
        """
        return GenericRect3D.z.fget(self)

    @z.setter
    def _(self, value: float) -> None:
        return GenericRect3D.z.fset(self, value)

    @property
    def x1(self) -> float:
        """
        The x-coordinate of the top-right corner of the X-Y plane.

        Returns:
            float -> The x-coordinate of the X-Y plane's top-right corner.
        """
        return GenericRect3D.x1.fget(self)

    @x1.setter
    def _(self, value: float) -> None:
        return GenericRect3D.x1.fset(self, value)

    @property
    def y1(self) -> float:
        """
        The y-coordinate of the top-right corner of the X-Y plane.

        Returns:
            float -> The y-coordinate of the X-Y plane's top-right corner.
        """
        return GenericRect3D.y1.fget(self)

    @y1.setter
    def _(self, value: float) -> None:
        return GenericRect3D.y1.fset(self, value)

    @property
    def z1(self) -> float:
        """
        The z-coordinate of the top-right corner of the X-Y plane.

        Returns:
            float -> The z-coordinate of the X-Y plane's top-right corner.
        """
        return GenericRect3D.z1.fget(self)

    @z1.setter
    def _(self, value: float) -> None:
        return GenericRect3D.z1.fset(self, value)

    @property
    def range(self) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]]:
        """
        The limits of the cuboid in the form ((x_min, x_max), (y_min, y_max), (z_min, z_max)).
        """
        return GenericRect3D.range.fget(self)

    @property
    def width(self) -> float:
        """
        The width of the X-Y plane.

        Returns:
            float -> The width of the X-Y plane.
        """
        return GenericRect3D.width.fget(self)

    @property
    def height(self) -> float:
        """
        The height of the X-Y plane.
        
        Returns:
            float -> The height of the X-Y plane.
        """
        return GenericRect3D.height.fget(self)

    @property
    def depth(self) -> float:
        """
        The depth between the far to near planes.

        Returns:
            float -> The depth between the far to near planes.
        """
        return GenericRect3D.depth.fget(self)

    @property
    def centre(self) -> tuple[float, float, float]:
        """
        The coordinates of the center of the cuboid.

        Returns:
            tuple[float, float, float] -> (x, y, z)
        """
        return GenericRect3D.centre.fget(self)

    @property
    def volume(self) -> float:
        """
        The volume of the cuboid.

        Returns:
            float -> The volume of the cuboid.
        """
        return  GenericRect3D.volume.fget(self)

    @property
    def plane_x_y(self) -> Rect:
        return GenericRect3D.plane_x_y.fget(self)

    @property
    def plane_y_x(self) -> Rect:
        return GenericRect3D.plane_y_x.fget(self)

    @property
    def plane_x_z(self) -> Rect:
        return GenericRect3D.plane_x_z.fget(self)

    @property
    def plane_z_x(self) -> Rect:
        return GenericRect3D.plane_z_x.fget(self)

    @property
    def plane_y_z(self) -> Rect:
        return GenericRect3D.plane_y_z.fget(self)

    @property
    def plane_z_y(self) -> Rect:
        return GenericRect3D.plane_z_y.fget(self)

    def get_plane(self, axis_index: int = 2, flip: bool = False) -> Rect:
        return GenericRect3D.get_plane(self, axis_index, flip)

    def __copy__(self) -> "Rect3D":
        """
        Create a shallow copy of the cuboid.

        Returns:
            Rect3D -> A new instance of the Rect3D class with the same properties.
        """
        ranges = self.range
        return Rect3D(ranges[0][0], ranges[0][1], ranges[1][0], ranges[1][1], ranges[2][0], ranges[2][1])

    def __repr__(self) -> str:
        return "Rect3D: " + self.__str__()

    def __add__(self, value: IRect3D[T]) -> "Rect3D":
        return super().__add__(value)

    def __sub__(self, value: IRect3D[T]) -> "Rect3D":
        return super().__sub__(value)

    def __mul__(self, value: float) -> "Rect3D":
        return super().__mul__(value)

    def __div__(self, value: float) -> "Rect3D":
        return super().__div__(value)



class DiscreteRect3D(GenericRect3D[int]):
    """
    A 3D rectangle (cuboid).

    Parameters:
        int x_min:
            X-coordinate of the bottom-left corner of the X-Y plane.
        int x_max:
            X-coordinate of the top-right corner of the X-Y plane.
        int y_min:
            Y-coordinate of the bottom-left corner of the X-Y plane.
        int y_max:
            Y-coordinate of the top-right corner of the X-Y plane.
        int z_min:
            Z-coordinate of the near plane.
        int z_max:
            Z-coordinate of the far plane.

    Use the following classmethods to create an instance:
        - create_from_size(x, y, z, width, height, depth)
        - create_from_centre(x, y, z, width, height, depth)
        - create_from_limits(x_min, x_max, y_min, y_max, z_min, z_max)
    """

    @classmethod
    def create_from_size(cls, x: int, y: int, z: int, width: int, height: int, depth: int) -> "DiscreteRect3D":
        """
        Creates a DiscreteRect3D instance using the specified position of the bottom-left-near corner and size.

        Parameters:
            int x:
                The x-coordinate of the bottom-left corner of the near plane.
            int y:
                The y-coordinate of the bottom-left corner of the near plane.
            int z:
                The z-coordinate of the near plane.
            int width:
                The width of the X-Y plane.
            int height:
                The height of the X-Y plane.
            int depth:
                The depth of the far plane from the near plane.

        Returns:
            DiscreteRect3D -> A new ReDiscreteRect3Dct3D instance defined by the given position and size.
        """
        return super().create_from_size(x, y, z, width, height, depth)
    
    @classmethod
    def create_from_centre(cls, x: int, y: int, z: int, width: int, height: int, depth: int) -> "DiscreteRect3D":
        """
        Create a DiscreteRect3D instance using the centre coordinates and dimensions.
        In the event that the width, height or depth are odd values, the upper bounds will be further from the centre by 1 then the lower bounds.

        Parameters:
            int x:
                The x-coordinate of the centre of the volume.
            int y:
                The y-coordinate of the centre of the volume.
            int z:
                The z-coordinate of the centre of the volume.
            int width:
                The width of the X-Y plane.
            int height:
                The height of the X-Y plane.
            int depth:
                The depth of the far plane from the near plane.

        Returns:
            DiscreteRect3D -> Instance centred on (x, y, z) with the specified width, height, and depth.
        """
        return cls(math.floor(x - width / 2), math.ceil(x + width / 2), math.floor(y - height / 2), math.ceil(y + height / 2), math.floor(z - depth / 2), math.ceil(z + depth / 2))

    @classmethod
    def create_from_limits(cls, x_min: int, x_max: int, y_min: int, y_max: int, z_min: int, z_max: int) -> "DiscreteRect3D":
        """
        Create a DiscreteRect3D instance from the specified boundary limits.
        This is the same as the constructor parameters and is implemented for consistency.

        Parameters:
            int x_min:
                The minimum x-coordinate of the rectangle.
            int x_max:
                The maximum x-coordinate of the rectangle.
            int y_min:
                The minimum y-coordinate of the rectangle.
            int y_max:
                The maximum y-coordinate of the rectangle.
            int z_min:
                The minimum z-coordinate of the rectangle.
            int z_max:
                The maximum z-coordinate of the rectangle.

        Returns:
            DiscreteRect3D -> A new instance of the DiscreteRect3D class defined by the given limits.
        """
        return super().create_from_limits(x_min, x_max, y_min, y_max, z_min, z_max)

    @classmethod
    def create_from_data(cls, x_data: Iterable[int], y_data: Iterable[int], z_data: Iterable[int]) -> "DiscreteRect3D":
        """
        Create a DiscreteRect3D instance that encompasses the provided data.

        Parameters:
            Iterable[int] x_data:
                X-coordinates.
            Iterable[int] y_data:
                Y-coordinates.
            Iterable[int] z_data:
                Z-coordinates.

        Returns:
            DiscreteRect3D -> A new instance of the DiscreteRect3D class that encompasses the data.
        """
        return super().create_from_data(x_data, y_data, z_data)

    @property
    def x(self) -> int:
        """
        The x-coordinate of the bottom-left corner of the X-Y plane.

        Returns:
            int -> The x-coordinate of the X-Y plane's bottom-left corner.
        """
        return GenericRect3D.x.fget(self)

    @x.setter
    def _(self, value: int) -> None:
        return GenericRect.x.fset(self, value)

    @property
    def y(self) -> int:
        """
        The y-coordinate of the bottom-left corner of the X-Y plane.

        Returns:
            int -> The y-coordinate of the X-Y plane's bottom-left corner.
        """
        return GenericRect3D.y.fget(self)

    @y.setter
    def _(self, value: int) -> None:
        return GenericRect.y.fset(self, value)
    
    @property
    def z(self) -> int:
        """
        The z-coordinate of the near plane.

        Returns:
            int -> The z-coordinate of the near plane.
        """
        return GenericRect3D.z.fget(self)

    @z.setter
    def _(self, value: int) -> None:
        return GenericRect3D.z.fset(self, value)

    @property
    def x1(self) -> int:
        """
        The x-coordinate of the top-right corner of the X-Y plane.

        Returns:
            int -> The x-coordinate of the X-Y plane's top-right corner.
        """
        return GenericRect3D.x1.fget(self)

    @x1.setter
    def _(self, value: int) -> None:
        return GenericRect.x1.fset(self, value)

    @property
    def y1(self) -> int:
        """
        The y-coordinate of the top-right corner of the X-Y plane.

        Returns:
            int -> The y-coordinate of the X-Y plane's top-right corner.
        """
        return GenericRect3D.y1.fget(self)

    @y1.setter
    def _(self, value: int) -> None:
        return GenericRect.y1.fset(self, value)

    @property
    def z1(self) -> int:
        """
        The z-coordinate of the top-right corner of the X-Y plane.

        Returns:
            int -> The z-coordinate of the X-Y plane's top-right corner.
        """
        return GenericRect3D.z1.fget(self)

    @z1.setter
    def _(self, value: int) -> None:
        return GenericRect3D.z1.fset(self, value)

    @property
    def range(self) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
        """
        The limits of the rectangle in the form ((x_min, x_max), (y_min, y_max), (z_min, z_max)).
        """
        return GenericRect3D.range.fget(self)

    @property
    def width(self) -> int:
        """
        The width of the X-Y plane.

        Returns:
            int -> The width of the X-Y plane.
        """
        return GenericRect3D.width.fget(self)

    @property
    def height(self) -> int:
        """
        The height of the X-Y plane.
        
        Returns:
            int -> The height of the X-Y plane.
        """
        return GenericRect3D.height.fget(self)

    @property
    def depth(self) -> int:
        """
        The depth between the far to near planes.

        Returns:
            int -> The depth between the far to near planes.
        """
        return GenericRect3D.depth.fget(self)

    @property
    def centre(self) -> tuple[int, int, int]:
        """
        The coordinates of the center of the cuboid.

        Returns:
            tuple[int, int, int] -> (x, y, z)
        """
        return (math.floor((self.x1 + self.x) / 2), math.floor((self.y1 + self.y) / 2), math.floor((self.z1 + self.z) / 2))

    @property
    def volume(self) -> int:
        """
        The volume of the cuboid.

        Returns:
            int -> The volume of the cuboid.
        """
        return  GenericRect3D.volume.fget(self)

    @property
    def plane_x_y(self) -> DiscreteRect:
        return GenericRect3D.plane_x_y.fget(self)

    @property
    def plane_y_x(self) -> DiscreteRect:
        return GenericRect3D.plane_y_x.fget(self)

    @property
    def plane_x_z(self) -> DiscreteRect:
        return GenericRect3D.plane_x_z.fget(self)

    @property
    def plane_z_x(self) -> DiscreteRect:
        return GenericRect3D.plane_z_x.fget(self)

    @property
    def plane_y_z(self) -> DiscreteRect:
        return GenericRect3D.plane_y_z.fget(self)

    @property
    def plane_z_y(self) -> DiscreteRect:
        return GenericRect3D.plane_z_y.fget(self)

    def get_plane(self, axis_index: int = 2, flip: bool = False) -> DiscreteRect:
        return GenericRect3D.get_plane(self, axis_index, flip)

    def __copy__(self) -> "DiscreteRect3D":
        """
        Create a shallow copy of the cuboid.

        Returns:
            DiscreteRect3D -> A new instance of the DiscreteRect3D class with the same properties.
        """
        ranges = self.range
        return DiscreteRect3D(ranges[0][0], ranges[0][1], ranges[1][0], ranges[1][1], ranges[2][0], ranges[2][1])

    def __repr__(self) -> str:
        return "DiscreteRect3D: " + self.__str__()

    def __add__(self, value: IRect3D[T]) -> "DiscreteRect3D":
        return super().__add__(value)

    def __sub__(self, value: IRect3D[T]) -> "DiscreteRect3D":
        return super().__sub__(value)

    def __mul__(self, value: float) -> "DiscreteRect3D":
        return type(self).create_from_size(
            self.x,
            self.y,
            self.z,
            math.floor(self.width * value),
            math.floor(self.height * value),
            math.floor(self.depth * value)
        )

    def __imul__(self, value: float) -> None:
        self.x1 = self.x + math.floor(self.width * value)
        self.y1 = self.y + math.floor(self.height * value)
        self.z1 = self.z + math.floor(self.depth * value)

    def __div__(self, value: float) -> "DiscreteRect3D":
        return type(self).create_from_size(
            self.x,
            self.y,
            self.z,
            math.floor(self.width / value),
            math.floor(self.height / value),
            math.floor(self.depth / value)
        )

    def __idiv__(self, value: float) -> None:
        self.x1 = self.x + math.floor(self.width / value)
        self.y1 = self.y + math.floor(self.height / value)
        self.z1 = self.z + math.floor(self.depth / value)
