import sys
import traceback
from typing import TypeVar, Generic, Any, Union, Collection, Sequence, List, Tuple, Dict, Callable
from abc import ABC, abstractmethod

from ..IO.Text._console import Console# print_info, print_verbose_info, print_warning, print_verbose_warning, print_error, print_verbose_error, print_debug
from .._global_settings import settings_object as _settings_object
from ..MPI import get_mpi_rank
from ..Tools._async import start_main_async

T = TypeVar("T")
U = TypeVar("U")

from types import ModuleType
from ..Data import AuthorInfomation as _AuthorInfomation, VersionInfomation as _VersionInfomation
from datetime import date as _date
from functools import wraps



def ScriptWrapper_passthrough_converter(value: str) -> str:
    return value

def ScriptWrapper_bool_converter(value: str) -> bool:
    return value.lower() in ("true", "t", "yes", "y", "1", "accept", "allow", "confirm")

def ScriptWrapper_filter_converter(value: str) -> Tuple[bool, ...]:
    return tuple(ScriptWrapper.bool_converter(element) for element in value.lower())

#def ScriptWrapper_reverse_flag_converter(value: bool) -> bool:
#    return not value

def ScriptWrapper_make_list_converter(seperator = ",", item_converters: Union[Sequence[Callable[[str], Any]], Callable[[str], Any], None] = None):
    if item_converters is None:
        item_converters = ScriptWrapper.passthrough_converter
    def list_converter(value: str) -> Any:
        if not isinstance(item_converters, Sequence):
            return [item_converters(item) if item != "" or item_converters == ScriptWrapper.passthrough_converter or item_converters == str else None for item in value.split(seperator)]
        else:
            converters_for_use: List[Callable[[str], Any]] = list(item_converters)
            strings = value.split(seperator)
            while len(converters_for_use) < len(strings):
                converters_for_use.append(ScriptWrapper.passthrough_converter)
            return [converters_for_use[i](strings[i]) if strings[i] != "" or converters_for_use[i] == ScriptWrapper.passthrough_converter or converters_for_use == str else None for i in range(len(strings))]
    return list_converter



class ScriptWrapper_ParamSpec(List["ScriptWrapper_ParamBase"]):
    """
    The parameters for a ScriptWrapper instance.
    """

    def __init__(
            self,
            *params: "ScriptWrapper_ParamBase",
            common_params_have_short_names: bool = True,
            custom_help_param: Union["ScriptWrapper_Flag", None] = None,
            custom_debug_param: Union["ScriptWrapper_Flag", None] = None,
            custom_verbose_param: Union["ScriptWrapper_Flag", None] = None
        ) -> None:
        super().__init__()
        self.__help_param    = custom_help_param if custom_help_param is not None else make_help_flag(long_name_only = not common_params_have_short_names)
        self.__debug_param   = custom_debug_param if custom_debug_param is not None else make_debug_flag(long_name_only = not common_params_have_short_names)
        self.__verbose_param = custom_verbose_param if custom_verbose_param is not None else make_verbose_flag(long_name_only = not common_params_have_short_names)
        self.__special_param_names = (self.__help_param.name, self.__debug_param.name, self.__verbose_param.name)
        self.__special_param_short_names = (self.__help_param.short_name, self.__debug_param.short_name, self.__verbose_param.short_name)
        self.add(self.__help_param   )
        self.add(self.__debug_param  )
        self.add(self.__verbose_param)
        self.add(*params)

    @property
    def help_param(self) -> "ScriptWrapper_Flag":
        return self.__help_param
    @property
    def debug_param(self) -> "ScriptWrapper_Flag":
        return self.__debug_param
    @property
    def verbose_param(self) -> "ScriptWrapper_Flag":
        return self.__verbose_param
    @property
    def special_param_names(self) -> Tuple[str, str, str]:
        return self.__special_param_names
    def special_param_short_names(self) -> Tuple[Union[str, None], Union[str, None], Union[str, None]]:
        return self.__special_param_short_names

    def add(self, *params: "ScriptWrapper_ParamBase"):
        """
        Insert parameter definitions.

        ScriptWrapper_ParamSpec_Error will be raised if an invalid addition is requested.
        In the event of a ScriptWrapper_ParamSpec_Error, no additions will be performed.
        """
        
        try:
            for param in params:
                for test_param in self:
                    if len(self) > 0 and isinstance(param, ScriptWrapper_PositionalParam) and self[-1].name not in self.__special_param_names and not isinstance(self[-1], ScriptWrapper_PositionalParam):
                        raise ScriptWrapper_ParamSpec_Error(f"Attempted to register a positional parameter ({param.name}) after registering a number of non-positional parameters.\nAll positional parameters must be registered in-order and before any non-positional parameters.")
                    if param.name == test_param.name:
                        raise ScriptWrapper_ParamSpec_Error(f"Attempted to register two parameters with the name \"{param.name}\".")
                    if param.short_name == test_param.short_name and param.short_name is not None:
                        raise ScriptWrapper_ParamSpec_Error(f"Attempted to register two parameters with the short name \"{param.short_name}\".")
                    if param.target_parameter_name == test_param.target_parameter_name:
                        if not param.can_conflict_with(test_param):
                            raise ScriptWrapper_ParamSpec_Error(f"Attempted to register parameter {param.name} that targets the same function parameter ({param.target_parameter_name}) as {test_param.name}, but does not indicate the later as a conflict.\nParameters that target the same function parameter must indicate each other as conflicts!")
                        elif not test_param.can_conflict_with(param):
                            raise ScriptWrapper_ParamSpec_Error(f"Attempted to register parameter {param.name} that targets the same function parameter ({param.target_parameter_name}) as {test_param.name}, but the latter does not indicate the former as a conflict.\nParameters that target the same function parameter must indicate each other as conflicts!")
                        if isinstance(param, ScriptWrapper_RequiredParam):
                            raise ScriptWrapper_ParamSpec_Error(f"Attempted to register parameter {param.name} that targets the same function parameter ({param.target_parameter_name}) as {test_param.name}, but the former is a required parameter.\nRequired parameters must be the sole parameter definition for a particular target function parameter.")
                        elif isinstance(test_param, ScriptWrapper_RequiredParam):
                            raise ScriptWrapper_ParamSpec_Error(f"Attempted to register parameter {param.name} that targets the same function parameter ({param.target_parameter_name}) as {test_param.name}, but the latter is a required parameter.\nRequired parameters must be the sole parameter definition for a particular target function parameter.")
                        if param.requires(test_param):
                            raise ScriptWrapper_ParamSpec_Error(f"Attempted to register parameter {param.name} that targets the same function parameter ({param.target_parameter_name}) as {test_param.name}, but the former requires the latter.\nParameter definitions that target the same function parameter cannot also require each other!")
                        elif param.is_required_by(test_param):
                            raise ScriptWrapper_ParamSpec_Error(f"Attempted to register parameter {param.name} that targets the same function parameter ({param.target_parameter_name}) as {test_param.name}, but the latter requires the former.\nParameter definitions that target the same function parameter cannot also require each other!")
                        if param.default is not None and test_param.default is not None:
                            raise ScriptWrapper_ParamSpec_Error(f"Attempted to register parameter {param.name} that targets the same function parameter ({param.target_parameter_name}) as {test_param.name}, but both specify a non-null default value.\nParameter definitions that target the same function parameter cannot include more than one non-null default value!")
                    if param.can_conflict_with(test_param):
                        if isinstance(test_param, ScriptWrapper_RequiredParam):
                            raise ScriptWrapper_ParamSpec_Error(f"Attempted to register parameter {param.name} with a required parameter ({test_param.name}) as a conflict.\nConflicting parameters cannot be required parameters!")
                        elif param.is_required_by(test_param):
                            raise ScriptWrapper_ParamSpec_Error(f"Attempted to register parameter {param.name} with {test_param.name} as a conflict, however {test_param.name} lists {param.name} as a requirement.\nConflicting parameters cannot also require each other!")
                    if test_param.can_conflict_with(param):
                        if isinstance(param, ScriptWrapper_RequiredParam):
                            raise ScriptWrapper_ParamSpec_Error(f"Attempted to register parameter {param.name} (a required parameter) but ({test_param.name}) indicates {param.name} is a conflict.\nConflicting parameters cannot be required parameters!")
                        elif param.requires(test_param):
                            raise ScriptWrapper_ParamSpec_Error(f"Attempted to register parameter {param.name} with {test_param.name} as a requirement, however {test_param.name} lists {param.name} as a conflict.\nConflicting parameters cannot also require each other!")
                param._regester_spec(self)
                self.append(param)
        except Exception as e:
            for param in params:
                param._regester_spec(None)
                try:
                    self.remove(param)
                except: pass
            raise e
        
    def get_keyword_arguments(self) -> Dict[str, Union[Any, None]]:
        kwargs: Dict[str, Union[Any, None]] = {}
        for param in self:
            if param.name in self.special_param_names:
                continue # Special params shouls not be passed to the target function.
            if param.target_parameter_name not in kwargs:
                kwargs[param.target_parameter_name] = None
            if param.has_non_null_value:
                kwargs[param.target_parameter_name] = param.value
        return kwargs
        
    def reset(self) -> None:
        """
        Reset all parameters back to their starting values.
        """
        
        for p in self:
            p._reset()
    
    #TODO: handle __add__ and other list type features!

