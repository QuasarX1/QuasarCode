from ...Tools._edit_locals import use_locals

from typing import TypeVar, ParamSpec
from collections.abc import Callable
from functools import wraps



P = ParamSpec("P")
T = TypeVar("T")



@use_locals(0, 0)
def synchronyse(target: T, /, root: int = 0, comm: object|None = None) -> T:
    return target



def if_mpi_root(default: T, root: int|None = None):
    def inner(func: Callable[P, T]) -> Callable[P, T]:
        return func
    return inner
