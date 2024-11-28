from ..._global_settings import settings_object as _settings_object
from ...MPI import get_mpi_rank
from ...Tools._stopwatch import IStopwatch, SimpleStopwatch



class Console(object):
    """
    Rich test IO interface for the console.

    When using MPI, process information uses the following layout order: (MPI rank, subprocess)
    """

    __stopwatch: IStopwatch = SimpleStopwatch.start_new()
    @staticmethod
    def reset_stopwatch(synchronise: IStopwatch|None = None) -> None:
        Console.__stopwatch.stop()
        Console.__stopwatch.reset()
        if synchronise is not None:
            Console.__stopwatch.synchronise_start(synchronise)
        else:
            Console.__stopwatch.start()

    __print_newline_indentation: str = " " * 10
    @staticmethod
    def __custom_newline_format(info_insert_length, s) -> str:
        return str(s).replace("\n", f"\n{Console.__print_newline_indentation}" + (" " * info_insert_length))

    @staticmethod
    def __print(prefix: str, raw_text_input: list[str], /, show_insert: bool, **kwargs) -> None:

        # Don't print if on a rank that is blocked from printing
        if not (Console.__limit_mpi_output_ranks is None or (Console.__debug_bypasses_mpi_output_restriction and _settings_object.debug) or get_mpi_rank() in Console.__limit_mpi_output_ranks):
            return

        if prefix != "":
            prefix += " "

        insert_text: str = ""
        if show_insert:
            if _settings_object.mpi_avalible or Console.__process_id is not None:
                process_list = []
                if _settings_object.mpi_avalible:
                    process_list.append(str(get_mpi_rank()))
                if Console.__process_id is not None:
                    process_list.append(str(Console.__process_id))
                insert_text += "(" + ",".join(process_list) + ") "#TODO: add padding for numbers with fewer digits than the largest number in each category
            if Console.__show_time:
                insert_text += f"[{Console.__stopwatch.get_elapsed_time():.3f}] "
        insert_test_length = len(insert_text)

        # Indent newlines
        text: str = " ".join([Console.__custom_newline_format(insert_test_length, str(s)) for s in raw_text_input])

        if "flush" not in kwargs and (_settings_object.debug or _settings_object.slurm or _settings_object.mpi_avalible):
            kwargs["flush"] = True

        print(f"{prefix}{insert_text}{text}", **kwargs)

    __show_time: bool = False
    @staticmethod
    def show_times():
        Console.__show_time = True
    @staticmethod
    def hide_times():
        Console.__show_time = False

    __limit_mpi_output_ranks: tuple[int]|None = None
    __debug_bypasses_mpi_output_restriction: bool = False
    @staticmethod
    def mpi_output_all_ranks() -> None:
        Console._limit_mpi_output_ranks = None
    @staticmethod
    def mpi_output_root_rank_only(root_rank: int = 0, /, bypass_when_debug = False) -> None:
        if not isinstance(root_rank, int):
            try:
                root_rank = int(root_rank)
            except:
                raise TypeError(f"Argument provided for parameter root_rank (instance of {type(root_rank)}) is not an integer and cannot be interpreted as one.")
        if root_rank < 0:
            raise ValueError("Negative values cannot be MPI rank indexes.")
        Console.__limit_mpi_output_ranks = (root_rank, )
        Console.__debug_bypasses_mpi_output_restriction = bypass_when_debug
    @staticmethod
    def mpi_output_ranks_only(*ranks: int, bypass_when_debug = False) -> None:
        parsed_ranks = []
        for rank in ranks:
            if not isinstance(rank, int):
                try:
                    rank = int(rank)
                except:
                    raise TypeError(f"Argument provided for parameter ranks (instance of {type(rank)}) is not an integer and cannot be interpreted as one.")
            if rank < 0:
                raise ValueError("Negative values cannot be MPI rank indexes.")
            parsed_ranks.append(rank)
        Console.__limit_mpi_output_ranks = tuple(parsed_ranks)
        Console.__debug_bypasses_mpi_output_restriction = bypass_when_debug

    __process_id: str|int|None = None
    @staticmethod
    def clear_process_id() -> None:
        """
        Clear the manually set process ID.

        MPI ranks are handled automatically.
        """
        Console.__process_id = None
    @staticmethod
    def set_process_id(id: str|int) -> None:
        """
        Set process ID.

        MPI ranks are handled automatically.
        """
        Console.__process_id = id

    @staticmethod
    def print_raw(*args: str, **kwargs) -> None:
        Console.__print("", args, show_insert = False, **kwargs)
    @staticmethod
    def print_raw_verbose(*args: str, verbosity_level: int = 0, **kwargs) -> None:
        if _settings_object.verbose and verbosity_level >= _settings_object.verbosity_level:
            Console.__print("", args, show_insert = False, **kwargs)
    @staticmethod
    def print_raw_verbose_debug(*args: str, verbosity_level: int|None = -1, **kwargs) -> None:
        if _settings_object.debug and (verbosity_level is None or _settings_object.verbose and verbosity_level >= _settings_object.verbosity_level):
            Console.__print("", args, show_insert = False, **kwargs)
    @staticmethod
    def print_raw_debug(*args: str, **kwargs) -> None:
        Console.print_raw_verbose_debug(*args, verbosity_level = None, **kwargs)

    @staticmethod
    def print(*args: str, **kwargs) -> None:
        Console.__print("", args, show_insert = True, **kwargs)

    @staticmethod
    def print_verbose(*args: str, verbosity_level: int = 0, **kwargs) -> None:
        if _settings_object.verbose and verbosity_level >= _settings_object.verbosity_level:
            Console.__print("", args, show_insert = True, **kwargs)

    @staticmethod
    def print_info(*args: str, **kwargs) -> None:
        Console.__print("|INFO|", args, show_insert = True, **kwargs)
    @staticmethod
    def print_verbose_info(*args: str, verbosity_level: int = 0, **kwargs) -> None:
        if _settings_object.verbose and verbosity_level >= _settings_object.verbosity_level:
            Console.print_info(*args, **kwargs)

    @staticmethod
    def print_warning(*args: str, **kwargs) -> None:
        Console.__print("\u00BFWARN?", args, show_insert = True, **kwargs)
    @staticmethod
    def print_verbose_warning(*args: str, verbosity_level: int = 0, **kwargs) -> None:
        if _settings_object.verbose and verbosity_level >= _settings_object.verbosity_level:
            Console.print_warning(*args, **kwargs)

    @staticmethod
    def print_error(*args: str, **kwargs) -> None:
        Console.__print("!ERRO!", args, show_insert = True, **kwargs)
    @staticmethod
    def print_verbose_error(*args: str, verbosity_level: int = 0, **kwargs) -> None:
        if _settings_object.verbose and verbosity_level >= _settings_object.verbosity_level:
            Console.print_error(*args, **kwargs)

    @staticmethod
    def print_verbose_debug(*args: str, verbosity_level: int|None = -1, **kwargs) -> None:
        if _settings_object.debug and (verbosity_level is None or _settings_object.verbose and verbosity_level >= _settings_object.verbosity_level):
            Console.__print("<DBUG>", args, show_insert = True, **kwargs)
    @staticmethod
    def print_debug(*args: str, **kwargs) -> None:
        Console.print_verbose_debug(*args, verbosity_level = None, **kwargs)

    @staticmethod
    def custom_print(prefix: str, *args: str, show_insert: bool = True, **kwargs) -> None:
        if len(prefix) < 6:
            prefix = (" " * (6 - len(prefix))) + prefix
        elif len(prefix) > 6:
            prefix = prefix[:6]
        Console.__print(prefix, args, show_insert = show_insert, **kwargs)
    @staticmethod
    def custom_print_verbose(prefix: str, *args: str, show_insert: bool = True, verbosity_level: int = -1, **kwargs) -> None:
        if _settings_object.verbose and verbosity_level >= _settings_object.verbosity_level:
            Console.custom_print(prefix, *args, show_insert = show_insert, **kwargs)
    @staticmethod
    def custom_print_verbose_debug(prefix: str, *args: str, show_insert: bool = True, verbosity_level: int|None = -1, **kwargs) -> None:
        if _settings_object.debug and (verbosity_level is None or _settings_object.verbose and verbosity_level >= _settings_object.verbosity_level):
            Console.custom_print(prefix, *args, show_insert = show_insert, **kwargs)
    def custom_print_debug(prefix: str, *args: str, show_insert: bool = True, **kwargs) -> None:
        Console.custom_print_verbose_debug(prefix, *args, show_insert = show_insert, verbosity_level = None, **kwargs)

    @staticmethod
    def pause(exit = False):
        input("Press enter to {}... ".format("exit" if exit else "continue"))

    @staticmethod
    def read_line() -> str:
        return input()

    @staticmethod
    def input(prompt: str, **kwargs) -> str:
        Console.__print("|INPT|", [prompt], show_insert = False, end = "\n       >>> ", **kwargs)
        return Console.read_line()





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
            if Console._limit_mpi_output_ranks is None or get_mpi_rank() in Console._limit_mpi_output_ranks:
                return func(f" ({get_mpi_rank()})", *args, **kwargs)
            else:
                return lambda *args, **kwargs: None
        if _settings_object.mpi_avalible:
            return wrapper
        else:
            return lambda *args, **kwargs: func("", *args, **kwargs)

