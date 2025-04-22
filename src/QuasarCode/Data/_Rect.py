from decimal import Decimal

import numpy as np


class Rect:
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

    Use the following static methods to create an instance:
        - create_from_size(x, y, width, height)
        - create_from_center(x, y, width, height)
        - create_from_limits(x_min, x_max, y_min, y_max)
    """
    def __init__(self, x_min: float, x_max: float, y_min: float, y_max: float):
        self.__x_min = x_min
        self.__x_max = x_max
        self.__y_min = y_min
        self.__y_max = y_max

    @staticmethod
    def create_from_size(x: float, y: float, width: float, height: float) -> "Rect":
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
        return Rect(x, x + width, y, y + height)

    @staticmethod
    def create_from_center(x: float, y: float, width: float, height: float) -> "Rect":
        """
        Create a Rect instance using the center coordinates and dimensions.

        Parameters:
            float x:
                The x-coordinate of the center of the rectangle.
            float y:
                The y-coordinate of the center of the rectangle.
            float width:
                The width of the rectangle.
            float height:
                The height of the rectangle.

        Returns:
            Rect -> Instance centred on (x, y) with the specified width and height.
        """
        return Rect(x - width / 2, x + width / 2, y - height / 2, y + height / 2)

    @staticmethod
    def create_from_limits(x_min: float, x_max: float, y_min: float, y_max: float) -> "Rect":
        """
        Create a Rect instance from the specified boundary limits.

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
        return Rect(x_min, x_max, y_min, y_max)

    @property
    def extent(self) -> tuple[float, float, float, float]:
        """
        The limits of the rectangle in the form (x_min, x_max, y_min, y_max).
        This is the same as the constructor parameters and is implemented for consistency.
        This corresponds to the format of a matplotlib 'extent' parameter.
        """
        return (self.__x_min, self.__x_max, self.__y_min, self.__y_max)

    @property
    def width(self) -> float:
        """
        The width of the rectangle.

        Returns:
            float -> The width of the rectangle.
        """
        return self.__x_max - self.__x_min

    @property
    def height(self) -> float:
        """
        The height of the rectangle.
        
        Returns:
            float -> The height of the rectangle.
        """
        return self.__y_max - self.__y_min

    @property
    def centre(self) -> tuple[float, float]:
        """
        The coordinates of the center of the rectangle.

        Returns:
            tuple[float, float] -> (x, y)
        """
        return ((self.__x_max + self.__x_min) / 2, (self.__y_max + self.__y_min) / 2)

    @property
    def area(self) -> float:
        """
        The area of the rectangle.

        Returns:
            float -> The area of the rectangle.
        """
        return self.width * self.height

    def __copy__(self) -> "Rect":
        """
        Create a shallow copy of the rectangle.

        Returns:
            Rect -> A new instance of the Rect class with the same properties.
        """
        return Rect(self.__x_min, self.__x_max, self.__y_min, self.__y_max)
    
    def __str__(self) -> str:
        return f"Rect(x: {self.__x_min} -> {self.__x_max}, y: {self.__y_min} -> {self.__y_max})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, value):
        if isinstance(value, Rect):
            return self.__x_min == value.__x_min and self.__x_max == value.__x_max and self.__y_min == value.__y_min and self.__y_max == value.__y_max
        return False
    
    def __ne__(self, value):
        return not self.__eq__(value)
    
    def __gt__(self, value):
        if isinstance(value, Rect):
            return self.area > value.area
        elif isinstance(value, (int, float, Decimal, np.integer, np.floating)):
            return self.area > value
        return False
    
    def __ge__(self, value):
        if isinstance(value, Rect):
            return self.area >= value.area
        elif isinstance(value, (int, float, Decimal, np.integer, np.floating)):
            return self.area >= value
        return False
    
    def __lt__(self, value):
        if isinstance(value, Rect):
            return self.area < value.area
        elif isinstance(value, (int, float, Decimal, np.integer, np.floating)):
            return self.area < value
        return False
    
    def __le__(self, value):
        if isinstance(value, Rect):
            return self.area <= value.area
        elif isinstance(value, (int, float, Decimal, np.integer, np.floating)):
            return self.area <= value
        return False
