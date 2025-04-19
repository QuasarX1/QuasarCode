from typing import cast as typing_cast, Any, TypeVar, ParamSpec
from collections.abc import Callable, Sized, Sequence
from functools import wraps, singledispatch

from mpi4py import MPI
import numpy as np

from .._independant_mpi._mpi_config import mpi_config as MPI_Config
from ...Tools._edit_locals import use_locals



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



def mpi_sum(data: Sequence[T], comm: MPI.Intracomm|None = None, root: int|None = None) -> T:
    """
    Calculate the sum of data across multiple ranks.
    """

    comm = MPI_Config.allow_default_comm(comm)
    root = MPI_Config.allow_default_root(root)

    comm.barrier()

    local_sum: T|None = sum(data[1:], start = data[0]) if len(data) > 1 else data[0] if len(data) > 0 else None

    result: T
    has_valid_data: bool
    rank_sums: list[T|None]|None = comm.gather(local_sum, root = root)
    if MPI_Config.check_is_root(root = root):
        valid_data: list[T] = [v for v in typing_cast(list[T], rank_sums) if v is not None]
        has_valid_data = len(valid_data) > 0
        if has_valid_data:
            result = sum(valid_data[1:], start = valid_data[0]) if len(valid_data) > 1 else valid_data[0]

    synchronyse("has_valid_data", root = root, comm = comm)
    if not has_valid_data:
        raise IndexError("No data provided by any rank.")

    synchronyse("result", root = root, comm = comm)

    comm.barrier()

    return result



def mpi_mean(data: Sequence[float], weights: Sequence[float]|None = None, comm: MPI.Intracomm|None = None, root: int|None = None) -> float:
    """
    Calculate the mean of data across multiple ranks.
    Optionally, specify weights to calculate the weighted mean.
    """

    comm = MPI_Config.allow_default_comm(comm)
    root = MPI_Config.allow_default_root(root)

    comm.barrier()

    local_sum: float = np.sum(data) if weights is None else np.sum(np.array(data) * np.array(weights))
    local_summed_divisor: float = len(data) if weights is None else np.sum(weights)

    result: float
    divide_by_zero: bool
    rank_sums: list[float]|None = comm.gather(local_sum, root = root)
    rank_divisor_sums: list[float]|None = comm.gather(local_summed_divisor, root = root)
    if MPI_Config.check_is_root(root = root):
        divisor = sum(typing_cast(list[float], rank_divisor_sums))
        divide_by_zero = divisor == 0
        if not divide_by_zero:
            result = sum(typing_cast(list[float], rank_sums)) / divisor

    synchronyse("divide_by_zero", root = root, comm = comm)
    if divide_by_zero:
        if weights is None:
            raise IndexError("No data provided by any rank.")
        else:
            raise ZeroDivisionError("Sum of weights was 0.")

    synchronyse("result", root = root, comm = comm)

    comm.barrier()

    return result



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



