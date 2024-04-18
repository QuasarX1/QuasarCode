from typing import Generic, TypeVar, Callable, Any
from typing_extensions import ParamSpec, Concatenate

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

    def __call__(self, value: Any) -> T:
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