class ScriptWrapper_ParamSpec_Error(Exception):
    """
    An error arrising from a ScriptWrapper_ParamSpec object.
    """

class ScriptWrapper_ParamBase(ABC, Generic[T]):
    """
    
    """

    def __init__(
                    self,
                    name:                str,
                    short_name:          Union[str, None]                                               = None,
                    sets_param:          Union[str, None]                                               = None,
                    default_value:       Union[T, None]                                                 = None,
                    conversion_function: Union[Callable[[str], T], None]                                = None,
                    conflicts:           Union[Collection[Union[str, "ScriptWrapper_ParamBase"]], None] = None,
                    requirements:        Union[Collection[Union[str, "ScriptWrapper_ParamBase"]], None] = None,
                    description:         Union[str, None]                                               = None
                ) -> None:
        self.__name: str = name
        self.__short_name: Union[str, None] = short_name
        self.__parameter_name_to_set: str = sets_param if sets_param is not None else name.replace("-", "_")
        self.__default_value: Union[T, None] = default_value
#        self.__conversion_function: Callable[[str], T] = conversion_function if conversion_function is not None else ScriptWrapper.passthrough_converter
        self.__conversion_function: Callable[[str], T] = conversion_function if conversion_function is not None else ScriptWrapper_passthrough_converter
        self.__conflicting_param_names: Tuple[str, ...] = tuple((v.name if isinstance(v, ScriptWrapper_ParamBase) else v) for v in conflicts   ) if conflicts is not None else tuple()
        self.__requirement_param_names: Tuple[str, ...] = tuple((v.name if isinstance(v, ScriptWrapper_ParamBase) else v) for v in requirements) if requirements is not None else tuple()
        self.__description: str = description if description is not None else ""

        self.__value: Union[T, None] = self.__default_value
        self.__value_explicitly_set = False

        self.__spec: Union[ScriptWrapper_ParamSpec, None] = None

        invalid_params = set(self.__conflicting_param_names).intersection(set(self.__requirement_param_names))
        if len(invalid_params) > 0:
            raise ValueError(f"Conflicts and requirements contained common parameters: {invalid_params}")

    @property
    def name(self) -> str:
        """
        Name of the parameter.

        This parameter may be specified by preceding the name with two dashes (e.g. '--<param name> <appropriate value>').
        """
        return self.__name

    @property
    def short_name(self) -> Union[str, None]:
        """
        Short string alternate name for the parameter.

        This parameter may be specified by preceding the name with a single dash (e.g. '-<short param name> <appropriate value>').
        """
        return self.__short_name

    @property
    def target_parameter_name(self) -> str:
        """
        Name of the function kwarg set by this parameter.
        """
        return self.__parameter_name_to_set

    @property
    def default(self) -> Union[T, None]:
        """
        Default value if this parameter is not specified.
        """
        return self.__default_value

    @property
    def conversion_function(self) -> Callable[[str], T]:
        """
        Function to be used for converting inputs to the intended type.
        """
        return self.__conversion_function

    @property
    def conflicts(self) -> Tuple[str, ...]:
        """
        Parameters that cannot be set if this parameter is used.
        """
        return self.__conflicting_param_names
    
    @property
    def requirements(self) -> Tuple[str, ...]:
        """
        Parameters that must be set if this parameter is used.
        """
        return self.__requirement_param_names

    @property
    def description(self) -> str:
        """
        Description of the parameter.
        """
        return self.__description

    @property
    def value(self) -> Union[T, None]:
        """
        Current assigned value.
        """
        return self.__value

    def __str__(self) -> str:
        return f"ScriptWrapper Parameter: {self.__name}\n{self.__description}"
    
    def _regester_spec(self, param_spec: Union[ScriptWrapper_ParamSpec, None]) -> None:
        self.__spec = param_spec

    @property
    def _spec(self) -> Union[ScriptWrapper_ParamSpec, None]:
        return self.__spec
    
    def can_conflict_with(self, test_param: "ScriptWrapper_ParamBase") -> bool:
        """
        Can this parameter conflict with another?
        """
        return test_param.name in self.__conflicting_param_names

    def conflicts_with(self, test_param: "ScriptWrapper_ParamBase") -> bool:
        """
        Does this parameter conflict with another, given their current state?
        """
        return self.can_conflict_with(test_param) and self.is_explicitly_set and test_param.is_explicitly_set
    
    def requires(self, test_param: "ScriptWrapper_ParamBase") -> bool:
        """
        Does this parameter require another?
        """
        return test_param.name in self.__requirement_param_names
    
    def is_required_by(self, test_param: "ScriptWrapper_ParamBase") -> bool:
        """
        Does another parameter require this one?
        """
        return test_param.requires(self)
    
    @property
    def has_non_null_value(self) -> bool:
        """
        Does the param have a value that isn't None.
        """
        return self.__value is not None
    
    @property
    def is_explicitly_set(self) -> bool:
        """
        Has a value been assigned to the param.
        """
        return self.__value_explicitly_set
    
    def _set(self, value: T, /) -> None:
        self.__value = value
        self.__value_explicitly_set = True

    def _reset(self):
        self.__value = self.__default_value
        self.__value_explicitly_set = False

    @abstractmethod
    def set_from_args(self, named_arguments: Dict[str, str]) -> bool:
        """
        Attempt to set the value of this parameter given the avalible argument strings.
        """
        raise NotImplementedError("Attempted to call an abstract method.")
    
    def validate(self) -> None:
        """
        Ensure the value assigned to this patameter is valid after parsing all parameters.
        """
        if self.__spec is None:
            raise ScriptWrapper_Param_ValidityError(self, f"Parameter {self.name} was not assigned to a ScriptWrapper_ParamSpec object.")
        if self.has_non_null_value:
            for test_param in self.__spec:
                if self.conflicts_with(test_param):
                    raise ScriptWrapper_Param_ConflictError(self, test_param)
                elif self.requires(test_param) and not test_param.is_explicitly_set:
                    raise ScriptWrapper_Param_MissingRequirementError(self, test_param)
    
