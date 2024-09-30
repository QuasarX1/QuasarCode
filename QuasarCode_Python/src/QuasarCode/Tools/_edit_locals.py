from collections.abc import Callable, Iterable, Sequence
from typing import TypeVar, ParamSpec
from functools import wraps
import inspect



P = ParamSpec("P")
T = TypeVar("T")



def update_locals(*local_variable_parameter_names_or_indexes: str|int, remove_target_arguments: bool = True):
    if len(local_variable_parameter_names_or_indexes) == 0:
        raise IndexError("No local variable parameter information provided.")

    def inner(func: Callable[P, T]) -> Callable[P, None]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            args = list(args) # Make args mutable

            SKIP_THIS_FRAME = True # Adds a local variable that can be checked for in case of stacked calls
            frame = inspect.currentframe()
            while True:
                frame = frame.f_back
                if frame is None:
                    raise RuntimeError("Unable to find root calling frame. A valid calling frame must not have a local named \"SKIP_THIS_FRAME\".")
                calling_scope_locals = frame.f_locals
                if "SKIP_THIS_FRAME" not in calling_scope_locals:
                    break

            target_variable_names = []
            removable_args_indexes = []
            removable_kwargs_keys = []
            for name_param_location in local_variable_parameter_names_or_indexes:
                if isinstance(name_param_location, int):
                    removable_args_indexes.append(name_param_location)
                    target_variable_names.append(args[name_param_location])
                else:
                    removable_kwargs_keys.append(name_param_location)
                    target_variable_names.append(kwargs[name_param_location])
            if remove_target_arguments:
                removable_args_indexes.sort(reverse = True)
                for i in removable_args_indexes:
                    args.pop(i)
                for key in removable_kwargs_keys:
                    kwargs.pop(key)

            result = func(*args, **kwargs)

            if len(target_variable_names) == 1:
                calling_scope_locals[target_variable_names[0]] = result

            else:
                if not isinstance(result, Iterable):
                    raise TypeError(f"Decorated method return type of {type(result)} is not Iterable but multiple target varaibles were specified. Unable to unpack non-iterable output.")
                result = tuple(result)
                if len(result) != len(target_variable_names):
                    raise IndexError(f"Unable to unpack {len(result)} values into {len(target_variable_names)} variables.")
                for i in range(len(target_variable_names)):
                    calling_scope_locals[target_variable_names[i]] = result[i]

        return wrapper
    return inner



def read_locals(*local_variable_parameter_names_or_indexes: str|int):

    if len(local_variable_parameter_names_or_indexes) == 0:
        def inner(func: Callable[P, T]) -> Callable[P, T]:
            return func
        return inner

    def inner(func: Callable[P, T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            args = list(args) # Make args mutable

            SKIP_THIS_FRAME = True # Adds a local variable that can be checked for in case of stacked calls
            frame = inspect.currentframe()
            while True:
                frame = frame.f_back
                if frame is None:
                    raise RuntimeError("Unable to find root calling frame. A valid calling frame must not have a local named \"SKIP_THIS_FRAME\".")
                calling_scope_locals = frame.f_locals
                if "SKIP_THIS_FRAME" not in calling_scope_locals:
                    break

            for name_param_location in local_variable_parameter_names_or_indexes:
                if isinstance(name_param_location, int):
                    args[name_param_location] = calling_scope_locals[args[name_param_location]]
                else:
                    kwargs[name_param_location] = calling_scope_locals[kwargs[name_param_location]]

            return func(*args, **kwargs)

        return wrapper
    return inner



def use_locals(readable_parameter_names_or_indexes: str|int|Sequence[str|int], updateable_parameter_names_or_indexes: str|int|Sequence[str|int], remove_extra_updateable_target_arguments: bool = True):
    if not isinstance(readable_parameter_names_or_indexes, Sequence):
        readable_parameter_names_or_indexes = (readable_parameter_names_or_indexes, )
    if not isinstance(updateable_parameter_names_or_indexes, Sequence):
        updateable_parameter_names_or_indexes = (updateable_parameter_names_or_indexes, )
    
    if len(updateable_parameter_names_or_indexes) == 0:
        raise IndexError("No updateable local variable parameter information provided.")

    def inner(func: Callable[P, T]) -> Callable[P, None]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            args = list(args) # Make args mutable

            SKIP_THIS_FRAME = True # Adds a local variable that can be checked for in case of stacked calls
            frame = inspect.currentframe()
            while True:
                frame = frame.f_back
                if frame is None:
                    raise RuntimeError("Unable to find root calling frame. A valid calling frame must not have a local named \"SKIP_THIS_FRAME\".")
                calling_scope_locals = frame.f_locals
                if "SKIP_THIS_FRAME" not in calling_scope_locals:
                    break

            target_variable_names = []
            removable_args_indexes = []
            removable_kwargs_keys = []
            for name_param_location in updateable_parameter_names_or_indexes:
                if isinstance(name_param_location, int):
                    if name_param_location not in readable_parameter_names_or_indexes:
                        removable_args_indexes.append(name_param_location)
                    target_variable_names.append(args[name_param_location])
                else:
                    if name_param_location not in readable_parameter_names_or_indexes:
                        removable_kwargs_keys.append(name_param_location)
                    target_variable_names.append(kwargs[name_param_location])

            for name_param_location in readable_parameter_names_or_indexes:
                if isinstance(name_param_location, int):
                    args[name_param_location] = calling_scope_locals[args[name_param_location]]
                else:
                    kwargs[name_param_location] = calling_scope_locals[kwargs[name_param_location]]

            if remove_extra_updateable_target_arguments:
                removable_args_indexes.sort(reverse = True)
                for i in removable_args_indexes:
                    args.pop(i)
                for key in removable_kwargs_keys:
                    kwargs.pop(key)

            result = func(*args, **kwargs)

            if len(target_variable_names) == 1:
                calling_scope_locals[target_variable_names[0]] = result

            else:
                if not isinstance(result, Iterable):
                    raise TypeError(f"Decorated method return type of {type(result)} is not Iterable but multiple target varaibles were specified. Unable to unpack non-iterable output.")
                result = tuple(result)
                if len(result) != len(target_variable_names):
                    raise IndexError(f"Unable to unpack {len(result)} values into {len(target_variable_names)} variables.")
                for i in range(len(target_variable_names)):
                    calling_scope_locals[target_variable_names[i]] = result[i]

        return wrapper
    return inner
