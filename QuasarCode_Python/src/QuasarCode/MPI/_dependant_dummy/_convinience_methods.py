from ...Tools._edit_locals import use_locals

from typing import TypeVar, ParamSpec
from collections.abc import Callable, Sized, Sequence
from functools import wraps

import numpy as np



P = ParamSpec("P")
T = TypeVar("T")



@use_locals(0, 0)
def synchronyse(target: T, /, root: int = 0, comm: object|None = None) -> T:
    """
    Broadcast the value of a variable on the root rank to the same variable on all ranks in the communicator.

    The first argument should be a string containing the variable name NOT the value of the variable!
    """
    return target



def mpi_check_equal(value: T, /, root: int|None = None, comm: object|None = None) -> bool:
    """
    Check all ranks have the same value.
    """
    return True



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



def mpi_gather_array(data: np.ndarray, comm: object|None = None, root: int|None = None, target_buffer: np.ndarray|None = None) -> np.ndarray:
    """
    Gather numpy array data to the root rank.
    If the resulting array is larger than the MPI buffer length, data will be transmitted point-to-point in rank order instead of using the Gatherv method.
    """
    if target_buffer is None:
        return data
    else:
        target_buffer[:] = data[:]
        return target_buffer



def mpi_scatter_array(data: np.ndarray|None, elements_this_rank: int|None = None, elements_per_rank: list[int]|None = None, comm: object|None = None, root: int|None = None, target_buffer: np.ndarray|None = None) -> np.ndarray:
    """
    Scatter numpy array data from the root rank to all ranks.
    If the target array is larger than the MPI buffer length, data will be transmitted point-to-point in rank order instead of using the Scatterv method.
    """
    if elements_this_rank is not None and elements_this_rank != data.shape[0]:
        raise

    if target_buffer is None:
        return data
    else:
        target_buffer[:] = data[:]
        return target_buffer



def mpi_redistribute_array_evenly(data: np.ndarray, elements_this_rank: int|None = None, elements_per_rank: list[int]|None = None, comm: object|None = None, root: int|None = None, target_buffer: np.ndarray|None = None) -> np.ndarray:
    return data