class ScriptWrapper_Param_ValidityError(Exception):
    """
    Parameter definition was invalid after parsing of arguments.
    """
    def __init__(self, param_object: ScriptWrapper_ParamBase, message: str):
        self.raising_parameter: ScriptWrapper_ParamBase = param_object
        super().__init__(message)
class ScriptWrapper_Param_ValueError(ScriptWrapper_Param_ValidityError, ValueError):
    """
    Parameter definition was assigned an invalid value.
    """
    def __init__(self, param: ScriptWrapper_ParamBase, value_string: str):
        super().__init__(param, f"Parameter {param.name} was passed an invalid value: \"{value_string}\"")
class ScriptWrapper_Param_TypeError(ScriptWrapper_Param_ValidityError, TypeError):
    """
    Parameter definition parsed an argument and produced an invalid type.
    """
    def __init__(self, param: ScriptWrapper_ParamBase):
        super().__init__(param, f"Parameter {param.name} produced a value with an invalid type: {type(param.value)}")
class ScriptWrapper_Param_UnsetError(ScriptWrapper_Param_ValidityError):
    """
    Parameter definition required a value, but none was passed as an argument.
    """
    def __init__(self, param: ScriptWrapper_ParamBase):
        super().__init__(param, f"Parameter {param.name} requires a value but none was provided.")
class ScriptWrapper_Param_ConflictError(ScriptWrapper_Param_ValidityError):
    """
    Parameter definition was assigned a value, along woth a conflicting parameter.
    """
    def __init__(self, param: ScriptWrapper_ParamBase, conflicting_param: ScriptWrapper_ParamBase):
        self.conflicting_parameter: ScriptWrapper_ParamBase = conflicting_param
        super().__init__(param, f"Parameter {param.name} conflicts with {conflicting_param.name} and both were set.")
class ScriptWrapper_Param_MissingRequirementError(ScriptWrapper_Param_ValidityError):
    """
    Parameter definition was assigned a value, however a required parameter was not.
    """
    def __init__(self, param: ScriptWrapper_ParamBase, required_param: ScriptWrapper_ParamBase):
        self.required_parameter: ScriptWrapper_ParamBase = required_param
        super().__init__(param, f"Parameter {param.name} requires {required_param.name}, however the later was not explicitly specified.")

