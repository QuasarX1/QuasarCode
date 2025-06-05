from abc import abstractmethod
from decimal import Decimal
import math
from typing import Iterable, TypeVar, Generic

import numpy as np

T = TypeVar("T")
class IRect(Generic[T]):
    """
    Interface for a 2D rectangle type.

    Use the following static classmethods on an implementation to create an instance:
        - create_from_size(x, y, width, height)
        - create_from_centre(x, y, width, height)
        - create_from_limits(x_min, x_max, y_min, y_max)
    """

    @abstractmethod
    @classmethod
    def create_from_size(cls, x: T, y: T, width: T, height: T) -> "IRect[T]":
        """
        Creates an IRect instance using the specified position of the bottom-left corner and size.

        Parameters:
            T x:
                The x-coordinate of the bottom-left corner of the rectangle.
            T y:
                The y-coordinate of the bottom-left corner of the rectangle.
            T width:
                The width of the rectangle.
            T height:
                The height of the rectangle.

        Returns:
            IRect[T] -> A new IRect instance defined by the given position and size.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    @classmethod
    def create_from_centre(cls, x: T, y: T, width: T, height: T) -> "IRect[T]":
        """
        Create a IRect instance using the centre coordinates and dimensions.

        Parameters:
            T x:
                The x-coordinate of the centre of the rectangle.
            T y:
                The y-coordinate of the centre of the rectangle.
            T width:
                The width of the rectangle.
            T height:
                The height of the rectangle.

        Returns:
            IRect[T] -> Instance centred on (x, y) with the specified width and height.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    @classmethod
    def create_from_limits(cls, x_min: T, x_max: T, y_min: T, y_max: T) -> "IRect[T]":
        """
        Create a IRect instance from the specified boundary limits.
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

        Returns:
            IRect[T] -> A new instance of the Rect class defined by the given limits.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    @classmethod
    def create_from_data(cls, x_data: Iterable[T], y_data: Iterable[T]) -> "IRect[T]":
        """
        Create a IRect instance that encompasses the provided data.

        Parameters:
            Iterable[T] x_data:
                X-coordinates.
            Iterable[T] y_data:
                Y-coordinates.

        Returns:
            IRect[T] -> A new instance of the Rect class that encompasses the data.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    @property
    def x(self) -> T:
        """
        The x-coordinate of the bottom-left corner of the rectangle.

        Returns:
            T -> The x-coordinate of the bottom-left corner.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    @x.setter
    def _(self, value: T) -> None:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    @property
    def y(self) -> T:
        """
        The y-coordinate of the bottom-left corner of the rectangle.

        Returns:
            T -> The y-coordinate of the bottom-left corner.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    @y.setter
    def _(self, value: T) -> None:
        raise NotImplementedError("This method must be implemented by subclasses.")
        
    @abstractmethod
    @property
    def x1(self) -> T:
        """
        The x-coordinate of the top-right corner of the rectangle.

        Returns:
            T -> The x-coordinate of the top-right corner.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    @x1.setter
    def _(self, value: T) -> None:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    @property
    def y1(self) -> T:
        """
        The y-coordinate of the top-right corner of the rectangle.

        Returns:
            T -> The y-coordinate of the top-right corner.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    @y1.setter
    def _(self, value: T) -> None:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    @property
    def extent(self) -> tuple[T, T, T, T]:
        """
        The limits of the rectangle in the form (x_min, x_max, y_min, y_max).
        This corresponds to the format of a matplotlib 'extent' parameter.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    @property
    def range(self) -> tuple[tuple[T, T], tuple[T, T]]:
        """
        The limits of the rectangle in the form ((x_min, x_max), (y_min, y_max)).
        This corresponds to the format of a numpy histogram2d 'range' parameter.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    @property
    def width(self) -> T:
        """
        The width of the rectangle.

        Returns:
            T -> The width of the rectangle.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    @property
    def height(self) -> T:
        """
        The height of the rectangle.
        
        Returns:
            T -> The height of the rectangle.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    @property
    def centre(self) -> tuple[T, T]:
        """
        The coordinates of the center of the rectangle.

        Returns:
            tuple[T, T] -> (x, y)
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    @property
    def area(self) -> T:
        """
        The area of the rectangle.

        Returns:
            T -> The area of the rectangle.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __copy__(self) -> "IRect[T]":
        """
        Create a shallow copy of the rectangle.

        Returns:
            GenericRect[T] -> A new instance of the GenericRect class with the same properties.
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
    def __add__(self, value: "IRect[T]") -> "IRect[T]":
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __iadd__(self, value: "IRect[T]") -> None:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __sub__(self, value: "IRect[T]") -> "IRect[T]":
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __isub__(self, value: "IRect[T]") -> None:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __mul__(self, value: float) -> "IRect[T]":
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __imul__(self, value: float) -> None:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __div__(self, value: float) -> "IRect[T]":
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __idiv__(self, value: float) -> None:
        raise NotImplementedError("This method must be implemented by subclasses.")



class GenericRect(IRect[T]):
    """
    A 2D rectangle that supports coordinates using integers or floating point values.

    Parameters:
        T x_min:
            X-coordinate of the bottom-left corner.
        T x_max:
            X-coordinate of the top-right corner.
        T y_min:
            Y-coordinate of the bottom-left corner.
        T y_max:
            Y-coordinate of the top-right corner.

    Use the following classmethods to create an instance:
        - create_from_size(x, y, width, height)
        - create_from_centre(x, y, width, height)
        - create_from_limits(x_min, x_max, y_min, y_max)
    """

    def __init__(self, x_min: T, x_max: T, y_min: T, y_max: T) -> None:
        self.__x_min = x_min
        self.__x_max = x_max
        self.__y_min = y_min
        self.__y_max = y_max

    @classmethod
    def create_from_size(cls, x: T, y: T, width: T, height: T) -> "GenericRect[T]":
        """
        Creates a GenericRect instance using the specified position of the bottom-left corner and size.

        Parameters:
            T x:
                The x-coordinate of the bottom-left corner of the rectangle.
            T y:
                The y-coordinate of the bottom-left corner of the rectangle.
            T width:
                The width of the rectangle.
            T height:
                The height of the rectangle.

        Returns:
            GenericRect[T] -> A new GenericRect instance defined by the given position and size.
        """
        return cls(x, x + width, y, y + height)

    @classmethod
    def create_from_centre(cls, x: T, y: T, width: T, height: T) -> "GenericRect[T]":
        """
        Create a GenericRect instance using the centre coordinates and dimensions.

        Parameters:
            T x:
                The x-coordinate of the centre of the rectangle.
            T y:
                The y-coordinate of the centre of the rectangle.
            T width:
                The width of the rectangle.
            T height:
                The height of the rectangle.

        Returns:
            GenericRect[T] -> Instance centred on (x, y) with the specified width and height.
        """
        return cls(x - width / 2, x + width / 2, y - height / 2, y + height / 2)

    @classmethod
    def create_from_limits(cls, x_min: T, x_max: T, y_min: T, y_max: T) -> "GenericRect[T]":
        """
        Create a GenericRect instance from the specified boundary limits.
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

        Returns:
            GenericRect[T] -> A new instance of the Rect class defined by the given limits.
        """
        return cls(x_min, x_max, y_min, y_max)

    @classmethod
    def create_from_data(cls, x_data: Iterable[T], y_data: Iterable[T]) -> "GenericRect[T]":
        """
        Create a GenericRect instance that encompasses the provided data.

        Parameters:
            Iterable[T] x_data:
                X-coordinates.
            Iterable[T] y_data:
                Y-coordinates.

        Returns:
            GenericRect[T] -> A new instance of the Rect class that encompasses the data.
        """
        return cls(min(x_data), max(x_data), min(y_data), max(y_data))

    @property
    def x(self) -> T:
        """
        The x-coordinate of the bottom-left corner of the rectangle.

        Returns:
            T -> The x-coordinate of the bottom-left corner.
        """
        return self.__x_min

    @x.setter
    def _(self, value: T) -> None:
        self.__x_min = value

    @property
    def y(self) -> T:
        """
        The y-coordinate of the bottom-left corner of the rectangle.

        Returns:
            T -> The y-coordinate of the bottom-left corner.
        """
        return self.__y_min

    @y.setter
    def _(self, value: T) -> None:
        self.__y_min = value

    @property
    def x1(self) -> T:
        """
        The x-coordinate of the top-right corner of the rectangle.

        Returns:
            T -> The x-coordinate of the top-right corner.
        """
        return self.__x_max

    @x1.setter
    def _(self, value: T) -> None:
        self.__x_max = value

    @property
    def y1(self) -> T:
        """
        The y-coordinate of the top-right corner of the rectangle.

        Returns:
            T -> The y-coordinate of the top-right corner.
        """
        return self.__y_max

    @y1.setter
    def _(self, value: T) -> None:
        self.__y_max = value

    @property
    def extent(self) -> tuple[T, T, T, T]:
        """
        The limits of the rectangle in the form (x_min, x_max, y_min, y_max).
        This corresponds to the format of a matplotlib 'extent' parameter.
        """
        return (self.__x_min, self.__x_max, self.__y_min, self.__y_max)

    @property
    def range(self) -> tuple[tuple[T, T], tuple[T, T]]:
        """
        The limits of the rectangle in the form ((x_min, x_max), (y_min, y_max)).
        This corresponds to the format of a numpy histogram2d 'range' parameter.
        """
        return ((self.__x_min, self.__x_max), (self.__y_min, self.__y_max))

    @property
    def width(self) -> T:
        """
        The width of the rectangle.

        Returns:
            T -> The width of the rectangle.
        """
        return self.__x_max - self.__x_min

    @property
    def height(self) -> T:
        """
        The height of the rectangle.
        
        Returns:
            T -> The height of the rectangle.
        """
        return self.__y_max - self.__y_min

    @property
    def centre(self) -> tuple[T, T]:
        """
        The coordinates of the center of the rectangle.

        Returns:
            tuple[T, T] -> (x, y)
        """
        return ((self.__x_max + self.__x_min) / 2, (self.__y_max + self.__y_min) / 2)

    @property
    def area(self) -> T:
        """
        The area of the rectangle.

        Returns:
            T -> The area of the rectangle.
        """
        return self.width * self.height

    def __copy__(self) -> "GenericRect[T]":
        """
        Create a shallow copy of the rectangle.

        Returns:
            GenericRect[T] -> A new instance of the GenericRect class with the same properties.
        """
        return GenericRect(self.__x_min, self.__x_max, self.__y_min, self.__y_max)

    def __str__(self) -> str:
        return f"Rect(x: {self.__x_min} -> {self.__x_max}, y: {self.__y_min} -> {self.__y_max})"

    def __repr__(self) -> str:
        return "GenericRect: " + self.__str__()

    def __eq__(self, value):
        if isinstance(value, GenericRect):
            return self.__x_min == value.__x_min and self.__x_max == value.__x_max and self.__y_min == value.__y_min and self.__y_max == value.__y_max
        return False

    def __ne__(self, value) -> bool:
        return not self.__eq__(value)

    def __gt__(self, value) -> bool:
        if isinstance(value, IRect):
            return self.area > value.area
        elif isinstance(value, (int, float, Decimal, np.integer, np.floating)):
            return self.area > value
        return False

    def __ge__(self, value) -> bool:
        if isinstance(value, IRect):
            return self.area >= value.area
        elif isinstance(value, (int, float, Decimal, np.integer, np.floating)):
            return self.area >= value
        return False

    def __lt__(self, value) -> bool:
        if isinstance(value, IRect):
            return self.area < value.area
        elif isinstance(value, (int, float, Decimal, np.integer, np.floating)):
            return self.area < value
        return False

    def __le__(self, value) -> bool:
        if isinstance(value, IRect):
            return self.area <= value.area
        elif isinstance(value, (int, float, Decimal, np.integer, np.floating)):
            return self.area <= value
        return False
    
    def __add__(self, value: IRect[T]) -> "GenericRect[T]":
        return type(self).create_from_size(
            self.__x_min + value.x,
            self.__y_min + value.y,
            self.width + value.width,
            self.height + value.height
        )

    def __iadd__(self, value: IRect[T]) -> None:
        current_width = self.width
        current_height = self.height
        self.__x_min += value.x
        self.__y_min += value.y
        self.__x_max = self.__x_min + current_width + value.width
        self.__y_max = self.__y_min + current_height + value.height

    def __sub__(self, value: IRect[T]) -> "GenericRect[T]":
        return type(self).create_from_size(
            self.__x_min - value.x,
            self.__y_min - value.y,
            self.width - value.width,
            self.height - value.height
        )

    def __isub__(self, value: IRect[T]) -> None:
        current_width = self.width
        current_height = self.height
        self.__x_min -= value.x
        self.__y_min -= value.y
        self.__x_max = self.__x_min + current_width - value.width
        self.__y_max = self.__y_min + current_height - value.height

    def __mul__(self, value: float) -> "GenericRect[T]":
        return type(self).create_from_size(
            self.__x_min,
            self.__y_min,
            self.width * value,
            self.height * value
        )

    def __imul__(self, value: float) -> None:
        self.__x_max = self.__x_min + (self.width * value)
        self.__y_max = self.__y_min + (self.height * value)
        return self

    def __div__(self, value: float) -> "GenericRect[T]":
        return type(self).create_from_size(
            self.__x_min,
            self.__y_min,
            self.width / value,
            self.height / value
        )

    def __idiv__(self, value: float) -> None:
        self.__x_max = self.__x_min + (self.width / value)
        self.__y_max = self.__y_min + (self.height / value)
        return self



class Rect(GenericRect[float]):
    """
    A 2D rectangle.

    Parameters:
        float x_min:
            X-coordinate of the bottom-left corner.
        float x_max:
            X-coordinate of the top-right corner.
        float y_min:
            Y-coordinate of the bottom-left corner.
        float y_max:
            Y-coordinate of the top-right corner.

    Use the following classmethods to create an instance:
        - create_from_size(x, y, width, height)
        - create_from_centre(x, y, width, height)
        - create_from_limits(x_min, x_max, y_min, y_max)
    """

    @classmethod
    def create_from_size(cls, x: float, y: float, width: float, height: float) -> "Rect":
        """
        Creates a Rect instance using the specified position of the bottom-left corner and size.

        Parameters:
            float x:
                The x-coordinate of the bottom-left corner of the rectangle.
            float y:
                The y-coordinate of the bottom-left corner of the rectangle.
            float width:
                The width of the rectangle.
            float height:
                The height of the rectangle.

        Returns:
            Rect -> A new Rect instance defined by the given position and size.
        """
        return super().create_from_size(x, width, y, height)

    @classmethod
    def create_from_centre(cls, x: float, y: float, width: float, height: float) -> "Rect":
        """
        Create a Rect instance using the centre coordinates and dimensions.

        Parameters:
            float x:
                The x-coordinate of the centre of the rectangle.
            float y:
                The y-coordinate of the centre of the rectangle.
            float width:
                The width of the rectangle.
            float height:
                The height of the rectangle.

        Returns:
            Rect -> Instance centred on (x, y) with the specified width and height.
        """
        return super().create_from_centre(x, y, width, height)

    @classmethod
    def create_from_limits(cls, x_min: float, x_max: float, y_min: float, y_max: float) -> "Rect":
        """
        Create a Rect instance from the specified boundary limits.
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

        Returns:
            Rect -> A new instance of the Rect class defined by the given limits.
        """
        return super().create_from_limits(x_min, x_max, y_min, y_max)

    @classmethod
    def create_from_data(cls, x_data: Iterable[float], y_data: Iterable[float]) -> "Rect":
        """
        Create a Rect instance that encompasses the provided data.

        Parameters:
            Iterable[float] x_data:
                X-coordinates.
            Iterable[float] y_data:
                Y-coordinates.

        Returns:
            Rect -> A new instance of the Rect class that encompasses the data.
        """
        return super().create_from_data(x_data, y_data)

    @property
    def x(self) -> float:
        """
        The x-coordinate of the bottom-left corner of the rectangle.

        Returns:
            float -> The x-coordinate of the bottom-left corner.
        """
        return GenericRect.x.fget(self)

    @x.setter
    def _(self, value: float) -> None:
        return GenericRect.x.fset(self, value)

    @property
    def y(self) -> float:
        """
        The y-coordinate of the bottom-left corner of the rectangle.

        Returns:
            float -> The y-coordinate of the bottom-left corner.
        """
        return GenericRect.y.fget(self)

    @y.setter
    def _(self, value: float) -> None:
        return GenericRect.y.fset(self, value)

    @property
    def x1(self) -> float:
        """
        The x-coordinate of the top-right corner of the rectangle.

        Returns:
            float -> The x-coordinate of the top-right corner.
        """
        return GenericRect.x1.fget(self)

    @x1.setter
    def _(self, value: float) -> None:
        return GenericRect.x1.fset(self, value)

    @property
    def y1(self) -> float:
        """
        The y-coordinate of the top-right corner of the rectangle.

        Returns:
            float -> The y-coordinate of the top-right corner.
        """
        return GenericRect.y1.fget(self)

    @y1.setter
    def _(self, value: float) -> None:
        return GenericRect.y1.fset(self, value)

    @property
    def extent(self) -> tuple[float, float, float, float]:
        """
        The limits of the rectangle in the form (x_min, x_max, y_min, y_max).
        This corresponds to the format of a matplotlib 'extent' parameter.
        """
        return GenericRect.extent.fget(self)

    @property
    def range(self) -> tuple[tuple[float, float], tuple[float, float]]:
        """
        The limits of the rectangle in the form ((x_min, x_max), (y_min, y_max)).
        This corresponds to the format of a numpy histogram2d 'range' parameter.
        """
        return GenericRect.range.fget(self)

    @property
    def width(self) -> float:
        """
        The width of the rectangle.

        Returns:
            float -> The width of the rectangle.
        """
        return GenericRect.width.fget(self)

    @property
    def height(self) -> float:
        """
        The height of the rectangle.
        
        Returns:
            float -> The height of the rectangle.
        """
        return GenericRect.height.fget(self)

    @property
    def centre(self) -> tuple[float, float]:
        """
        The coordinates of the center of the rectangle.

        Returns:
            tuple[float, float] -> (x, y)
        """
        return GenericRect.centre.fget(self)

    @property
    def area(self) -> float:
        """
        The area of the rectangle.

        Returns:
            float -> The area of the rectangle.
        """
        return  GenericRect.area.fget(self)

    def __copy__(self) -> "Rect":
        """
        Create a shallow copy of the rectangle.

        Returns:
            Rect -> A new instance of the Rect class with the same properties.
        """
        return Rect(*self.extent)

    def __repr__(self) -> str:
        return "Rect: " + self.__str__()

    def __add__(self, value: IRect[T]) -> "Rect":
        return super().__add__(value)

    def __sub__(self, value: IRect[T]) -> "Rect":
        return super().__sub__(value)

    def __mul__(self, value: float) -> "Rect":
        return super().__mul__(value)

    def __div__(self, value: float) -> "Rect":
        return super().__div__(value)



class DiscreteRect(GenericRect[int]):
    """
    A 2D rectangle.

    Parameters:
        int x_min:
            X-coordinate of the bottom-left corner.
        int x_max:
            X-coordinate of the top-right corner.
        int y_min:
            Y-coordinate of the bottom-left corner.
        int y_max:
            Y-coordinate of the top-right corner.

    Use the following classmethods to create an instance:
        - create_from_size(x, y, width, height)
        - create_from_centre(x, y, width, height)
        - create_from_limits(x_min, x_max, y_min, y_max)
    """

    @classmethod
    def create_from_size(cls, x: int, y: int, width: int, height: int) -> "DiscreteRect":
        """
        Creates a DiscreteRect instance using the specified position of the bottom-left corner and size.

        Parameters:
            int x:
                The x-coordinate of the bottom-left corner of the rectangle.
            int y:
                The y-coordinate of the bottom-left corner of the rectangle.
            int width:
                The width of the rectangle.
            int height:
                The height of the rectangle.

        Returns:
            DiscreteRect -> A new DiscreteRect instance defined by the given position and size.
        """
        return super().create_from_size(x, y, width, height)
    
    @classmethod
    def create_from_centre(cls, x: int, y: int, width: int, height: int) -> "DiscreteRect":
        """
        Create a DiscreteRect instance using the centre coordinates and dimensions.
        In the event that the width or height are odd values, the upper bounds will be further from the centre by 1 then the lower bounds.

        Parameters:
            int x:
                The x-coordinate of the centre of the rectangle.
            int y:
                The y-coordinate of the centre of the rectangle.
            int width:
                The width of the rectangle.
            int height:
                The height of the rectangle.

        Returns:
            DiscreteRect -> Instance centred on (x, y) with the specified width and height.
        """
        return cls(math.floor(x - width / 2), math.ceil(x + width / 2), math.floor(y - height / 2), math.ceil(y + height / 2))
    
    @classmethod
    def create_from_limits(cls, x_min: int, x_max: int, y_min: int, y_max: int) -> "DiscreteRect":
        """
        Create a DiscreteRect instance from the specified boundary limits.
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

        Returns:
            DiscreteRect -> A new instance of the DiscreteRect class defined by the given limits.
        """
        return super().create_from_limits(x_min, x_max, y_min, y_max)
    
    @classmethod
    def create_from_data(cls, x_data: Iterable[int], y_data: Iterable[int]) -> "DiscreteRect":
        """
        Create a DiscreteRect instance that encompasses the provided data.

        Parameters:
            Iterable[int] x_data:
                X-coordinates.
            Iterable[int] y_data:
                Y-coordinates.

        Returns:
            DiscreteRect -> A new instance of the DiscreteRect class that encompasses the data.
        """
        return super().create_from_data(x_data, y_data)

    @property
    def x(self) -> int:
        """
        The x-coordinate of the bottom-left corner of the rectangle.

        Returns:
            int -> The x-coordinate of the bottom-left corner.
        """
        return GenericRect.x.fget(self)

    @x.setter
    def _(self, value: int) -> None:
        return GenericRect.x.fset(self, value)

    @property
    def y(self) -> int:
        """
        The y-coordinate of the bottom-left corner of the rectangle.

        Returns:
            int -> The y-coordinate of the bottom-left corner.
        """
        return GenericRect.y.fget(self)

    @y.setter
    def _(self, value: int) -> None:
        return GenericRect.y.fset(self, value)

    @property
    def x1(self) -> int:
        """
        The x-coordinate of the top-right corner of the rectangle.

        Returns:
            int -> The x-coordinate of the top-right corner.
        """
        return GenericRect.x1.fget(self)

    @x1.setter
    def _(self, value: int) -> None:
        return GenericRect.x1.fset(self, value)

    @property
    def y1(self) -> int:
        """
        The y-coordinate of the top-right corner of the rectangle.

        Returns:
            int -> The y-coordinate of the top-right corner.
        """
        return GenericRect.y1.fget(self)

    @y1.setter
    def _(self, value: int) -> None:
        return GenericRect.y1.fset(self, value)

    @property
    def extent(self) -> tuple[int, int, int, int]:
        """
        The limits of the rectangle in the form (x_min, x_max, y_min, y_max).
        This corresponds to the format of a matplotlib 'extent' parameter.
        """
        return GenericRect.extent.fget(self)

    @property
    def range(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        The limits of the rectangle in the form ((x_min, x_max), (y_min, y_max)).
        This corresponds to the format of a numpy histogram2d 'range' parameter.
        """
        return GenericRect.range.fget(self)

    @property
    def width(self) -> int:
        """
        The width of the rectangle.

        Returns:
            int -> The width of the rectangle.
        """
        return GenericRect.width.fget(self)

    @property
    def height(self) -> int:
        """
        The height of the rectangle.
        
        Returns:
            int -> The height of the rectangle.
        """
        return GenericRect.height.fget(self)

    @property
    def centre(self) -> tuple[int, int]:
        """
        The coordinates of the center of the rectangle.

        Returns:
            tuple[int, int] -> (x, y)
        """
        return (math.floor((self.__x_max + self.__x_min) / 2), math.floor((self.__y_max + self.__y_min) / 2))

    @property
    def area(self) -> int:
        """
        The area of the rectangle.

        Returns:
            int -> The area of the rectangle.
        """
        return  GenericRect.area.fget(self)

    def __copy__(self) -> "DiscreteRect":
        """
        Create a shallow copy of the rectangle.

        Returns:
            DiscreteRect -> A new instance of the DiscreteRect class with the same properties.
        """
        return DiscreteRect(*self.extent)

    def __repr__(self) -> str:
        return "DiscreteRect: " + self.__str__()

    def __add__(self, value: IRect[T]) -> "DiscreteRect":
        return super().__add__(value)

    def __sub__(self, value: IRect[T]) -> "DiscreteRect":
        return super().__sub__(value)

    def __mul__(self, value: float) -> "DiscreteRect":
        return type(self).create_from_size(
            self.x,
            self.y,
            math.floor(self.width * value),
            math.floor(self.height * value)
        )

    def __imul__(self, value: float) -> None:
        self.x1 = self.x + math.floor(self.width * value)
        self.y1 = self.y + math.floor(self.height * value)

    def __div__(self, value: float) -> "DiscreteRect":
        return type(self).create_from_size(
            self.x,
            self.y,
            math.floor(self.width / value),
            math.floor(self.height / value)
        )

    def __idiv__(self, value: float) -> None:
        self.x1 = self.x + math.floor(self.width / value)
        self.y1 = self.y + math.floor(self.height / value)
