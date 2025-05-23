from abc import ABC, abstractmethod
from typing import Any, TypeVar, Type

T = TypeVar("T", bound = "Cacheable")

class Cacheable(ABC):
    """
    Marks an object as being cacheable using a CacheTarget.

    Abstract Methods:
        __from_cache_data__
        __get_cache_data__
    """

    @classmethod
    @abstractmethod
    def __from_cache_data__(cls: Type[T], data: dict[str, Any]) -> T:
        """
        Load the object from a cache target.

        Parameters:
            dict[str, Any] data:
                The data to load the object from.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    @abstractmethod
    def __get_cache_data__(self) -> dict[str, Any]:
        """
        Get the data to be cached.

        Returns:
            dict[str, Any] -> The data to be cached.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")
