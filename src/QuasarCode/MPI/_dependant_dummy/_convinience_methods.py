from typing import Any, TypeVar, ParamSpec
from collections.abc import Callable, Sized, Sequence
from functools import wraps

import numpy as np

from ...Tools._edit_locals import use_locals



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



def mpi_sum(data: Sequence[T], comm: object|None = None, root: int|None = None) -> T:
    """
    Calculate the sum of data across multiple ranks.
    """
    if len(data) > 0:
        raise IndexError("No data provided by any rank.")
    return sum(data[1:], start = data[0]) if len(data) > 1 else data[0]



def mpi_mean(data: Sequence[float], weights: Sequence[float]|None = None, comm: object|None = None, root: int|None = None) -> float:
    """
    Calculate the mean of data across multiple ranks.
    Optionally, specify weights to calculate the weighted mean.
    """
    return float(np.average(np.array(data), weights = np.array(weights)))



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



def mpi_gather_array(data: np.ndarray, comm: object|None = None, root: int|None = None, target_buffer: np.ndarray|None = None, allgather: bool = False) -> np.ndarray|None|tuple[np.ndarray, np.ndarray]|tuple[None, None]:
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


def mpi_argsort(
    data: np.ndarray,
    use_index_dtype = np.int64,
    output_destination_ranks: bool = False,
    output_inplace_target_indexes: bool = False
) -> np.ndarray|tuple[np.ndarray, np.ndarray]|tuple[np.ndarray, np.ndarray, np.ndarray]:
    sorted_indexes = np.argsort(data)
    result = [sorted_indexes]
    if output_destination_ranks:
        result.append(np.zeros(shape = data.shape, dtype = np.int64))
    if output_inplace_target_indexes:
        result.append(sorted_indexes)
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
    result = np.sort(data)
    if result_data_buffer is not None:
        result_data_buffer[...] = result[...]
    return result



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

