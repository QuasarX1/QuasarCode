from ..._global_settings import settings_object as _settings_object
from ...MPI import get_mpi_rank

class _PrivateModuleFunctions(object):
    @staticmethod
    def _slurm_wrapper(func):
        def wrapper(*args, **kwargs):
            if _settings_object.slurm:
                if "flush" not in kwargs:
                    kwargs["flush"] = True
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def _debug_wrapper(func):
        def wrapper(*args, **kwargs):
            if _settings_object.debug:
                if "flush" not in kwargs:
                    kwargs["flush"] = True
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def _mpi_wrapper(func):
        def wrapper(*args, **kwargs):
            if "flush" not in kwargs:
                kwargs["flush"] = True
            return func(f" ({get_mpi_rank()})", *args, **kwargs)
        if _settings_object.mpi_avalible:
            return wrapper
        else:
            return lambda *args, **kwargs: func("", *args, **kwargs)

class Console(object):

    __print_custom_newline_spaces = "                "
    @staticmethod
    def __print_custom_newline_format(mpi_rank_insert, s):
        return str(s).replace("\n", f"\n{Console.__print_custom_newline_spaces}" + (" " * len(mpi_rank_insert)))

    @staticmethod
    @_PrivateModuleFunctions._mpi_wrapper
    @_PrivateModuleFunctions._debug_wrapper
    def print_info(mpi_rank_insert, firstValue = "", *args, **kwargs):
        print(f"--|| INFO ||--{mpi_rank_insert}  {Console.__print_custom_newline_format(mpi_rank_insert, firstValue)}", *[Console.__print_custom_newline_format(mpi_rank_insert, arg) for arg in args], **kwargs)

    def print_verbose_info(firstValue = "", *args, **kwargs):
        if _settings_object.verbose:
            Console.print_info(firstValue, *args, **kwargs)

    @staticmethod
    @_PrivateModuleFunctions._mpi_wrapper
    @_PrivateModuleFunctions._debug_wrapper
    def print_warning(mpi_rank_insert, firstValue = "", *args, **kwargs):
        print(f"--\u00BF\u00BF WARN ??--{mpi_rank_insert}  {Console.__print_custom_newline_format(mpi_rank_insert, firstValue)}", *[Console.__print_custom_newline_format(mpi_rank_insert, arg) for arg in args], **kwargs)

    @staticmethod
    def print_verbose_warning(firstValue = "", *args, **kwargs):
        if _settings_object.verbose:
            Console.print_warning(firstValue, *args, **kwargs)

    @staticmethod
    @_PrivateModuleFunctions._mpi_wrapper
    @_PrivateModuleFunctions._debug_wrapper
    def print_error(mpi_rank_insert, firstValue = "", *args, **kwargs):
        print(f"--!! ERRO !!--{mpi_rank_insert}  {Console.__print_custom_newline_format(mpi_rank_insert, firstValue)}", *[Console.__print_custom_newline_format(mpi_rank_insert, arg) for arg in args], **kwargs)

    def print_verbose_error(firstValue = "", *args, **kwargs):
        if _settings_object.verbose:
            Console.print_error(firstValue, *args, **kwargs)

    @staticmethod
    @_PrivateModuleFunctions._mpi_wrapper
    @_PrivateModuleFunctions._debug_wrapper
    def print_debug(mpi_rank_insert, firstValue = "", *args, **kwargs):
        if _settings_object.debug:
            print(f"--<< DEBG >>--{mpi_rank_insert}  {Console.__print_custom_newline_format(mpi_rank_insert, firstValue)}", *[Console.__print_custom_newline_format(mpi_rank_insert, arg) for arg in args], **kwargs)

    @staticmethod
    def pause(exit = False):
        input("Press enter to {}... ".format("exit" if exit else "continue"))
