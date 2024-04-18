from typing import Generic, TypeVar, Union, Any

from .cast import Cast

class AutoProperty(property):
    def __init__(self, doc: Union[str, None] = None) -> None:
        self.__name: Union[str, None] = None
        self.__declaring_type_name: Union[str, None] = None
        super().__init__(doc = doc)

    def __set_name__(self, owner, name):
        self.__declaring_type_name = owner.__qualname__
        self.__name = name

    @property
    def _name(self) -> Union[str, None]:
        return self.__name

    def __get_storage_attribute_name(self):
        return f"_{self.__declaring_type_name}__autoprop_{self.__name}"
    
    def _initialise(self, instance: Any):
        setattr(instance, self.__get_storage_attribute_name(), None)

    def __get__(self, instance: Any, owner: Union[type, None] = None, /) -> Any:
        return getattr(instance, self.__get_storage_attribute_name())

    def __set__(self, instance: Any, value: Any, /) -> None:
        setattr(instance, self.__get_storage_attribute_name(), value)

#    @staticmethod
#    def init_autoproperties(instance: Any, instance_type: type) -> None:
#        for attribute in [vars(instance_type)[attribute_name] for attribute_name in vars(instance_type)]:
#            if isinstance(attribute, AutoProperty):
#                attribute._initialise(instance)


T = TypeVar("T")
class TypeCast_AutoProperty(AutoProperty, Generic[T]):
    def __init__(self, cast: Cast[T], doc: Union[str, None] = None) -> None:
        self.__cast: Cast[T] = cast
        super().__init__(doc)

    def __set__(self, instance: Any, value: Any, /) -> None:
        super().__set__(instance, self.__cast(value))
