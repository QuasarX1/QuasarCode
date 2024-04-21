import numpy as np
from typing import Union, Generic, TypeVar, Callable, Iterable, Sized, SupportsIndex, Collection, Sequence, Dict, Any, cast
from typing_extensions import ParamSpec, Concatenate
from unyt import unyt_array

P = ParamSpec("P")
T = TypeVar("T")
class Cast(Generic[T]):
    def __init__(self, cast_func: Callable[Concatenate[Any, P], T], *args: P.args, nullable: bool = False, **kwargs: P.kwargs) -> None:
        self.__target_func = cast_func
        self.__nullable = nullable
        self.__args = args
        self.__kwargs = kwargs

    @property
    def nullable(self) -> bool:
        return self.__nullable

    def __call__(self, value: Any) -> Union[T, None]:
        return None if value is None and self.__nullable else self.__target_func(value, *self.__args, **self.__kwargs)
    
    @staticmethod
    def passthrough() -> "Cast[None]":
        return Cast(lambda o, *args, **kwargs: o, nullable = True)



def non_nullable_cast(cast_func: Callable[Concatenate[Any, P], T], *args: P.args, **kwargs: P.kwargs) -> Cast[T]:
    """
    Creates a wrapper function that allows other arguments to be passed to a cast function.
    None values are passed through to the function!
    """
    return Cast(cast_func, nullable = False, *args, **kwargs)

def nullable_cast(cast_func: Callable[Concatenate[Any, P], T], *args: P.args, **kwargs: P.kwargs) -> Cast[T]:
    """
    Creates a wrapper function that allows None values to bypass a cast function.

    value is None:     return None
    value is NOT None: apply cast
    """
    return Cast(cast_func, nullable = True, *args, **kwargs)

class NestedCast(Cast[T]):
    def __init__(self, *layer_cast_funcs: Union[Callable[..., Any], Cast], nullable: bool = False, layer_args: Union[Sequence[Union[Collection[Any], None]], None] = None, layer_kwargs: Union[Sequence[Union[Dict[str, Any], None]], None] = None) -> None:
        self.__target_layer_funcs = layer_cast_funcs
        self.__last_layer_index = len(self.__target_layer_funcs) - 1

        if layer_args is None:
            layer_args = [None for _ in range(len(self.__target_layer_funcs))]
        if layer_kwargs is None:
            layer_kwargs = [None for _ in range(len(self.__target_layer_funcs))]

        super().__init__(self._traverse_nest, layer_args, layer_kwargs)

    def _traverse_nest(self, value: Any, layer_args: Sequence[Union[Collection[Any], None]], layer_kwargs: Sequence[Union[Dict[str, Any], None]], layer: int = 0):
        if layer != self.__last_layer_index and isinstance(value, Sized) and isinstance(value, SupportsIndex):
            if isinstance(value, unyt_array):
                value = list(value.value) # The target must not have attached units as this might brake on looking at the values!
            if isinstance(value, np.ndarray):
                value = list(value) # The target must not be a ndarray as this will mutate the cast elements when returned to the target!
            if isinstance(value, tuple):
                value = list(value) # The target must be mutable!
            for i, inner_value in enumerate(value):
                value[i] = self._traverse_nest(inner_value, layer_args, layer_kwargs, layer = layer + 1)

        args = cast(Collection[Any], layer_args[layer] if layer_args[layer] is not None else [])
        kwargs = cast(Dict[str, Any], layer_kwargs[layer] if layer_kwargs[layer] is not None else {})
        return self.__target_layer_funcs[layer](value, *args, **kwargs)
