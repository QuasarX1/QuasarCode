from abc import ABC, abstractmethod
from functools import wraps
from typing import Generic, TypeVar, Union, Tuple, Iterable, Callable, Any
from typing_extensions import ParamSpec, Concatenate

P = ParamSpec("P")
T = TypeVar("T")

class TypeShield_Base(Generic[T], ABC):

    @abstractmethod
    def report_format_types(self) -> str:
        raise NotImplementedError("Attempted to call abstract method.")

    @abstractmethod
    def check_type(self, value: Any) -> bool:
        raise NotImplementedError("Attempted to call abstract method.")

    def __str__(self) -> str:
        return self.report_format_types()

    def __call__(self, func: Callable[Concatenate[Any, P], T]):
        @wraps(func)
        def wrapper(value: Any, *args: P.args, **kwargs: P.kwargs) -> T:
            if self.check_type(value):
                return func(value, *args, **kwargs)
            raise TypeError(f"Attepted to assign value with incorrect type: {type(value).__qualname__} and any parent class(es) not in {self}.")
        return wrapper

class TypeShield(TypeShield_Base[T]):
    """
    Produces a function wrapper that restricts the type of the first argument.

    Many types may be specified.

    Usage:

    @TypeShield[Collection](tuple, list, numpy.ndarray, unyt.unyt_array)
    def my_func(val: Collection): pass
    """

    def __init__(self, *allowed_types: type):
        self.__allowed_types: Tuple[type] = allowed_types

        # If nothing specified, apply a dummy guard type
        if len(self.__allowed_types) == 0:
            self.__allowed_types = (object,)

    @property
    def allowed_types(self) -> Tuple[type]:
        """
        Types permitted by the TypeShield.
        """
        return self.__allowed_types

    def report_format_types(self) -> str:
        return f"TypeShield({', '.join([t.__qualname__ for t in self.__allowed_types])})"

    def check_type(self, value: Any) -> bool:
        for valid_target_type in self.__allowed_types:
            if isinstance(value, valid_target_type):
                return True
        return False

class NestedTypeShield(TypeShield_Base[T]):
    """
    Produces a function wrapper that restricts the type of the first argument by checking the types of the argument's substructure.
    For nested datatypes, this checks only the depth of the leftermost branches and NOT the whole dataset!
    For dictionary substructure, only test_dict[tuple(test_dict.keys())[0]] will be type checked.

    Many types may be specified at each level.

    Usage:

    @TypeShield[Collection[Union[Tuple[np.ndarray, ...], List[np.ndarray]]]](Collection, [tuple, list], np.ndarray, float)
    def my_func(val: Collection[Collection[np.ndarray]]): pass
    """

    def __init__(self, *allowed_type_layers: Union[type, Iterable[Union[type, None]], None]):
        self.__allowed_type_layers: Tuple[Tuple[Union[type, None], ...], ...] = tuple([(None,) if v is None else (v,) if isinstance(v, type) else tuple(v) if len(v) > 0 else (object,) for v in allowed_type_layers])

        # If nothing specified, apply a dummy guard type
        if len(self.__allowed_type_layers) == 0:
            self.__allowed_type_layers = ((object,),)

    @property
    def allowed_types(self) -> Tuple[Tuple[Union[type, None], ...], ...]:
        """
        Types permitted by the TypeShield.
        """
        return self.__allowed_type_layers

    def report_format_types(self, subset = None) -> str:
        chunk = f"{'(' if subset is None else '{'}{(' -> ' if subset is None else ', ').join([t.__qualname__ if len(t) == 1 else self.report_format_types(subset = t) for t in (self.__allowed_type_layers if subset is None else subset)])}{')' if subset is None else '}'}"
        return f"TypeShield({chunk})" if subset is None else chunk

    def check_type(self, value: Any, level = 0) -> bool:
        valid = False
        for valid_target_type in self.__allowed_type_layers[level]:
            if isinstance(value, valid_target_type):
                valid = True
                break

        return (self.check_type(value[tuple(value.keys())[0]] if isinstance(value, dict) else value[0], level = level) if level < len(self) - 1 else True) if valid else level