class ScriptWrapper_ArgParamBase(ScriptWrapper_ParamBase[T]):
    def __init__(
                    self,
                    name:                str,
                    short_name:          Union[str, None]                                               = None,
                    sets_param:          Union[str, None]                                               = None,
                    default_value:       Union[Any, None]                                               = None,
                    conversion_function: Union[Callable[[str], T], None]                                = None,
                    type_check:          Union[type, None]                                              = None,
                    conflicts:           Union[Collection[Union[str, ScriptWrapper_ParamBase]], None]   = None,
                    requirements:        Union[Collection[Union[str, ScriptWrapper_ParamBase]], None]   = None,
                    description:         Union[str, None]                                               = None
                ) -> None:
        super().__init__(
                            name = name,
                      short_name = short_name,
                      sets_param = sets_param,
                   default_value = default_value,
             conversion_function = conversion_function,
                       conflicts = conflicts,
                    requirements = requirements,
                     description = description
        )
        self.__required_type: Union[type, None] = type_check
        if default_value is not None:
            self._set(default_value)

    @property
    def _type_to_check_against(self) -> Union[type, None]:
        """
        Type of which a valid resulting value must be an instance.
        """
        return self.__required_type

    def _set_from_raw(self, input_string: str, /) -> None:
        self._set(self.conversion_function(input_string))

    def set_from_args(self, named_arguments: Dict[str, str]) -> bool:
        if self.name in named_arguments:
            self._set_from_raw(named_arguments[self.name])
            return True
        return False

    def validate(self):
        if self._type_to_check_against is not None and self.is_explicitly_set and not isinstance(self.value, self._type_to_check_against):
            raise ScriptWrapper_Param_TypeError(self)
        super().validate()

class ScriptWrapper_OptionalParam(ScriptWrapper_ArgParamBase[T]):
    """
    
    """

class ScriptWrapper_RequiredParam(ScriptWrapper_ArgParamBase[T]):
    """
    
    """

    def __init__(
                    self,
                    name:                   str,
                    short_name:             Union[str, None]                = None,
                    sets_param:             Union[str, None]                = None,
                    conversion_function:    Union[Callable[[str], T], None] = None,
                    type_check:             Union[type, None]               = None,
                    description:            Union[str, None]                = None
                ) -> None:
        super().__init__(
                            name = name,
                      short_name = short_name,
                      sets_param = sets_param,
                   default_value = None,
             conversion_function = conversion_function,
                      type_check = type_check,
                       conflicts = None,
                    requirements = None,
                     description = description
        )

    def validate(self):
        if not self.is_explicitly_set:
            raise ScriptWrapper_Param_UnsetError(self)
        super().validate()

class ScriptWrapper_PositionalParam(ScriptWrapper_RequiredParam[T]):
    """
    A type of ScriptWrapper parameter that must be specified at in the parameter list before any optional parameters or flags.
    This type of parameter is not required to be specified by name (though may be if desired).
    These parameters have no default value, and must be assigned a value.
    """

    def set_from_positional_arg(self, arg_string: str) -> None:
        self._set_from_raw(arg_string)

class ScriptWrapper_Flag(ScriptWrapper_ParamBase[bool]):
    """
    A type of ScriptWrapper parameter that takes no argument and toggles a single boolean state.
    """

    def __init__(
                    self,
                    name:           str,
                    short_name:     Union[str, None]                                                = None,
                    sets_param:     Union[str, None]                                                = None,
                    inverted:       bool                                                            = False,
                    conflicts:      Union[Collection[Union[str, ScriptWrapper_ParamBase]], None]    = None,
                    requirements:   Union[Collection[Union[str, ScriptWrapper_ParamBase]], None]    = None,
                    description:    Union[str, None]                                                = None
                ) -> None:
        super().__init__(
                            name = name,
                      short_name = short_name,
                      sets_param = sets_param,
                   default_value = bool(inverted), # Cast to a bool just in case attempt is made to set field with an integer
             conversion_function = None,
                       conflicts = conflicts,
                    requirements = requirements,
                     description = description
        )
        self.__inverted = inverted

    @property
    def inverted(self) -> bool:
        """
        Type of which a valid resulting value must be an instance.
        """
        return self.__inverted

    def set_from_args(self, named_arguments: Dict[str, str]) -> bool:
        if self.name in named_arguments:
            self._set(not self.__inverted)
            return True
        return False



def make_help_flag(name = "help", short_name = "h", long_name_only = False):
    return ScriptWrapper_Flag(
               name = name,
         short_name = None if long_name_only else short_name,
         sets_param = None,
           inverted = False,
        description = "Display this docstring."
    )
def make_debug_flag(name = "debug", short_name = "d", long_name_only = False):
    return ScriptWrapper_Flag(
               name = name,
         short_name = None if long_name_only else short_name,
         sets_param = None,
           inverted = False,
        description = "Display debug infomation."
    )
def make_verbose_flag(name = "verbose", short_name = "v", long_name_only = False):
    return ScriptWrapper_Flag(
               name = name,
         short_name = None if long_name_only else short_name,
         sets_param = None,
           inverted = False,
        description = "Display progression infomation."
    )