def mpi_gather_array(data: np.ndarray, comm: MPI.Intracomm|None = None, root: int|None = None, target_buffer: np.ndarray|None = None, return_chunk_sizes: bool = False, allgather: bool = False) -> np.ndarray|None|tuple[np.ndarray, np.ndarray]|tuple[None, None]:
    """
    Gather numpy array data to the root rank.
    If the resulting array is larger than the MPI buffer length, data will be transmitted point-to-point in rank order instead of using the Gatherv method.
    """
    comm = MPI_Config.allow_default_comm(comm)
    root = MPI_Config.allow_default_root(root)

    comm.barrier()

    if sum(comm.allgather(int(allgather))) not in (0, comm.size):
        raise ValueError("Not all ranks set parameter \"allgather\" as True.")
    comm.barrier()

    if not allgather:
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
    input_buffer_lengths_first_dimension: list[int] = comm.allgather(data.shape[0], root = root)
    comm.barrier()
    if comm.rank == root or allgather:
        input_buffer_lengths_first_dimension: np.ndarray = np.array(input_buffer_lengths_first_dimension, dtype = int) # Why is this necessary???
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
    
    if comm.rank == root or allgather:
        if target_buffer is None:
            target_buffer = np.empty(shape = (output_buffer_length_first_dimension, *data.shape[1:]), dtype = data.dtype)
        rank_offsets_first_dimension = np.insert(np.cumsum(input_buffer_lengths_first_dimension), 0, 0)[:-1]
        rank_offsets = np.insert(np.cumsum(input_buffer_lengths_first_dimension * local_buffer_step_size), 0, 0)[:-1]

    # The output buffer is within the maximum allowed size
    if not use_manual_transfer:
        comm.barrier()
        if allgather:
            comm.Allgatherv(data, None if comm.rank != root else (target_buffer, (input_buffer_lengths_first_dimension * local_buffer_step_size, rank_offsets)))
        else:
            comm.Gatherv(data, None if comm.rank != root else (target_buffer, (input_buffer_lengths_first_dimension * local_buffer_step_size, rank_offsets)), root = root)
        comm.barrier()

    # The output buffer is larger than the maximum buffer length
    # Data must be communicated manualy
    else:
        if comm.rank == root or allgather:
            target_buffer[rank_offsets_first_dimension[comm.rank]:data.shape[0]] = data[:]
        comm.barrier()
        for i in range(0, comm.size):
            if not allgather and i == root:
                # The root has already had an opportunity to transfer its data so we can skip this one
                continue
            if comm.rank != i:
                total_expected_elements_all_dimensions = input_buffer_lengths_first_dimension[i] * local_buffer_step_size
                if total_expected_elements_all_dimensions <= _MAX_BUFFER_SIZE:
                    # Data can be transferred in a single function call
                    if allgather:
                        comm.Bcast(target_buffer[rank_offsets_first_dimension[i] : rank_offsets_first_dimension[i] + input_buffer_lengths_first_dimension[i]], root = i)
                    else:
                        comm.Recv(target_buffer[rank_offsets_first_dimension[i] : rank_offsets_first_dimension[i] + input_buffer_lengths_first_dimension[i]], source = i)
                else:
                    # Data is too large be transferred in a single function call
                    # Multiple calls required
                    local_chunk_offset: int = 0
                    elements_first_dimension_remaining: int = input_buffer_lengths_first_dimension[i]
                    while elements_first_dimension_remaining > 0:
                        chunk_size_this_transfer = _MAX_BUFFER_SIZE if elements_first_dimension_remaining > _MAX_BUFFER_SIZE else elements_first_dimension_remaining
                        if allgather:
                            comm.Bcast(target_buffer[rank_offsets_first_dimension[i] + local_chunk_offset : rank_offsets_first_dimension[i] + local_chunk_offset + chunk_size_this_transfer], root = i)
                        else:
                            comm.Recv(target_buffer[rank_offsets_first_dimension[i] + local_chunk_offset : rank_offsets_first_dimension[i] + local_chunk_offset + chunk_size_this_transfer], source = i)
                        local_chunk_offset += chunk_size_this_transfer
                        elements_first_dimension_remaining -= chunk_size_this_transfer
            elif comm.rank == i:
                if np.prod(data.shape) <= _MAX_BUFFER_SIZE:
                    if allgather:
                        comm.Bcast(data, root = comm.rank)
                    else:
                        comm.Send(data, dest = root)
                else:
                    local_chunk_offset: int = 0
                    elements_first_dimension_remaining: int = data.shape[0]
                    while elements_first_dimension_remaining > 0:
                        chunk_size_this_transfer = _MAX_BUFFER_SIZE if elements_first_dimension_remaining > _MAX_BUFFER_SIZE else elements_first_dimension_remaining
                        if allgather:
                            comm.Bcast(data[local_chunk_offset : local_chunk_offset + chunk_size_this_transfer], root = comm.rank)
                        else:
                            comm.Send(data[local_chunk_offset : local_chunk_offset + chunk_size_this_transfer], dest = root)
                        local_chunk_offset += chunk_size_this_transfer
                        elements_first_dimension_remaining -= chunk_size_this_transfer
            comm.barrier()

    if return_chunk_sizes:
        return target_buffer, input_buffer_lengths_first_dimension
    else:
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
                    rank_chunk_start, rank_chunk_stop, _ = mpi_get_slice(data.shape[0], comm = comm, rank = i).indices(data.shape[0])
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
        if any(comm.allgather(target_buffer is not None and (target_buffer.shape[0] != elements_this_rank or target_buffer.shape[1:] != local_buffer_shape_after_first_dimension))):
            raise BufferError("Output buffers provided to ranks did not match their respective expected sizes/shapes.")
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
        comm.Scatterv(None if comm.rank != root else (data, (output_buffer_lengths_first_dimension * buffer_step_size, rank_offsets)), target_buffer, root = root)
        comm.barrier()

    # The input buffer is larger than the maximum buffer length
    # Data must be communicated manualy
    else:
        if comm.rank == root:
            target_buffer[:] = data[:output_buffer_lengths_first_dimension[0]]
        comm.barrier()
        for i in range(1, comm.size):
            if comm.rank == root:
                total_expected_elements_all_dimensions = output_buffer_lengths_first_dimension[i] * buffer_step_size
                if total_expected_elements_all_dimensions <= _MAX_BUFFER_SIZE:
                    # Data can be transferred in a single function call
                    comm.Send(data[rank_offsets_first_dimension[i] : rank_offsets_first_dimension[i] + output_buffer_lengths_first_dimension[i] ], dest = i)
                else:
                    # Data is too large be transferred in a single function call
                    # Multiple calls required
                    local_chunk_offset: int = 0
                    elements_first_dimension_remaining: int = output_buffer_lengths_first_dimension[i]
                    while elements_first_dimension_remaining > 0:
                        chunk_size_this_transfer = _MAX_BUFFER_SIZE if elements_first_dimension_remaining > _MAX_BUFFER_SIZE else elements_first_dimension_remaining
                        comm.Send(data[rank_offsets_first_dimension[i] + local_chunk_offset : rank_offsets_first_dimension[i] + local_chunk_offset + chunk_size_this_transfer], dest = i)
                        local_chunk_offset += chunk_size_this_transfer
                        elements_first_dimension_remaining -= chunk_size_this_transfer
            elif comm.rank == i:
                if elements_this_rank * np.prod(local_buffer_shape_after_first_dimension) <= _MAX_BUFFER_SIZE:
                    comm.Recv(target_buffer, source = root)
                else:
                    local_chunk_offset: int = 0
                    elements_first_dimension_remaining: int = elements_this_rank
                    while elements_first_dimension_remaining > 0:
                        chunk_size_this_transfer = _MAX_BUFFER_SIZE if elements_first_dimension_remaining > _MAX_BUFFER_SIZE else elements_first_dimension_remaining
                        comm.Recv(target_buffer[local_chunk_offset : local_chunk_offset + chunk_size_this_transfer], source = root)
                        local_chunk_offset += chunk_size_this_transfer
                        elements_first_dimension_remaining -= chunk_size_this_transfer
            comm.barrier()

    return target_buffer



