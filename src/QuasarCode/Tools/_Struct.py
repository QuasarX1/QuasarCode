from typing import Union, Collection, TypeVar, Type, Any

from ..IO.Caching._Cacheable import Cacheable

class Struct(object):
    """
    Structure type definition.
    Allows a number of public instance attributes to be declared and populated from the constructor.

    Constructor Design Order:
        1.) Declare all public attributes first.
        2.) super().__init__(**kwargs)

    To specify a human readable type name for errors, overload: _get_typename(self) -> Union[str, None]
    To specify type casts for attributes, set fields to an instance of TypeCastAutoProperty
    """
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
            except AttributeError as e:
                raise AttributeError(f"{self._get_typename if self._get_typename is not None else type(self).__qualname__} struct defines no public field named \"{key}\".") from e

    @staticmethod
    def _get_typename() -> Union[str, None]:
        """
        Overload this to specify a string to appear in the error message provided when attempting to initalise a nonexistant attribute.
        """
        return None



T = TypeVar("T", bound = "CacheableStruct")

class CacheableStruct(Struct, Cacheable):
    """
    Structure type definition.
    Allows a number of public instance attributes to be declared and populated from the constructor.

    Constructor Design Order:
        1.) Declare all public attributes first.
        2.) super().__init__(cacheable_attributes = [<attribute-names>], **kwargs)
            where <attribute-names> is a list of the attributes that should be cached.

    To specify a human readable type name for errors, overload: _get_typename(self) -> Union[str, None]
    To specify type casts for attributes, set fields to an instance of TypeCastAutoProperty
    """
    
    def __init__(self, cacheable_attributes: Collection[str], **kwargs):
        self.__cacheable_attributes: tuple[str, ...] = tuple(cacheable_attributes)
        super().__init__(**kwargs)

    @classmethod
    def __from_cache_data__(cls: Type[T], data: dict[str, Any]) -> T:
        instance = cls(data.keys())
        for attribute_name in data:
            if attribute_name not in data:
                raise KeyError(f"Cache data is missing required attribute \"{attribute_name}\".")
            setattr(instance, attribute_name, data[attribute_name] if not isinstance(data[attribute_name], dict) or "datatype" not in data[attribute_name] else data[attribute_name]["datatype"].__from_cache_data__(data[attribute_name]["data"]))
            if isinstance(getattr(instance, attribute_name), dict):
                for sub_key in getattr(instance, attribute_name):
                    if isinstance(getattr(instance, attribute_name)[sub_key], dict) and "datatype" in getattr(instance, attribute_name)[sub_key]:
                        getattr(instance, attribute_name)[sub_key] = getattr(instance, attribute_name)[sub_key]["datatype"].__from_cache_data__(getattr(instance, attribute_name)[sub_key]["data"])
        return instance

    def __get_cache_data__(self) -> dict[str, Any]:
        data = {
            attribute_name : getattr(self, attribute_name)
            for attribute_name
            in self.__cacheable_attributes
        }
        for key in data:
            if isinstance(data[key], Cacheable):
                data[key] = { "datatype" : type(data[key]), "data" : data[key].__get_cache_data__() }
            elif isinstance(data[key], dict):
                contains_cacheable = False
                for sub_key in data[key]:
                    if isinstance(data[key][sub_key], Cacheable):
                        contains_cacheable = True
                        data[key][sub_key] = { "datatype" : type(data[key][sub_key]), "data" : data[key][sub_key].__get_cache_data__() }
                if contains_cacheable:
                    data[key]["has_cacheables"] = True
        return data
