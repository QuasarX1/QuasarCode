from ...Tools._edit_locals import use_locals

from typing import TypeVar, ParamSpec
from collections.abc import Callable, Sized, Sequence
from functools import wraps



P = ParamSpec("P")
T = TypeVar("T")



@use_locals(0, 0)
def synchronyse(target: T, /, root: int = 0, comm: object|None = None) -> T:
    """
    Broadcast the value of a variable on the root rank to the same variable on all ranks in the communicator.

    The first argument should be a string containing the variable name NOT the value of the variable!
    """
    return target



def if_mpi_root(default: T, root: int|None = None):
    """
    Function decorator for restricting calls to the root rank.

    A default return value of the appropriate return type must be provided (this can be None if the wrapped function allows it or specifies no return type).
    """
    def inner(func: Callable[P, T]) -> Callable[P, T]:
        return func
    return inner



def mpi_barrier(comm: object|None = None) -> None:
    """
    Wait for all ranks in the communicator to reach this barrier.
    """
    pass



def mpi_get_slice(length: int|Sized, comm: object|None = None, rank: int|None = None) -> slice:
    """
    Partition a set of data such that it is distributed evenly accross each MPI rank.

    This method can be used to help get data from a h5py dataset when using parallel IO.

    Parameters:
                 int|Sized length -> The length of the target data or the target data if a size can be derived from it.
        MPI.Intracomm|None comm   -> Optional MPI communicator object (defaults to the one from MPI_Config).
                  int|None comm   -> Optional MPI rank (defaults to the one from MPI_Config if not comm is specified or the one from the provided comm).

    Returns:
        slice -> A slice object that can be applied a Sequence of the appropriate length.
    """
    if not isinstance(length, int):
        length = len(length)
    return slice(0, length)



def mpi_slice(data: Sequence[T], comm: object|None = None, rank: int|None = None) -> Sequence[T]:
    """
    Partition a set of data such that it is distributed evenly accross each MPI rank.

    This method can be used to quickly get data from a h5py dataset when using parallel IO.

    Parameters:
                  Sequence data -> Data to be partitioned.
        MPI.Intracomm|None comm -> Optional MPI communicator object (defaults to the one from MPI_Config).
                  int|None comm -> Optional MPI rank (defaults to the one from MPI_Config if not comm is specified or the one from the provided comm).

    Returns:
        Sequence -> Section of the data assigned to the calling rank.
    """
    return data[:]
