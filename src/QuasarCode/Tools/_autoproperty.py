from typing import Generic, TypeVar, Union, Iterable, Callable, Any, cast

from ._cast import Cast
from ._typeshield import TypeShield_Base

T = TypeVar("T")

class AutoProperty(property, Generic[T]):
    """
    Automation of the property type that automatically handles the creation of a hidden attribute.

    Uninitialised properties are assigned None and are considered uninitialised (i.e. like NULLPTR).

    Calling the deleter will uninitialise the value back to None.

    Constructor:
        str | None doc                 -> Optional documentation string for the property. Defaults to None.
              bool allow_uninitialised -> If the property is unititialised, should None be returned upon attempting to access the value? Default is False.
    """
    
    def __init__(self, default_value: Union[T, None] = None, doc: Union[str, None] = None, allow_uninitialised: bool = False) -> None:
        self.__name: Union[str, None] = None
        self.__declaring_type_name: Union[str, None] = None
        self.__check_uninitialised: bool = not (allow_uninitialised or default_value is not None)
        self.__default_value = default_value
        super().__init__(doc = doc)

    def __set_name__(self, owner, name):
        self.__declaring_type_name = owner.__qualname__
        self.__name = name

    @property
    def _name(self) -> Union[str, None]:
        return self.__name
    
    def is_initialised(self, instance: Any) -> Union[bool, None]:
        if self.__check_uninitialised:
            initilised: Union[bool, None] = None
            try:
                initilised = cast(bool, getattr(instance, self.__get_storage_attribute_name() + "__isinit"))
            except AttributeError:
                initilised = False
                setattr(instance, self.__get_storage_attribute_name() + "__isinit", False)
            return initilised
        else:
            return None

    def __get_storage_attribute_name(self):
        return f"_{self.__declaring_type_name}__autoprop_{self.__name}"

    def __get__(self, instance: Any, owner: Union[type, None] = None, /) -> Union[T, None]:
        if self.__check_uninitialised:
            if not self.is_initialised(instance):
                raise ValueError("Attempted to access value of uninitialised AutoProperty with initialisation enforcement enabled.")

        try:
            return getattr(instance, self.__get_storage_attribute_name())
        except AttributeError:
            setattr(instance, self.__get_storage_attribute_name(), self.__default_value)
            return getattr(instance, self.__get_storage_attribute_name())

    def __set__(self, instance: Any, value: Any, /) -> None:
        setattr(instance, self.__get_storage_attribute_name(), value)
        if self.__check_uninitialised:
            setattr(instance, self.__get_storage_attribute_name() + "__isinit", True)

    def __delete__(self, instance: Any, /) -> None:
        setattr(instance, self.__get_storage_attribute_name(), None)
        if self.__check_uninitialised:
            setattr(instance, self.__get_storage_attribute_name() + "__isinit", False)

class AutoProperty_NonNullable(AutoProperty[T]):
    """
    Automation of the property type that automatically handles the creation of a hidden attribute.
    A value must be assigned before attempting to read from a property of this type.
    Attempting to read from an uninitialised property will result in a ValueError.

    Syntactic sugar for AutoProperty(..., allow_uninitialised = False)
    Also adds a more appropriate type hint for the underlying property __get__ method.

    Calling the deleter will uninitialise the value making the property unreadable.

    Constructor:
        str | None doc -> Optional documentation string for the property. Defaults to None.
    """

    def __init__(self, default_value: Union[T, None] = None, doc: Union[str, None] = None) -> None:
        super().__init__(default_value = default_value, doc = doc, allow_uninitialised = False)

    def __get__(self, instance: Any, owner: Union[type, None] = None, /) -> T:
        return cast(T, super().__get__(instance, owner))

class NullableTypedAutoProperty(AutoProperty[T]):
    """
    Automation of the property type that automatically handles the creation of a hidden attribute.

    Uninitialised properties are assigned None by default.

    Calling the deleter will uninitialise the value back to None.

    TypeParam:
        T -> The type of the property's value (when initialised).

    Constructor:
        TypeShield_Base type_shield -> Type objects (and None) that are considered valid types for the property's value.
             str | None doc         -> Optional documentation string for the property. Defaults to None.
    """

    def __init__(self, type_shield: TypeShield_Base, default_value: Union[T, None] = None, doc: Union[str, None] = None) -> None:
        self.__valid_type_definition_shield = type_shield
        super().__init__(default_value = default_value, doc = doc, allow_uninitialised = True)

    def __set__(self, instance: Any, value: Any, /) -> None:
        super().__set__(instance, self.__valid_type_definition_shield.shield_check(value) if value is not None else None)

class TypedAutoProperty(AutoProperty_NonNullable[T]):
    """
    Automation of the property type that automatically handles the creation of a hidden attribute.

    Uninitialised properties are assigned None and are considered uninitialised (i.e. like NULLPTR).

    Calling the deleter will uninitialise the value back to None.

    TypeParam:
        T -> The type of the property's value (when initialised).

    Constructor:
        TypeShield_Base type_shield -> Type objects (and None) that are considered valid types for the property's value.
             str | None doc         -> Optional documentation string for the property. Defaults to None.
    """

    def __init__(self, type_shield: TypeShield_Base, default_value: Union[T, None] = None, doc: Union[str, None] = None) -> None:
        self.__valid_type_definition_shield = type_shield
        super().__init__(default_value = default_value, doc = doc)

    def __set__(self, instance: Any, value: Any, /) -> None:
        super().__set__(instance, self.__valid_type_definition_shield.shield_check(value))

class TypeCastAutoProperty(AutoProperty[T]):
    """
    Automation of the property type that automatically handles the creation of a hidden attribute.

    Uninitialised properties are assigned None and are considered uninitialised (i.e. like NULLPTR).

    Calling the deleter will uninitialise the value back to None.

    TypeParam:
        T -> The return type of the cast operation. Also the type of the property's value (when initialised).

    Constructor:
        str | None doc                 -> Optional documentation string for the property. Defaults to None.
              bool allow_uninitialised -> If the property is unititialised, should None be returned upon attempting to access the value? Default is False.
    """

    def __init__(self, cast: Union[Cast[T], Callable[[Any], T]], default_value: Union[T, None] = None, doc: Union[str, None] = None) -> None:
        self.__cast: Union[Cast[T], Callable[[Any], T]] = cast
        super().__init__(default_value = default_value, doc = doc, allow_uninitialised = cast.nullable if isinstance(cast, Cast) else False)

    def __set__(self, instance: Any, value: Any, /) -> None:
        super().__set__(instance, self.__cast(value))
