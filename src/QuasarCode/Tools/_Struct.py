from abc import abstractmethod
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
        instance = cls()
        for attribute_name in data:
            if attribute_name == "__has_cacheables":
                continue
            attribute_data = data[attribute_name] if not isinstance(data[attribute_name], dict) or "datatype" not in data[attribute_name] else data[attribute_name]["datatype"].__from_cache_data__(data[attribute_name]["data"])
            if isinstance(attribute_data, dict) and "__has_cacheables" in attribute_data:
                loaded_attribute_data = attribute_data
                attribute_data = {}
                for sub_key in loaded_attribute_data:
                    if sub_key == "__has_cacheables":
                        continue#TODO: why is this needed again???
                    actual_subkey = sub_key if not isinstance(sub_key, dict) or "__key_needs_loading" not in loaded_attribute_data[sub_key] else sub_key["datatype"].__from_cache_data__(sub_key["data"])
                    actual_value: Any
                    if isinstance(loaded_attribute_data[sub_key], dict) and "datatype" in loaded_attribute_data[sub_key]:
                        actual_value = loaded_attribute_data[sub_key]["datatype"].__from_cache_data__(loaded_attribute_data[sub_key]["data"])
                    else:
                        actual_value = loaded_attribute_data[sub_key]
                    attribute_data[actual_subkey] = actual_value
                #attribute_data.pop("__has_cacheables")
            setattr(instance, attribute_name, attribute_data)
        return instance

    def __get_cache_data__(self) -> dict[str, Any]:
        data = {}
        for attribute_name in self.__cacheable_attributes:

            attribute_data = getattr(self, attribute_name)

            if isinstance(attribute_data, Cacheable):
                data[attribute_name] = { "datatype" : type(attribute_data), "data" : attribute_data.__get_cache_data__() }

            elif isinstance(attribute_data, dict):
                data_to_save: dict[Any, Any] = {}

                contains_cacheable = False

                for attr_data_key in attribute_data:
                    if isinstance(attr_data_key, Cacheable) or isinstance(attribute_data[attr_data_key], Cacheable):
                        contains_cacheable = True
                        key_is_cacheable = isinstance(attr_data_key, Cacheable)
                        key = attr_data_key if not key_is_cacheable else { "datatype": type(attr_data_key), "data": attr_data_key.__get_cache_data__() }
                        value = attribute_data[attr_data_key] if not isinstance(attribute_data[attr_data_key], Cacheable) else attribute_data[attr_data_key].__get_cache_data__()
                        data_to_save[key] = { "datatype": type(attribute_data[attr_data_key]), "data": value }
                        data_to_save[key]["__key_needs_loading"] = key_is_cacheable
                    else:
                        data_to_save[attr_data_key] = attribute_data[attr_data_key]

                if contains_cacheable:
                    data_to_save["__has_cacheables"] = True

                data[attribute_name] = data_to_save

            else:
                data[attribute_name] = attribute_data

        return data