[DeprecationWarning]
class OldConsole(object):

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
            raise ValueError("Negative values cannot be MPI rank indexes.")
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
                raise ValueError("Negative values cannot be MPI rank indexes.")
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
    @_PrivateModuleFunctions._mpi_wrapper # Still necessary to set auto-flushing etc.
    @_PrivateModuleFunctions._debug_wrapper
    @_PrivateModuleFunctions._slurm_wrapper
    def print_raw(_, firstValue = "", *args, **kwargs):
        """
        Print with no extra layout alterations but retaining all the functionality that the Console methods offer for MPI rank limitations and auto-flushing.
        """
        print(firstValue, *args, **kwargs)

    @staticmethod
    @_PrivateModuleFunctions._mpi_wrapper # Still necessary to set auto-flushing etc.
    @_PrivateModuleFunctions._debug_wrapper
    @_PrivateModuleFunctions._slurm_wrapper
    def print_raw_verbose(_, firstValue = "", *args, **kwargs):
        """
        Print (when verbose output is enabled) with no extra layout alterations but retaining all the functionality that the Console methods offer for MPI rank limitations and auto-flushing.
        """
        if _settings_object.verbose:
            print(firstValue, *args, **kwargs)

    @staticmethod
    @_PrivateModuleFunctions._mpi_wrapper # Still necessary to set auto-flushing etc.
    @_PrivateModuleFunctions._debug_wrapper
    @_PrivateModuleFunctions._slurm_wrapper
    def print_raw_debug(_, firstValue = "", *args, **kwargs):
        """
        Print (when verbose output is enabled) with no extra layout alterations but retaining all the functionality that the Console methods offer for MPI rank limitations and auto-flushing.
        """
        if _settings_object.debug:
            print(firstValue, *args, **kwargs)

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
