from ..._global_settings import settings_object as _settings_object
from ...MPI import get_mpi_rank

from functools import wraps

class _PrivateModuleFunctions(object):
    @staticmethod
    def _slurm_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if _settings_object.slurm:
                if "flush" not in kwargs:
                    kwargs["flush"] = True
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def _debug_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if _settings_object.debug:
                if "flush" not in kwargs:
                    kwargs["flush"] = True
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def _mpi_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "flush" not in kwargs:
                kwargs["flush"] = True
            if Console._limit_mpi_output_ranks is None or get_mpi_rank() not in Console._limit_mpi_output_ranks:
                return func(f" ({get_mpi_rank()})", *args, **kwargs)
            else:
                return lambda *args, **kwargs: None
        if _settings_object.mpi_avalible:
            return wrapper
        else:
            return lambda *args, **kwargs: func("", *args, **kwargs)

class Console(object):

    __print_custom_newline_spaces = " " * 16 # "                "
    @staticmethod
    def __print_custom_newline_format(mpi_rank_insert, s):
        return str(s).replace("\n", f"\n{Console.__print_custom_newline_spaces}" + (" " * len(mpi_rank_insert)) + (" " * len(Console.__create_locak_rank_insert())))
    
    _limit_mpi_output_ranks: tuple[int]|None = None
    @staticmethod
    def mpi_output_all_ranks() -> None:
        Console._limit_mpi_output_ranks = None
    @staticmethod
    def mpi_output_root_rank_only(root_rank: int = 0) -> None:
        if not isinstance(root_rank, int):
            try:
                root_rank = int(root_rank)
            except:
                raise TypeError(f"Argument provided for parameter root_rank (instance of {type(root_rank)}) is not an integer and cannot be interpreted as one.")
        if root_rank < 0:
            raise ValueError("Negitive values cannot be MPI rank indexes.")
        Console._limit_mpi_output_ranks = (root_rank, )
    @staticmethod
    def mpi_output_ranks_only(*ranks: int) -> None:
        parsed_ranks = []
        for rank in ranks:
            if not isinstance(rank, int):
                try:
                    rank = int(rank)
                except:
                    raise TypeError(f"Argument provided for parameter root_rank (instance of {type(rank)}) is not an integer and cannot be interpreted as one.")
            if rank < 0:
                raise ValueError("Negitive values cannot be MPI rank indexes.")
            parsed_ranks.append(rank)
        Console._limit_mpi_output_ranks = tuple(parsed_ranks)

    __local_parallel_rank: int|None = None
    @staticmethod
    def clear_local_parallel_rank() -> None:
        """
        Remove printing of non-MPI process ranks.
        """
        Console.__local_parallel_rank = None
    @staticmethod
    def set_local_parallel_rank(rank_index: int) -> None:
        """
        Set this processes rank for the given MPI rank.

        (i.e. when there are multiple local processes spawned from the same MPI rank process)
        """
        Console.__local_parallel_rank = rank_index
    @staticmethod
    def __create_locak_rank_insert() -> str:
        return f"[{Console.__local_parallel_rank}]" if Console.__local_parallel_rank is not None else ""
    
    @staticmethod
    @_PrivateModuleFunctions._mpi_wrapper
    @_PrivateModuleFunctions._debug_wrapper
    @_PrivateModuleFunctions._slurm_wrapper
    def print(mpi_rank_insert, firstValue = "", *args, **kwargs):
        rank_inserts = f"{mpi_rank_insert}{Console.__create_locak_rank_insert()}  "
        if rank_inserts == " " * 2:
            rank_inserts = ""
        print(f"{rank_inserts}{Console.__print_custom_newline_format(mpi_rank_insert, firstValue)}", *[Console.__print_custom_newline_format(mpi_rank_insert, arg) for arg in args], **kwargs)

    @staticmethod
    @_PrivateModuleFunctions._mpi_wrapper
    @_PrivateModuleFunctions._debug_wrapper
    @_PrivateModuleFunctions._slurm_wrapper
    def print_info(mpi_rank_insert, firstValue = "", *args, **kwargs):
        print(f"--|| INFO ||--{mpi_rank_insert}{Console.__create_locak_rank_insert()}  {Console.__print_custom_newline_format(mpi_rank_insert, firstValue)}", *[Console.__print_custom_newline_format(mpi_rank_insert, arg) for arg in args], **kwargs)

    def print_verbose_info(firstValue = "", *args, **kwargs):
        if _settings_object.verbose:
            Console.print_info(firstValue, *args, **kwargs)

    @staticmethod
    @_PrivateModuleFunctions._mpi_wrapper
    @_PrivateModuleFunctions._debug_wrapper
    @_PrivateModuleFunctions._slurm_wrapper
    def print_warning(mpi_rank_insert, firstValue = "", *args, **kwargs):
        print(f"--\u00BF\u00BF WARN ??--{mpi_rank_insert}{Console.__create_locak_rank_insert()}  {Console.__print_custom_newline_format(mpi_rank_insert, firstValue)}", *[Console.__print_custom_newline_format(mpi_rank_insert, arg) for arg in args], **kwargs)

    @staticmethod
    def print_verbose_warning(firstValue = "", *args, **kwargs):
        if _settings_object.verbose:
            Console.print_warning(firstValue, *args, **kwargs)

    @staticmethod
    @_PrivateModuleFunctions._mpi_wrapper
    @_PrivateModuleFunctions._debug_wrapper
    @_PrivateModuleFunctions._slurm_wrapper
    def print_error(mpi_rank_insert, firstValue = "", *args, **kwargs):
        print(f"--!! ERRO !!--{mpi_rank_insert}{Console.__create_locak_rank_insert()}  {Console.__print_custom_newline_format(mpi_rank_insert, firstValue)}", *[Console.__print_custom_newline_format(mpi_rank_insert, arg) for arg in args], **kwargs)

    def print_verbose_error(firstValue = "", *args, **kwargs):
        if _settings_object.verbose:
            Console.print_error(firstValue, *args, **kwargs)

    @staticmethod
    @_PrivateModuleFunctions._mpi_wrapper
    @_PrivateModuleFunctions._debug_wrapper
    @_PrivateModuleFunctions._slurm_wrapper
    def print_debug(mpi_rank_insert, firstValue = "", *args, **kwargs):
        if _settings_object.debug:
            print(f"--<< DEBG >>--{mpi_rank_insert}{Console.__create_locak_rank_insert()}  {Console.__print_custom_newline_format(mpi_rank_insert, firstValue)}", *[Console.__print_custom_newline_format(mpi_rank_insert, arg) for arg in args], **kwargs)

    @staticmethod
    def pause(exit = False):
        input("Press enter to {}... ".format("exit" if exit else "continue"))