def mpi_redistribute_array_evenly(data: np.ndarray, elements_this_rank: int|None = None, elements_per_rank: list[int]|None = None, comm: MPI.Intracomm|None = None, root: int|None = None, target_buffer: np.ndarray|None = None) -> np.ndarray:
    """
    Send all data to the root rank for redistribution to all ranks.
    See mpi_gather_array for information regarting the "data" parameter.
    See mpi_scatter_array for information regarting the "elements_this_rank" and "elements_per_rank" parameters.
    """
#    comm = MPI_Config.allow_default_comm(comm)
#    root = MPI_Config.allow_default_root(root)
    return mpi_scatter_array(mpi_gather_array(data, comm = comm, root = root), target_buffer = target_buffer, elements_this_rank = elements_this_rank, elements_per_rank = elements_per_rank, comm = comm, root = root)



def mpi_argsort(
    data: np.ndarray,
    use_index_dtype = np.int64,
    output_destination_ranks: bool = False,
    output_inplace_target_indexes: bool = False
) -> np.ndarray|tuple[np.ndarray, np.ndarray]|tuple[np.ndarray, np.ndarray, np.ndarray]:

    # Wait for all ranks to be ready
    mpi_barrier()

    # Compute the total length accross all ranks and index bounaries
    elements_per_rank: list[int] = MPI_Config.comm.allgather(data.shape[0])
    total_data_length = sum(elements_per_rank)
    rank_boundary_indexes: np.ndarray = np.array([0, *np.cumsum(elements_per_rank)], dtype = use_index_dtype) # boundarys are half-open [...)
    rank_global_start_index = rank_boundary_indexes[MPI_Config.rank]
    rank_global_end_index = rank_boundary_indexes[MPI_Config.rank + 1]

    # Create somwhere to store the final results of the argsort
    sorted_indexes = np.empty(shape = data.shape[0], dtype = use_index_dtype)
    if output_inplace_target_indexes:
        global_sorted_position_indexes = np.empty(shape = data.shape[0], dtype = use_index_dtype)
    if output_destination_ranks:
        destination_rank = np.empty(shape = data.shape[0], dtype = np.int64)

    # Sort the data locally
    # The smallest value accross all datasets must now be in the first position of the argsort of one of the ranks
    local_sort_indexes = np.argsort(data)
    local_sort_indexes_index: int|None = 0

    mpi_barrier()

    if MPI_Config.is_root:
        # List of rank indexes that can be filtered along with the selection options
        rank_indexes = np.arange(MPI_Config.comm_size)
        # Create a staging area to hold the smallest unselected value from each rank
        options = np.empty(shape = (MPI_Config.comm_size, *data.shape[1:]), dtype = data.dtype)
        # Create a mask that can be used to ignore ranks that have no remaining test values
        valid_options_mask = np.full(options.shape, True)

        # Set the first test value locally
        if data.shape[0] == 0:
            valid_options_mask[0] = False
        else:
            options[0] = data[local_sort_indexes[local_sort_indexes_index]]

        # Check all other ranks for data being avalible then recive the first value from such ranks
        for rank in range(0, MPI_Config.comm_size):
            mpi_barrier()
            # Ignore the root rank as that has already been handled
            if rank == MPI_Config.root:
                continue
            has_value_avalible = MPI_Config.comm.recv(source = rank)
            mpi_barrier()
            if has_value_avalible:
                options[rank] = MPI_Config.comm.recv(source = rank)
            else:
                valid_options_mask[rank] = False

    else:
        # Loop over all non-root ranks
        for rank in range(0, MPI_Config.comm_size):
            mpi_barrier()
            # Ignore the root rank as that has already been handled
            if rank == MPI_Config.root:
                continue
            # Wait for this rank's turn
            if MPI_Config.rank == rank:
                if data.shape[0] == 0:
                    # No data avalible
                    MPI_Config.comm.send(False, dest = MPI_Config.root)
                    mpi_barrier()
                else:
                    # Data is avalible so confirm this then send the smallest element
                    MPI_Config.comm.send(True, dest = MPI_Config.root)
                    mpi_barrier()
                    MPI_Config.comm.send(data[local_sort_indexes[local_sort_indexes_index]], dest = MPI_Config.root)
            else:
                # Everyone needs to call the barrier
                mpi_barrier()

    mpi_barrier()

    # Select the lowest element a number of times equal to the number of total data elements
    for sorted_element_index in range(total_data_length):

        # Select the lowest avalible option on the root rank then update all ranks with the rank that sent the smallest value
        rank_with_next_value: int
        if MPI_Config.is_root:
            rank_with_next_value = rank_indexes[valid_options_mask][np.argmin(options[valid_options_mask])]
        synchronyse("rank_with_next_value")

        global_index_of_selected_value: int

        # If this rank is the one with the current smallest value
        if MPI_Config.rank == rank_with_next_value:
            # Update the result for the current smallest item on this rank
            global_index_of_selected_value = rank_global_start_index + local_sort_indexes[local_sort_indexes_index]
            if output_inplace_target_indexes:
                global_sorted_position_indexes[local_sort_indexes[local_sort_indexes_index]] = sorted_element_index
            if output_destination_ranks:
                destination_rank[local_sort_indexes[local_sort_indexes_index]] = np.where(rank_boundary_indexes <= sorted_element_index)[0][-1]
            # Move to the next item
            local_sort_indexes_index += 1
            # If there is no next item, scrub the invalid index
            if local_sort_indexes_index >= data.shape[0]:
                local_sort_indexes_index = None

            # If the root rank has the selected value, just do all the updates locally
            if MPI_Config.is_root:
                if local_sort_indexes_index is not None:
                    options[0] = data[local_sort_indexes[local_sort_indexes_index]]
                else:
                    valid_options_mask[0] = False
                # Every other rank will have called an extra barrier to account for the usual status check call, so call anyway to match
                mpi_barrier()

            # If not the root rank, send the next lowest value to the root
            else:
                if local_sort_indexes_index is not None:
                    MPI_Config.comm.send(True, dest = MPI_Config.root)
                    mpi_barrier()
                    MPI_Config.comm.send(data[local_sort_indexes[local_sort_indexes_index]], dest = MPI_Config.root)
                else:
                    MPI_Config.comm.send(False, dest = MPI_Config.root)
                    mpi_barrier()

        # If the root rank does not contain the selected value, it still needs to recive an updated value
        elif MPI_Config.is_root:
            has_value_avalible = MPI_Config.comm.recv(source = rank_with_next_value)
            mpi_barrier()
            if has_value_avalible:
                options[rank_with_next_value] = MPI_Config.comm.recv(source = rank_with_next_value)
            else:
                valid_options_mask[rank_with_next_value] = False

        else:
            # Uninvolved ranks still need to call the barrier!
            mpi_barrier()

        mpi_barrier()

        synchronyse("global_index_of_selected_value", root = rank_with_next_value)

        mpi_barrier()

        if rank_global_start_index <= sorted_element_index and sorted_element_index < rank_global_end_index:
            sorted_indexes[sorted_element_index - rank_global_start_index] = global_index_of_selected_value

        mpi_barrier()

    mpi_barrier()

    result = [sorted_indexes]
    if output_destination_ranks:
        result.append(destination_rank)
    if output_inplace_target_indexes:
        result.append(global_sorted_position_indexes)
    return result[0] if len(result) == 1 else tuple(result)



