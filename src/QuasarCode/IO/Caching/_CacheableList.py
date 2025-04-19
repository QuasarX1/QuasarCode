from typing import Any, Iterable
from ._Cacheable import Cacheable

class CacheableList(list, Cacheable):
    """
    A list of cacheable objects.
    
    This class is used to handle a list of cacheable objects, allowing for the 
    serialization and deserialization of the list as a whole.
    
    Attributes:
        list[Cacheable] _cacheable_list:
            The list of cacheable objects.
    """
    
    def __init__(self, iterable: Iterable[Cacheable]) -> None:
        super().__init__(iterable)

    @classmethod
    def __from_cache_data__(cls, data: dict[str, Any]) -> "CacheableList":
        """
        Load the list of cacheable objects from a cache target.
        
        Parameters:
            dict[str, Any] data:
                The data to load the list of cacheable objects from.
        
        Returns:
            CacheableList -> The loaded list of cacheable objects.
        """
        number_of_items: int = data["count"]
        return cls([data["types"][i].__from_cache_data__(data["data"]) for i in range(number_of_items)])

    def __get_cache_data__(self) -> dict[str, Any]:
        return {
            "count": len(self),
            "types": [type(item) for item in self],
            "data": [item.__get_cache_data__() for item in self],
        }
