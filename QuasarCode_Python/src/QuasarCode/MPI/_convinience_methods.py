from ._mpi_configs import mpi_config as MPI_Config
from ..Tools._edit_locals import use_locals

from typing import TypeVar, ParamSpec
from collections.abc import Callable
from mpi4py import MPI
from functools import wraps



P = ParamSpec("P")
T = TypeVar("T")



@use_locals(0, 0)
def synchronyse(target: T, /, root: int|None = None, comm: MPI.Intracomm|None = None) -> T:
    if root == None:
        root = MPI_Config.root
    if comm == None:
        comm = MPI_Config.comm
    return comm.bcast(target, root)



def if_mpi_root(default: T, root: int|None = None):
    if root == None:
        root = MPI_Config.root
    def inner(func: Callable[P, T]) -> Callable[P, T]:
        @wraps
        def wrapper(*args: P.args, **kwargs: P.kwargs):
            if MPI_Config.rank == root:
                return func(*args, **kwargs)
            else:
                return default
        return wrapper
    return inner