def mpi_sort(
        data: np.ndarray,
        order: tuple[np.ndarray, np.ndarray]|None = None,
        result_data_buffer: np.ndarray|None = None,
        assume_memory_limitation: bool = False
) -> np.ndarray:
    """
    Sort a set of data in parallel.

    Parameters:

                           `numpy.ndarray` `data`                     -> The data to be sorted (along axis = 0)

        (`numpy.ndarray`, `numpy.ndarray`) `order`                    -> The ordering information from `mpi_argsort(...)[1:]` (target_ranks, inplace_sort_indexes) (optional)

                           `numpy.ndarray` `result_data_buffer`       -> Buffer to place results into (optional)

                                    `bool` `assume_memory_limitation` -> Perform the sort in a memory-efficient way, at the cost of speed (defaults to False - fastest)

    Returns:
        `numpy.ndarray` -> The data in a sorted order distributed accross each rank using the same distribution as the input data
    """
    if order is None:
        order = mpi_argsort(data, output_destination_ranks = True, output_inplace_target_indexes = True)[1:]

    sorted_data: np.ndarray
    unscrambling_indexes: np.ndarray
    if result_data_buffer is not None:
        sorted_data = result_data_buffer
    if not assume_memory_limitation:
        # Might as well request the memory in parallel
        if result_data_buffer is None:
            sorted_data = np.empty_like(data)
        unscrambling_indexes = np.empty(shape = data.shape[0], dtype = np.int64)

    for target_rank in range(MPI_Config.comm_size):
        mpi_barrier()

        rank_is_target = MPI_Config.check_is_root(target_rank)
        send_mask = order[0] == target_rank

        if assume_memory_limitation and rank_is_target:
            # Avoid requesting the memory until absolutely nessessary
            if result_data_buffer is None:
                sorted_data = np.empty_like(data)
            unscrambling_indexes = np.empty(shape = data.shape[0], dtype = np.int64)

        mpi_gather_array(    data[send_mask], root = target_rank, target_buffer =          sorted_data if rank_is_target else None)
        mpi_gather_array(order[1][send_mask], root = target_rank, target_buffer = unscrambling_indexes if rank_is_target else None)

        if assume_memory_limitation:
            # Do the unscramble now to avoid unnessessary memory being held
            # This will be slower as all ranks must wait for this to be completed
            if rank_is_target:
                unscrambled = np.empty_like(sorted_data)
                unscrambled[unscrambling_indexes - unscrambling_indexes.min()] = sorted_data
                sorted_data = unscrambled[:]
                del unscrambling_indexes
                del unscrambled

    mpi_barrier()

    if not assume_memory_limitation:
        # Do the unscramble at the end
        # This will be faster as this can be done in parallel, but uses more memory as the unscramble indexes are stored accross all calls
        unscrambled = np.empty_like(sorted_data)
        unscrambled[unscrambling_indexes - unscrambling_indexes.min()] = sorted_data
        sorted_data = unscrambled[:]
        del unscrambling_indexes
        del unscrambled

    return sorted_data



