from .._independant_mpi._mpi_config import mpi_config as MPI_Config
from ...Tools._edit_locals import use_locals

from typing import TypeVar, ParamSpec
from collections.abc import Callable, Sized, Sequence
from mpi4py import MPI
from functools import wraps, singledispatch
import numpy as np



P = ParamSpec("P")
T = TypeVar("T")



@use_locals(0, 0)
def synchronyse(target: T, /, root: int|None = None, comm: MPI.Intracomm|None = None) -> T:
    """
    Broadcast the value of a variable on the root rank to the same variable on all ranks in the communicator.

    The first argument should be a string containing the variable name NOT the value of the variable!
    """
    if root == None:
        root = MPI_Config.root
    if comm == None:
        comm = MPI_Config.comm
    result = comm.bcast(target, root)
    comm.barrier()
    return result



def if_mpi_root(default: T, root: int|None = None):
    """
    Function decorator for restricting calls to the root rank.

    A default return value of the appropriate return type must be provided (this can be None if the wrapped function allows it or specifies no return type).
    """
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



def mpi_barrier(comm: MPI.Intracomm|None = None) -> None:
    """
    Wait for all ranks in the communicator to reach this barrier.
    """
    (comm if comm is not None else MPI_Config.comm).barrier()



def mpi_get_slice(length: int|Sized, comm: MPI.Intracomm|None = None) -> slice:
    """
    Partition a set of data such that it is distributed evenly accross each MPI rank.

    This method can be used to help get data from a h5py dataset when using parallel IO.

    Parameters:
                 int|Sized length -> The length of the target data or the target data if a size can be derived from it.
        MPI.Intracomm|None comm   -> Optional MPI communicator object (defaults to the one from MPI_Config).

    Returns:
        slice -> A slice object that can be applied a Sequence of the appropriate length.
    """

    comm_size = MPI_Config.comm_size if comm is None else comm.Get_size()

    if not isinstance(length, int):
        length = len(length)

    base_chunk_size = length // comm_size
    chunks_with_one_extra = length % comm_size
    chunk_sizes = np.full(comm_size, base_chunk_size, dtype = int)
    chunk_sizes[:chunks_with_one_extra] += 1
    snaphot_data_offset: int = chunk_sizes[:max(0, comm_size - 1)].sum()
    snaphot_data_chunk_size: int = chunk_sizes[comm_size]

    return slice(snaphot_data_offset, snaphot_data_chunk_size)



def mpi_slice(data: Sequence[T], comm: MPI.Intracomm|None = None) -> Sequence[T]:
    """
    Partition a set of data such that it is distributed evenly accross each MPI rank.

    This method can be used to quickly get data from a h5py dataset when using parallel IO.

    Parameters:
                  Sequence data -> Data to be partitioned.
        MPI.Intracomm|None comm -> Optional MPI communicator object (defaults to the one from MPI_Config).

    Returns:
        Sequence -> Section of the data assigned to the calling rank.
    """
    return data[mpi_get_slice(len(data), comm)]
