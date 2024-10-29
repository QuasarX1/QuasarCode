from .._independant_mpi._mpi_config import mpi_config as MPI_Config
from ...Tools._edit_locals import use_locals

from typing import TypeVar, ParamSpec
from collections.abc import Callable, Sized, Sequence
from mpi4py import MPI
from functools import wraps, singledispatch
import numpy as np



P = ParamSpec("P")
T = TypeVar("T")
_MAX_BUFFER_SIZE = 2**31 - 1 # Max length of an signed int32



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
    return are_equal



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



def mpi_gather_array(data: np.ndarray, comm: MPI.Intracomm|None = None, root: int|None = None, target_buffer: np.ndarray|None = None) -> np.ndarray:
    """
    Gather numpy array data to the root rank.
    If the resulting array is larger than the MPI buffer length, data will be transmitted point-to-point in rank order instead of using the Gatherv method.
    """
    comm = MPI_Config.allow_default_comm(comm)
    root = MPI_Config.allow_default_root(root)

    comm.barrier()

    if any(comm.allgather(comm.rank != root and target_buffer is not None)):
        raise TypeError("Output buffer provided by non-root rank.")
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
    
    if comm.rank == root:
        if target_buffer is None:
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



def mpi_scatter_array(data: np.ndarray|None, elements_this_rank: int|None = None, elements_per_rank: list[int]|None = None, comm: MPI.Intracomm|None = None, root: int|None = None, target_buffer: np.ndarray|None = None) -> np.ndarray:
    """
    Scatter numpy array data from the root rank to all ranks.
    If the target array is larger than the MPI buffer length, data will be transmitted point-to-point in rank order instead of using the Scatterv method.
    """
    can_continue: bool # This is used to synchronise error conditions between ranks

    comm = MPI_Config.allow_default_comm(comm)
    root = MPI_Config.allow_default_root(root)

    comm.barrier()

    if comm.rank == root:
        can_continue = data is not None
    synchronyse("can_continue", root = root, comm = comm)
    if not can_continue:
        raise TypeError("Root rank did not provide any data.")

    if any(comm.allgather(comm.rank != root and data is not None)):
        raise TypeError("Non-root rank provided input data.")
    comm.barrier()

    if any(comm.allgather(comm.rank != root and elements_per_rank is not None)):
        raise TypeError("Non-root rank provided scattering information for all ranks.")
    comm.barrier()

    does_rank_give_chunk_size = comm.allgather(elements_this_rank is not None)
    if any(does_rank_give_chunk_size) and not all(does_rank_give_chunk_size):
        raise TypeError("Some but not all ranks provided chunk size information.")
    comm.barrier()

    if comm.rank == root:
        can_continue = elements_this_rank is None or not any(does_rank_give_chunk_size)
    synchronyse("can_continue", root = root, comm = comm)
    if not can_continue:
        raise TypeError("Root rank provided chunk sizes but ranks also provided chunk sizes.")

    output_buffer_lengths_first_dimension: np.ndarray
    rank_offsets_first_dimension: np.ndarray
    if elements_this_rank is None:
        if comm.rank == root:
            if elements_per_rank is None:
                output_buffer_lengths_first_dimension = np.empty(comm.size, dtype = int)
                rank_offsets_first_dimension = np.empty(comm.size, dtype = int)
                for i in range(comm.size):
                    rank_chunk_start, rank_chunk_stop = mpi_get_slice(data.shape[0], comm = comm, rank = i).indices(data.shape[0])
                    output_buffer_lengths_first_dimension[i] = rank_chunk_stop - rank_chunk_start
                    rank_offsets_first_dimension[i] = rank_chunk_start
            else:
                output_buffer_lengths_first_dimension = np.array(elements_per_rank, dtype = int)
                rank_offsets_first_dimension = np.insert(np.cumsum(output_buffer_lengths_first_dimension), 0, 0)[:-1]
        elements_this_rank = comm.scatter(None if comm.rank != root else output_buffer_lengths_first_dimension, root = root)
    else:
        output_buffer_lengths_first_dimension = comm.gather(elements_this_rank, root = root)
        comm.barrier()
        if comm.rank == root:
            output_buffer_lengths_first_dimension = np.array(output_buffer_lengths_first_dimension, dtype = int)
            rank_offsets_first_dimension = np.insert(np.cumsum(output_buffer_lengths_first_dimension), 0, 0)[:-1]

    local_buffer_shape_after_first_dimension: tuple[int, ...]
    if comm.rank == root:
        source_buffer_length = np.prod(data.shape)
        source_buffer_length_first_dimension = data.shape[0]
        one_dimension = source_buffer_length == source_buffer_length_first_dimension
        buffer_step_size = 1 if one_dimension else np.prod(data.shape[1:])
        local_buffer_shape_after_first_dimension = data.shape[1:]
    synchronyse("local_buffer_shape_after_first_dimension", root = root, comm = comm)

    if target_buffer is not None:
        if any(comm.allgather(target_buffer is not None and (target_buffer.shape[0] != elements_this_rank or target_buffer.shape[:1] != local_buffer_shape_after_first_dimension))):
            raise BufferError("Output bufferes provided to ranks did not match their respective expected sizes/shapes.")
        comm.barrier()

    target_datatype: object
    target_datatype: object
    if comm.rank == root:
        target_datatype = data.dtype
    synchronyse("target_datatype", root = root, comm = comm)
    if target_buffer is None:
        target_buffer = np.empty(shape = (elements_this_rank, *local_buffer_shape_after_first_dimension), dtype = target_datatype)

    if comm.rank == root:
        rank_offsets = np.insert(np.cumsum(output_buffer_lengths_first_dimension * buffer_step_size), 0, 0)[:-1]

    use_manual_transfer: bool
    if comm.rank == root:
        use_manual_transfer = data.shape[0] > _MAX_BUFFER_SIZE
    synchronyse("use_manual_transfer", root = root, comm = comm)

    # The input buffer is within the maximum allowed size
    if not use_manual_transfer:
        comm.barrier()
        comm.Scatter(None if comm.rank != root else (data, output_buffer_lengths_first_dimension * buffer_step_size, rank_offsets), target_buffer, root = root)
        comm.barrier()

    # The input buffer is larger than the maximum buffer length
    # Data must be communicated manualy
    else:
        if comm.rank == root:
            target_buffer[:] = data[:rank_offsets_first_dimension[1]]
        comm.barrier()
        for i in range(1, comm.size):
            if comm.rank == root:
                comm.send(data[rank_offsets_first_dimension[i - 1] : rank_offsets_first_dimension[i]], dest = i)
            elif comm.rank == i:
                comm.recv(target_buffer, source = root)
            comm.barrier()

    return target_buffer