class ScriptWrapper(object):
#    """
#    Singelton that handles command argument parsing for the currently running program.
#    Constructor Arguments:
#              str filename                 --> The name of the entrypoint file.
#              str author                   --> The name(s) of the file author(s).
#              str version_string           --> String indicating the current version of the file.
#              str edit_date                --> String indicating the date of the last edit.
#              str description              --> A description of the function of the script.
#        list[str] dependancies             --> A list of dependancies of the script.
#        list[str] usage_paramiter_examples --> A list of strings demonstrating example paramiter
#                                                   lists (exclude the call to the script).
#             list positional_params        --> List of paramiter information for paramiters that must
#                                                   appear at the start of the argument list in order
#                                                   without a flag identifier (each paramiter is a list
#                                                   with fields as below).
#                                                   [
#                                                    name, description, conversion func (nullable)
#                                                   ]
#             list params                   --> List of paramiter information (each paramiter is a list
#                                                   with fields as below).
#                                                   [
#                                                    name, short name (nullable), description,
#                                                    required?, flag?, conversion func (nullable),
#                                                    default value, mutually exclusive flags (list[str])
#                                                   ]
#    Public Methods:
#               run
#        static passthrough_converter
#        static bool_converter
#        static make_list_converter
#    """
    
    # Convinience type aliases for accessing dependant types
    AuthorInfomation  = _AuthorInfomation
    VersionInfomation = _VersionInfomation
    ParamSpec         = ScriptWrapper_ParamSpec
    OptionalParam     = ScriptWrapper_OptionalParam
    RequiredParam     = ScriptWrapper_RequiredParam
    PositionalParam   = ScriptWrapper_PositionalParam
    Flag              = ScriptWrapper_Flag

    #TODO: set this up to enforce a singleton
    #__initialised = False
    #__instance = None
    #
    #def __new__(cls, *args, **kwargs):
    #    if ScriptWrapper.__initialised:
    #        #raise RuntimeError("A running program may only define one ScriptWrapper instance.")
    #        return ScriptWrapper.__instance
    #    else:
    #        ScriptWrapper.__initialised = True
    #        ScriptWrapper.__instance = super(ScriptWrapper, cls).__new__(cls)
    #        return ScriptWrapper.__instance

    def __init__(
                    self,
                    parameters:               Union[ScriptWrapper_ParamSpec,          List[ScriptWrapper_ParamBase], None] = None,
                    command:                  Union[str,                                                             None] = None,
                    filename:                 Union[str,                                                             None] = None,
                    authors:                  Union[Sequence[_AuthorInfomation],                                     None] = None,
                    version:                  Union[_VersionInfomation,               str,                           None] = None,
                    edit_date:                Union[_date,                                                           None] = None,
                    description:              Union[str,                                                             None] = None,
                    dependancies:             Union[Sequence[Union[ModuleType, str]],                                None] = None,
                    usage_paramiter_examples: Union[Sequence[str],                                                   None] = None
                ) -> None:
        
        if usage_paramiter_examples is not None and len(list(v for v in usage_paramiter_examples)) > 0 and command is None and filename is None:
            raise ValueError("Unable to render usage examples without either a command name or file name.")
        
        if parameters is None:
            parameters = ScriptWrapper_ParamSpec()
        elif not isinstance(parameters, ScriptWrapper_ParamSpec):
            parameters = ScriptWrapper_ParamSpec(*parameters)

        if version is None:
            version = _VersionInfomation.from_string("0.0.0")
        elif isinstance(version, str):
            version = _VersionInfomation.from_string(version)

        self.__parameters:               ScriptWrapper_ParamSpec       = parameters
        self.__command_name:             Union[str, None]              = command
        self.__file_name:                Union[str, None]              = filename
        self.__author_info:              Tuple[_AuthorInfomation, ...] = tuple(authors) if authors is not None else tuple()
        self.__version:                  _VersionInfomation            = version
        self.__edit_date:                Union[_date, None]            = edit_date
        self.__description:              Union[str, None]              = description
        self.__import_dependancies:      Tuple[str, ...]               = tuple((dep.__name__ if isinstance(dep, ModuleType) else dep) for dep in dependancies) if dependancies is not None else tuple()
        self.__usage_paramiter_examples: Tuple[str, ...]               = tuple(usage_paramiter_examples) if usage_paramiter_examples is not None else tuple()

        self.__help_string: str = ""
        self.__render_help_string()


        self.__parameter_lookup_by_name: Dict[str, ScriptWrapper_ParamBase] = { p.name : p for p in self.__parameters }
        self.__parameter_lookup_by_short_name: Dict[str, ScriptWrapper_ParamBase] = { p.short_name : p for p in self.__parameters if p.short_name is not None }
        self.__arguments_have_been_parsed: bool = False
        self.__raw_arguments: Union[Sequence[str], None] = None

        self.use_MPI = False
        self.MPI_print_non_root_process_errors = False

    def __render_help_string(self):
        self.__help_string = ""
        if self.__command_name is not None:
            self.__help_string     += f"\nCommand: {self.__command_name}"
        if self.__file_name is not None:
            self.__help_string     += f"\nFile:    {self.__file_name}"
        self.__help_string         += f"\nVersion: {self.__version.to_string(minimum_length = True)}"
        if self.__edit_date is not None:
            self.__help_string     += f"\nDate:     {self.__edit_date.strftime(_settings_object.date_format)}"
        if len(self.__author_info) > 0:
            self.__help_string     +=  "\nAuthor:  " if len(self.__author_info) == 1 else "\nAuthors: "
            for i, author in enumerate(self.__author_info):
                self.__help_string +=  ("\n         " if i > 0 else "") + f"{author.given_name} {author.family_name}" + ((" (" + (author.email_address if author.email_address is not None else "") + (" | " if author.email_address is not None and author.website_url is not None else "") + (author.website_url if author.email_address is not None else "") + ")") if author.email_address is not None or author.website_url is not None else "")
        if self.__description is not None:
            self.__help_string     += f"\n\n{self.__description}"
        self.__help_string += """

Commandline arguments & flags ( p = required positional parameter,
                                r = required parameter,
                               f  = optional flag,
                               f+ = optional parameter with an argument):"""
        name_max_width = max([len(parameter_definition.name) for parameter_definition in self.__parameters])
        short_name_max_width = max([len(parameter_definition.short_name) if parameter_definition.short_name is not None else 0 for parameter_definition in self.__parameters])
        indent_spacing = name_max_width + ((short_name_max_width + 5) if short_name_max_width > 0 else 0) + 20
        for parameter_definition in self.__parameters:
            self.__help_string     +=  ("\n\n    ({}) --{}{}" + (" || " if short_name_max_width > 0 else "") + "{}{}{}").format(
                (" p" if isinstance(parameter_definition, self.PositionalParam) else (" r" if isinstance(parameter_definition, self.RequiredParam) else ("f " if isinstance(parameter_definition, self.Flag) else "f+"))),
                parameter_definition.name,
                (name_max_width - len(parameter_definition.name)) * " ",
                "" if parameter_definition.short_name is None else f"-{parameter_definition.short_name}",
                " " * (short_name_max_width - (len(parameter_definition.short_name) if parameter_definition.short_name is not None else 1)),
                (" --> " + parameter_definition.description.replace("\n", "\n" + (" " * indent_spacing))) if parameter_definition.description is not None else ""
            )
        if len(self.__import_dependancies) > 0:
            self.__help_string     +=  "\n\nDependancies:"
            for dependancy in self.__import_dependancies:
                self.__help_string += f"\n    {dependancy}"
        if len(self.__usage_paramiter_examples) > 0:
            self.__help_string     +=  "\n\nExample Usage:"
            for param_list in self.__usage_paramiter_examples:
                self.__help_string += f"\n    {self.__command_name if self.__command_name is not None else f'python {self.__file_name}'} {param_list}"

    @property
    def help_string(self):
        return self.__help_string

    def parse_arguments(self, arguments: Union[Sequence[str], None] = None):

        self.__parameters.reset() # Make sure all parameters are unaltered from their starting values

        # Select the parameter strings
        self.__raw_arguments = arguments if arguments is not None else sys.argv[1:]
        number_of_raw_args = len(self.__raw_arguments)

        # Create a lookup of named parameters
        named_argument_lookup: Dict[str, str] = {}
        for arg_index, raw_arg in enumerate(self.__raw_arguments):
            if len(raw_arg) == 1:
                continue # Argument too short to be a parameter name
            if raw_arg[0] == "-":
                # Argument starts with a dash, so could be a param name
                # CAREFULL! Could be a negitive number or some user defined string starting with a dash.
                if len(raw_arg) > 2 and raw_arg[:2] == "--":
                    # Highly likley to be a parameter and definately not a short name
                    if raw_arg[2:] in self.__parameter_lookup_by_name:
                        param_name = raw_arg[2:]
                        if isinstance(self.__parameter_lookup_by_name[param_name], self.Flag):
                            named_argument_lookup[param_name] = ""
                        else:
                            if arg_index + 1 == number_of_raw_args:
                                raise IndexError("Final argument was parameter name that required a value.")
                            named_argument_lookup[param_name] = self.__raw_arguments[arg_index + 1]
                else:
                    # Could still be a short name
                    if raw_arg[1:] in self.__parameter_lookup_by_short_name:
                        param_short_name = raw_arg[1:]
                        param = self.__parameter_lookup_by_short_name[param_short_name]
                        if isinstance(param, self.Flag):
                            named_argument_lookup[param.name] = ""
                        else:
                            if arg_index + 1 == number_of_raw_args:
                                raise IndexError("Final argument was parameter name that required a value.")
                            named_argument_lookup[param.name] = self.__raw_arguments[arg_index + 1]

        for param in self.__parameters:
            param.set_from_args(named_argument_lookup)
        positional_arg_index = 0
        for param in self.__parameters:
            if isinstance(param, self.PositionalParam):
                if not param.is_explicitly_set:
                    if len(self.__raw_arguments) <= positional_arg_index:
                        raise IndexError("Too few arguments provided for the number of positional parameters.")
                    param.set_from_positional_arg(self.__raw_arguments[positional_arg_index])
                    positional_arg_index += 1
            else:
                if param.name not in self.__parameters.special_param_names:
                    break # No more positional parameters
        
        if not self.__parameters.help_param.value:
            # If help flag has been set, skip validation as target function won't actually be called.
            for param in self.__parameters:
                param.validate()
        self.__arguments_have_been_parsed = True

    @staticmethod
    def __run(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            if not self.__arguments_have_been_parsed:
                self.parse_arguments() # Automatically parse command line arguments

            is_root_process = True
            try:
                if not self.use_MPI or get_mpi_rank() == 0:
                    # Either the first MPI process or MPI isn't active
                    return func(self, *args, **kwargs)
                else:
                    if not _settings_object.mpi_avalible:
                        raise ImportError("MPI required but not avalible.")

                    # MPI active and not the first process
                    is_root_process = False
                    return func(self, *args, **kwargs)
                    
            except Exception as e:
                if is_root_process or self.MPI_print_non_root_process_errors:
                    has_message = str(e) != ""
                    Console.print_error(f"Execution encountered an error{(':' if has_message else ' (no details avalible).') if _settings_object.debug or _settings_object.verbose else '.'}")
                    Console.print_debug("Traceback (most recent call last):\n" + "".join(traceback.format_tb(e.__traceback__)) + type(e).__name__ + (f": {str(e)}" if has_message else ""))
                    if has_message and not _settings_object.debug:
                        Console.print_error(str(e))
                    Console.print_info("Terminating.")

        return inner

    @__run
    def run(self, func):
        if self.__parameters.help_param.value:
            print(self.help_string)
            sys.exit()
        if self.__parameters.debug_param.value:
            _settings_object.enable_debug()
        if self.__parameters.verbose_param.value:
            _settings_object.enable_verbose()
        kwargs = self.__parameters.get_keyword_arguments()
        return func(**kwargs)

    @__run
    def run_with_async(self, func):
        if self.__parameters.help_param.value:
            print(self.help_string)
            sys.exit()
        if self.__parameters.debug_param.value:
            _settings_object.enable_debug()
        if self.__parameters.verbose_param.value:
            _settings_object.enable_verbose()
        kwargs = self.__parameters.get_keyword_arguments()
        return start_main_async(func, **kwargs)

#    @staticmethod
#    def passthrough_converter(value: str) -> str:
#        return value
#
#    @staticmethod
#    def bool_converter(value: str) -> bool:
#        return value.lower() in ("true", "t", "yes", "y", "1", "accept", "allow", "confirm")
#
#    @staticmethod
#    def filter_converter(value: str) -> Tuple[bool, ...]:
#        return tuple(ScriptWrapper.bool_converter(element) for element in value.lower())
#
#    #@staticmethod
#    #def reverse_flag_converter(value: bool) -> bool:
#    #    return not value
#
#    @staticmethod
#    def make_list_converter(seperator = ",", item_converters: Union[Sequence[Callable[[str], Any]], Callable[[str], Any], None] = None):
#        if item_converters is None:
#            item_converters = ScriptWrapper.passthrough_converter
#        def list_converter(value: str) -> Any:
#            if not isinstance(item_converters, Sequence):
#                return [item_converters(item) if item != "" or item_converters == ScriptWrapper.passthrough_converter or item_converters == str else None for item in value.split(seperator)]
#            else:
#                converters_for_use: List[Callable[[str], Any]] = list(item_converters)
#                strings = value.split(seperator)
#                while len(converters_for_use) < len(strings):
#                    converters_for_use.append(ScriptWrapper.passthrough_converter)
#                return [converters_for_use[i](strings[i]) if strings[i] != "" or converters_for_use[i] == ScriptWrapper.passthrough_converter or converters_for_use == str else None for i in range(len(strings))]
#        return list_converter
    passthrough_converter = ScriptWrapper_passthrough_converter
    bool_converter = ScriptWrapper_bool_converter
    filter_converter = ScriptWrapper_filter_converter
    #reverse_flag_converter = ScriptWrapper_reverse_flag_converter
    make_list_converter = ScriptWrapper_make_list_converter



'''
class ScriptWrapper(object):
    """
    Singelton that handles command argument parsing for the currently running program.
    Constructor Arguments:
              str filename                 --> The name of the entrypoint file.
              str author                   --> The name(s) of the file author(s).
              str version_string           --> String indicating the current version of the file.
              str edit_date                --> String indicating the date of the last edit.
              str description              --> A description of the function of the script.
        list[str] dependancies             --> A list of dependancies of the script.
        list[str] usage_paramiter_examples --> A list of strings demonstrating example paramiter
                                                   lists (exclude the call to the script).
             list positional_params        --> List of paramiter information for paramiters that must
                                                   appear at the start of the argument list in order
                                                   without a flag identifier (each paramiter is a list
                                                   with fields as below).
                                                   [
                                                    name, description, conversion func (nullable)
                                                   ]
             list params                   --> List of paramiter information (each paramiter is a list
                                                   with fields as below).
                                                   [
                                                    name, short name (nullable), description,
                                                    required?, flag?, conversion func (nullable),
                                                    default value, mutually exclusive flags (list[str])
                                                   ]
    Public Methods:
               run
        static passthrough_converter
        static bool_converter
        static make_list_converter
    """

    #TODO: set this up to enforce a singleton
    #__initialised = False
    #__instance = None
    #
    #def __new__(cls, *args, **kwargs):
    #    if ScriptWrapper.__initialised:
    #        #raise RuntimeError("A running program may only define one ScriptWrapper instance.")
    #        return ScriptWrapper.__instance
    #    else:
    #        ScriptWrapper.__initialised = True
    #        ScriptWrapper.__instance = super(ScriptWrapper, cls).__new__(cls)
    #        return ScriptWrapper.__instance

    def __init__(self, filename: str, author: str, version_string: str, edit_date: str,
                       description: str,
                       dependancies: list,
                       usage_paramiter_examples: list,
                       positional_params: list = [], params: list = []):
        self.raw_case_args = sys.argv[1:]
        self.lowercase_args = [arg.lower() for arg in sys.argv[1:]]
        if "-d" in self.lowercase_args or "--debug" in self.lowercase_args:
            _settings_object.enable_debug()
        if "-v" in self.lowercase_args or "--verbose" in self.lowercase_args:
            _settings_object.enable_verbose()

        rendered_dependancy_strings = "\n".join([f"    {dependancy}" for dependancy in dependancies])

        rendered_usage_examples = "\n".join([f"    python {filename} {param_list}" for param_list in usage_paramiter_examples])

        self.n_positionals = len(positional_params)
        
        self.argument_spec = {}
        self.argument_spec["help"] = { "short_name": "h", "description": "Display this docstring.", "is_required": False, "is_positional": False, "is_flag": True, "mutually_exclusive_flags": [], "converter_function": ScriptWrapper.passthrough_converter, "default_value": None  }
        self.argument_spec["debug"] = { "short_name": "d", "description": "Display debug infomation.", "is_required": False, "is_positional": False, "is_flag": True, "mutually_exclusive_flags": [], "converter_function": ScriptWrapper.passthrough_converter, "default_value": None  }
        self.argument_spec["verbose"] = { "short_name": "v", "description": "Display progression infomation.", "is_required": False, "is_positional": False, "is_flag": True, "mutually_exclusive_flags": [], "converter_function": ScriptWrapper.passthrough_converter, "default_value": None  }
        for param in positional_params:
            self.argument_spec[param[0]] = { "short_name": None, "description": param[1], "is_required": True, "is_positional": True, "is_flag": False, "converter_function": ScriptWrapper.passthrough_converter if param[2] is None else param[2], "default_value": None }
        for param in params:
            self.argument_spec[param[0]] = { "short_name": param[1], "description": param[2], "is_required": param[3], "is_positional": False, "is_flag": param[4], "mutually_exclusive_flags": [] if len(param) <= 7 else param[7], "converter_function": ScriptWrapper.passthrough_converter if param[5] is None else param[5], "default_value": param[6] if param[6] is not None else ((ScriptWrapper.passthrough_converter if param[5] is None else param[5])(False) if param[4] else None) }

        name_spacing = max([len(name) for name in self.argument_spec])
        indent_spacing = name_spacing + 26

        rendered_argument_spec = "".join(["\n\n    ({}) {}{}{} || {} --> {}".format((" p" if self.argument_spec[name]["is_positional"] else (" r" if self.argument_spec[name]["is_required"] else ("f " if self.argument_spec[name]["is_flag"] else "f+"))), "  " if self.argument_spec[name]["is_positional"] else "--", name, (name_spacing - len(name)) * " ", ("  " if self.argument_spec[name]["short_name"] is None else "-{}".format(self.argument_spec[name]["short_name"])), self.argument_spec[name]["description"].replace("\n", "\n" + (indent_spacing * " "))) for name in self.argument_spec])

        self.help_string = f"""
File: {filename}
Author: {author}
Vesion: {version_string}
Date:   {edit_date}
{description}
Commandline arguments & flags ( p = required positional argument,
                                r = required paramiter,
                               f  = optional flag,
                               f+ = optional flag with a required argument):{rendered_argument_spec}
Dependancies:
{rendered_dependancy_strings}
Example Usage:
{rendered_usage_examples}
"""

        if "-h" in self.lowercase_args or "--help" in self.lowercase_args:
            print(self.help_string)
            sys.exit()

        self.params = {}
        for name in self.argument_spec:
            self.params[name] = self.argument_spec[name]["default_value"] 

        param_check_strings = []
        param_name_reverse_lookup = {}
        for name in self.argument_spec:
            param_check_strings.append(f"--{name}")
            if self.argument_spec[name]["short_name"] is not None:
                param_check_strings.append("-{}".format(self.argument_spec[name]["short_name"]))
                param_name_reverse_lookup[self.argument_spec[name]["short_name"]] = name

        arg_index = 0
        while arg_index < len(self.lowercase_args):
            if self.lowercase_args[arg_index] in param_check_strings:
                param_name = None
                if self.lowercase_args[arg_index][1] == "-":
                    param_name = self.lowercase_args[arg_index][2:]
                else:
                    param_name = param_name_reverse_lookup[self.lowercase_args[arg_index][1:]]

                if self.argument_spec[param_name]["is_flag"]:
                    self.params[param_name] = self.argument_spec[param_name]["converter_function"](True)
                    for flag_name in self.argument_spec[param_name]["mutually_exclusive_flags"]:
                        self.params[flag_name] = self.argument_spec[param_name]["converter_function"](False)
                else:
                    self.params[param_name] = self.argument_spec[param_name]["converter_function"](self.raw_case_args[arg_index + 1])
                    arg_index += 1

            arg_index += 1

        for i in range(self.n_positionals):
            self.params[positional_params[i][0]] = self.argument_spec[positional_params[i][0]]["converter_function"](self.raw_case_args[i])

        self.use_MPI = False
        self.MPI_print_non_root_process_errors = False

    def __run(func):
        def inner(self, *args, **kwargs):
            is_root_process = True
            try:
                if not self.use_MPI or get_mpi_rank() == 0:
                    # Either the first MPI process or MPI isn't active
                    return func(self, *args, **kwargs)
                else:
                    if not _settings_object.mpi_avalible:
                        raise ImportError("MPI required but not avalible.")

                    # MPI active and not the first process
                    is_root_process = False
                    return func(self, *args, **kwargs)
                    
            except Exception as e:
                if is_root_process or self.MPI_print_non_root_process_errors:
                    has_message = e.__str__() != ""
                    Console.print_error(f"Execution encountered an error{(':' if has_message else ' (no details avalible).') if _settings_object.debug or _settings_object.verbose else '.'}")
                    Console.print_debug("Traceback (most recent call last):\n" + "".join(traceback.format_tb(e.__traceback__)) + type(e).__name__ + (f": {e.__str__()}" if has_message else ""))
                    if has_message and not _settings_object.debug:
                        Console.print_error(e.__str__())
                    Console.print_info("Terminating.")

        return inner

    @__run
    def run(self, func):
        kwargs = { param.replace("-", "_"): self.params[param] for param in self.params if param not in ("help", "debug", "verbose") }
        return func(**kwargs)

    @__run
    def run_with_async(self, func):
        kwargs = { param.replace("-", "_"): self.params[param] for param in self.params if param not in ("help", "debug", "verbose") }
        return start_main_async(func, **kwargs)

    @staticmethod
    def passthrough_converter(value: str) -> str:
        return value

    @staticmethod
    def bool_converter(value: str) -> bool:
        return value in ("true", "t", "yes", "y", "accept", "1")

    @staticmethod
    def reverse_flag_converter(value: bool) -> bool:
        return not value

    @staticmethod
    def make_list_converter(seperator = ",", item_converters: list = None):
        if item_converters is None: item_converters = ScriptWrapper.passthrough_converter
        def list_converter(value: str) -> bool:
            if not isinstance(item_converters, (list, tuple)):
                return [item_converters(item) if item != "" or item_converters == ScriptWrapper.passthrough_converter or item_converters == str else None for item in value.split(seperator)]
            else:
                strings = value.split(seperator)
                while len(item_converters) < len(strings):
                    item_converters.append(ScriptWrapper.passthrough_converter)
                return [item_converters[i](strings[i]) if strings[i] != "" or item_converters[i] == ScriptWrapper.passthrough_converter or item_converters == str else None for i in range(len(strings))]
        return list_converter
'''
