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



def mpi_check_equal(value: T, /, root: int|None = None, comm: MPI.Intracomm|None = None) -> bool:
    """
    Check all ranks have the same value.
    """
    comm = MPI_Config.allow_default_comm(comm)
    root = MPI_Config.allow_default_root(root)
    are_equal: bool
    values: list[T]|None = comm.gather(value, root = root)
    if comm.rank == root:
        are_equal = True
        for v in values[1:]:
            are_equal = values[0] == v
            if not are_equal:
                break
    synchronyse("are_equal", root = root, comm = comm)



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



def mpi_get_slice(length: int|Sized, comm: MPI.Intracomm|None = None, rank: int|None = None) -> slice:
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

    comm_size = MPI_Config.comm_size if comm is None else comm.Get_size()
    if rank == None:
        rank = MPI_Config.rank if comm is None else comm.Get_rank()

    if not isinstance(length, int):
        length = len(length)

    base_chunk_size = length // comm_size
    chunks_with_one_extra = length % comm_size
    chunk_sizes = np.full(comm_size, base_chunk_size, dtype = int)
    chunk_sizes[:chunks_with_one_extra] += 1
    snaphot_data_offset: int = chunk_sizes[:rank].sum()
    snaphot_data_chunk_size: int = chunk_sizes[rank]

    return slice(snaphot_data_offset, snaphot_data_offset + snaphot_data_chunk_size)



def mpi_slice(data: Sequence[T], comm: MPI.Intracomm|None = None, rank: int|None = None) -> Sequence[T]:
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
    return data[mpi_get_slice(len(data), comm, rank)]



_MAX_BUFFER_SIZE = 2**31 - 1 # Max length of an signed int32
def mpi_gather_array(data: np.ndarray, comm: MPI.Intracomm|None = None, root: int|None = None, target_buffer: np.ndarray|None = None) -> np.ndarray:
    """
    Gather numpy array data to the root rank.
    If the resulting array is larger than the MPI buffer length, data will be transmitted point-to-point in rank order instead of using the Gatherv method.
    """
    comm = MPI_Config.allow_default_comm(comm)
    root = MPI_Config.allow_default_root(root)

    comm.barrier()

    if any(comm.allgather(comm.rank != root and target_buffer is not None)):
        raise BufferError("Output buffer provided by non-root rank.")
    comm.barrier()

    local_buffer_length = np.prod(data.shape)
    local_buffer_length_first_dimension = data.shape[0]
    one_dimension = local_buffer_length == local_buffer_length_first_dimension
    local_buffer_step_size = 1 if one_dimension else np.prod(data.shape[1:])

    if not mpi_check_equal([one_dimension, local_buffer_step_size], root = root, comm = comm):
        raise BufferError("Input buffers on ranks have different shapes beyond first dimension.")
    comm.barrier()

    use_manual_transfer: int
    input_buffer_lengths_first_dimension: list[int]|None = comm.gather(data.shape[0], root = root)
    comm.barrier()
    if comm.rank == root:
        input_buffer_lengths_first_dimension: np.ndarray = np.array(input_buffer_lengths_first_dimension, dtype = int)
        output_buffer_length_first_dimension: int = sum(input_buffer_lengths_first_dimension)
        output_buffer_length = output_buffer_length_first_dimension * local_buffer_step_size
        use_manual_transfer = output_buffer_length > _MAX_BUFFER_SIZE
    synchronyse("use_manual_transfer", root = root, comm = comm)

    can_continue: bool
    if comm.rank == root:
        can_continue = target_buffer is None or target_buffer.shape == (output_buffer_length_first_dimension, *data.shape[1:])
    synchronyse("can_continue", root = root, comm = comm)
    if not can_continue:
        raise BufferError("Input buffer size/shape is not correct for the input data.")
    
    if comm.rank == root and target_buffer is None:
        target_buffer = np.empty(shape = (output_buffer_length_first_dimension, *data.shape[1:]), dtype = data.dtype)
        rank_offsets_first_dimension = np.insert(np.cumsum(input_buffer_lengths_first_dimension), 0, 0)[:-1]
        rank_offsets = np.insert(np.cumsum(input_buffer_lengths_first_dimension * local_buffer_step_size), 0, 0)[:-1]

    # The output buffer is within the maximum allowed size
    if not use_manual_transfer:
        comm.barrier()
        comm.Gatherv(data, None if comm.rank != root else (target_buffer, input_buffer_lengths_first_dimension * local_buffer_step_size, rank_offsets), root = root)
        comm.barrier()

    # The output buffer is larger than the maximum buffer length
    # Data must be communicated manualy
    else:
        if comm.rank == root:
            target_buffer[:data.shape[0]] = data[:]
        comm.barrier()
        for i in range(1, comm.size):
            if comm.rank == root:
                comm.recv(target_buffer[rank_offsets_first_dimension[i - 1] : rank_offsets_first_dimension[i]], source = i)
            elif comm.rank == i:    
                comm.send(data, dest = root)
            comm.barrier()

    return target_buffer