def mpi_calculate_reorder(
    input_ids: np.ndarray,
    output_ids: np.ndarray,
    assume_memory_limitation: bool = False
) -> tuple[np.ndarray, np.ndarray]:
    order = mpi_argsort(input_ids, output_destination_ranks = True, output_inplace_target_indexes = True)
    reverse_order = mpi_argsort(order[0], output_destination_ranks = True, output_inplace_target_indexes = True)
    del order

    target_sort_order = mpi_argsort(output_ids, output_destination_ranks = True, output_inplace_target_indexes = True)
    reverse_target_sort_order = mpi_argsort(target_sort_order[0], output_destination_ranks = True, output_inplace_target_indexes = True)
    del target_sort_order

    return (
        mpi_sort(data = reverse_target_sort_order[1], order = reverse_order[1:], assume_memory_limitation = assume_memory_limitation),
        mpi_sort(data = reverse_target_sort_order[2], order = reverse_order[1:], assume_memory_limitation = assume_memory_limitation)
    )



def mpi_reorder(
    input_ids: np.ndarray,
    input_data: np.ndarray,
    output_ids: np.ndarray,
    output_data_buffer: np.ndarray|None = None,
    assume_memory_limitation: bool = False
) -> np.ndarray:
    order = mpi_calculate_reorder(input_ids, output_ids)
    return mpi_sort(
        data = input_data,
        order = order,
        result_data_buffer = output_data_buffer,
        assume_memory_limitation = assume_memory_limitation
    )



def mpi_apply_reorder(
    input_data: np.ndarray,
    order: tuple[np.ndarray, np.ndarray],
    output_data_buffer: np.ndarray|None = None,
    assume_memory_limitation: bool = False
) -> np.ndarray:
    """
    Wrapper for `mpi_sort` using a subset of the parameter names from `mpi_reorder`.

    `input_data` -> `data`

    `order` -> `order`

    `output_data_buffer` -> `result_data_buffer`

    `assume_memory_limitation` -> `assume_memory_limitation`
    """
    return mpi_sort(
        data = input_data,
        order = order,
        result_data_buffer = output_data_buffer,
        assume_memory_limitation = assume_memory_limitation
    )

