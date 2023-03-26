from QuasarCode._global_settings import settings_object as __settings_object
from QuasarCode.MPI import get_mpi_rank

def __debug_wrapper(func):
    def wrapper(*args, **kwargs):
        if __settings_object.debug:
            if "flush" not in kwargs:
                kwargs["flush"] = True
        return func(*args, **kwargs)
    return wrapper

def __mpi_wrapper(func):
    def wrapper(*args, **kwargs):
        if "flush" not in kwargs:
            kwargs["flush"] = True
        return func(f" ({get_mpi_rank()})", *args, **kwargs)
    if __settings_object.mpi_avalible:
        return wrapper
    else:
        return lambda *args, **kwargs: func("", *args, **kwargs)

__print_custom_newline_spaces = "                "
def __print_custom_newline_format(mpi_rank_insert, s):
    return str(s).replace("\n", f"\n{__print_custom_newline_spaces}" + (" " * len(mpi_rank_insert)))

@__mpi_wrapper
@__debug_wrapper
def print_info(mpi_rank_insert, firstValue = "", *args, **kwargs):
    print(f"--|| INFO ||--{mpi_rank_insert}  {__print_custom_newline_format(mpi_rank_insert, firstValue)}", *[__print_custom_newline_format(mpi_rank_insert, arg) for arg in args], **kwargs)

def print_verbose_info(firstValue = "", *args, **kwargs):
    if __settings_object.verbose:
        print_info(firstValue, *args, **kwargs)

@__mpi_wrapper
@__debug_wrapper
def print_warning(mpi_rank_insert, firstValue = "", *args, **kwargs):
    print(f"--\u00BF\u00BF WARN ??--{mpi_rank_insert}  {__print_custom_newline_format(mpi_rank_insert, firstValue)}", *[__print_custom_newline_format(mpi_rank_insert, arg) for arg in args], **kwargs)

def print_verbose_warning(firstValue = "", *args, **kwargs):
    if __settings_object.verbose:
        print_warning(firstValue, *args, **kwargs)

@__mpi_wrapper
@__debug_wrapper
def print_error(mpi_rank_insert, firstValue = "", *args, **kwargs):
    print(f"--!! ERRO !!--{mpi_rank_insert}  {__print_custom_newline_format(mpi_rank_insert, firstValue)}", *[__print_custom_newline_format(mpi_rank_insert, arg) for arg in args], **kwargs)

def print_verbose_error(firstValue = "", *args, **kwargs):
    if __settings_object.verbose:
        print_error(firstValue, *args, **kwargs)

@__mpi_wrapper
@__debug_wrapper
def print_debug(mpi_rank_insert, firstValue = "", *args, **kwargs):
    if __settings_object.debug:
        print(f"--<< DEBG >>--{mpi_rank_insert}  {__print_custom_newline_format(mpi_rank_insert, firstValue)}", *[__print_custom_newline_format(mpi_rank_insert, arg) for arg in args], **kwargs)

def pause(exit = False):
    input("Press enter to {}... ".format("exit" if exit else "continue"))
