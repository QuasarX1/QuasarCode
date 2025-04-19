from decimal import Decimal
import numpy as np
#from numpy.typing import NDArray
from typing import Union, Generic, TypeVar, Tuple, List, Dict, Callable, Any, cast
from unyt import unyt_quantity, unyt_array

from ._cast import Cast, non_nullable_cast, nullable_cast, NestedCast

# Typeparam definition
T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

# Some common type casts

# Non-nullables

cast_bool    : Cast[bool]    = non_nullable_cast(bool)
cast_int     : Cast[int]     = non_nullable_cast(int)
cast_float   : Cast[float]   = non_nullable_cast(float)
cast_Decimal : Cast[Decimal] = non_nullable_cast(Decimal)
cast_str     : Cast[str]     = non_nullable_cast(str)

cast_list  : Cast[List[Any]]  = non_nullable_cast(list)
cast_tuple : Cast[Tuple[Any, ...]] = non_nullable_cast(tuple)

def cast_typed_list(*type_casts: Cast[T]) -> NestedCast[List[T]]:
    return NestedCast[List[T]](cast_list, *type_casts, nullable = False)

def cast_typed_tuple(*type_casts: Cast[T]) -> NestedCast[Tuple[T]]:
    return NestedCast[Tuple[T]](cast_tuple, *type_casts, nullable = False)

def cast_dict(cast_keys: Union[Cast[K], None] = None, cast_values: Union[Cast[V], None] = None) -> Cast[Dict[K, V]]:
    if cast_keys is None:
        cast_keys = Cast.passthrough()
    if cast_values is None:
        cast_values = Cast.passthrough()
    def cast_dict_obj(value: Dict[Any, Any]) -> Dict[K, V]:
        return { cast(K, cast_keys(key)): cast(V, cast_values(value[key])) for key in value }
    return non_nullable_cast(cast_dict_obj)

def cast_ndarray(*args: Any, **kwargs: Any) -> Cast[np.ndarray]:
    """
    *args and **kwargs for numpy.array() may be passed
    """
    return non_nullable_cast(np.array, *args, **kwargs)

cast_ndarray_bool     : Cast[np.ndarray] = cast_ndarray(dtype = bool)
cast_ndarray_int      : Cast[np.ndarray] = cast_ndarray(dtype = int)
cast_ndarray_int8     : Cast[np.ndarray] = cast_ndarray(dtype = np.int8)
cast_ndarray_int16    : Cast[np.ndarray] = cast_ndarray(dtype = np.int16)
cast_ndarray_int32    : Cast[np.ndarray] = cast_ndarray(dtype = np.int32)
cast_ndarray_int64    : Cast[np.ndarray] = cast_ndarray(dtype = np.int64)
#cast_ndarray_int128   : Cast[np.ndarray] = cast_ndarray(dtype = np.int128)
#cast_ndarray_int256   : Cast[np.ndarray] = cast_ndarray(dtype = np.int256)
cast_ndarray_float    : Cast[np.ndarray] = cast_ndarray(dtype = float)
cast_ndarray_float16  : Cast[np.ndarray] = cast_ndarray(dtype = np.float16)
cast_ndarray_float32  : Cast[np.ndarray] = cast_ndarray(dtype = np.float32)
cast_ndarray_float64  : Cast[np.ndarray] = cast_ndarray(dtype = np.float64)
#cast_ndarray_float80  : Cast[np.ndarray] = cast_ndarray(dtype = np.float80)
#cast_ndarray_float96  : Cast[np.ndarray] = cast_ndarray(dtype = np.float96)
#cast_ndarray_float128 : Cast[np.ndarray] = cast_ndarray(dtype = np.float128)
#cast_ndarray_float256 : Cast[np.ndarray] = cast_ndarray(dtype = np.float256)
cast_ndarray_str      : Cast[np.ndarray] = cast_ndarray(dtype = str)

def cast_unyt_quantity(unit: str, *args: Any, **kwargs: Any) -> Cast[unyt_quantity]:
    """
    *args and **kwargs for unyt.unyt_quantity() may be passed
    (though will only be used if the target value is not already a unyt_quantity object!)
    """
    def inner(value: Any, _unit: str, *args: Any, **kwargs: Any):
        if isinstance(value, unyt_quantity):
            return value.to(_unit)
        elif isinstance(value, unyt_array):
            return unyt_quantity(value.to(_unit), _unit, *args, **kwargs)
        else:
            return unyt_quantity(value, _unit, *args, **kwargs)
    return non_nullable_cast(inner, unit, *args, **kwargs)

cast_unyt_quantity_mass_si           : Cast[unyt_quantity] = cast_unyt_quantity(unit = "kg",      dtype = np.float64)
cast_unyt_quantity_mass_imperial     : Cast[unyt_quantity] = cast_unyt_quantity(unit = "lb",      dtype = np.float64)
cast_unyt_quantity_mass_cgs          : Cast[unyt_quantity] = cast_unyt_quantity(unit = "g",       dtype = np.float64)
cast_unyt_quantity_mass_solar        : Cast[unyt_quantity] = cast_unyt_quantity(unit = "Msun",    dtype = np.float64)
cast_unyt_quantity_time_milliseconds : Cast[unyt_quantity] = cast_unyt_quantity(unit = "ms",      dtype = np.float64)
cast_unyt_quantity_time_seconds      : Cast[unyt_quantity] = cast_unyt_quantity(unit = "s",       dtype = np.float64)
cast_unyt_quantity_time_minutes      : Cast[unyt_quantity] = cast_unyt_quantity(unit = "min",     dtype = np.float64)
cast_unyt_quantity_time_hours        : Cast[unyt_quantity] = cast_unyt_quantity(unit = "hr",      dtype = np.float64)
cast_unyt_quantity_time_days         : Cast[unyt_quantity] = cast_unyt_quantity(unit = "day",     dtype = np.float64)
cast_unyt_quantity_time_years        : Cast[unyt_quantity] = cast_unyt_quantity(unit = "yr",      dtype = np.float64)
cast_unyt_quantity_time_Gyrs         : Cast[unyt_quantity] = cast_unyt_quantity(unit = "Gyr",     dtype = np.float64)
cast_unyt_quantity_length_si         : Cast[unyt_quantity] = cast_unyt_quantity(unit = "m",       dtype = np.float64)
cast_unyt_quantity_length_imperial   : Cast[unyt_quantity] = cast_unyt_quantity(unit = "ft",      dtype = np.float64)
cast_unyt_quantity_length_cgs        : Cast[unyt_quantity] = cast_unyt_quantity(unit = "cm",      dtype = np.float64)
cast_unyt_quantity_length_solar      : Cast[unyt_quantity] = cast_unyt_quantity(unit = "Rsun",    dtype = np.float64)
cast_unyt_quantity_length_pc         : Cast[unyt_quantity] = cast_unyt_quantity(unit = "pc",      dtype = np.float64)
cast_unyt_quantity_length_kpc        : Cast[unyt_quantity] = cast_unyt_quantity(unit = "kpc",     dtype = np.float64)
cast_unyt_quantity_length_Mpc        : Cast[unyt_quantity] = cast_unyt_quantity(unit = "Mpc",     dtype = np.float64)
cast_unyt_quantity_speed_si          : Cast[unyt_quantity] = cast_unyt_quantity(unit = "m/s",     dtype = np.float64)
cast_unyt_quantity_speed_imperial    : Cast[unyt_quantity] = cast_unyt_quantity(unit = "ft/s",    dtype = np.float64)
cast_unyt_quantity_speed_cgs         : Cast[unyt_quantity] = cast_unyt_quantity(unit = "cm/s",    dtype = np.float64)
cast_unyt_quantity_speed_kms         : Cast[unyt_quantity] = cast_unyt_quantity(unit = "km/s",    dtype = np.float64)
cast_unyt_quantity_speed_Mpc_per_Gyr : Cast[unyt_quantity] = cast_unyt_quantity(unit = "Mpc/Gyr", dtype = np.float64)
cast_unyt_quantity_force_si          : Cast[unyt_quantity] = cast_unyt_quantity(unit = "N",       dtype = np.float64)
cast_unyt_quantity_force_imperial    : Cast[unyt_quantity] = cast_unyt_quantity(unit = "lbf",     dtype = np.float64)
cast_unyt_quantity_force_cgs         : Cast[unyt_quantity] = cast_unyt_quantity(unit = "dyn",     dtype = np.float64)
cast_unyt_quantity_energy_si         : Cast[unyt_quantity] = cast_unyt_quantity(unit = "J",       dtype = np.float64)
cast_unyt_quantity_energy_imperial   : Cast[unyt_quantity] = cast_unyt_quantity(unit = "BTU",     dtype = np.float64)
cast_unyt_quantity_energy_cgs        : Cast[unyt_quantity] = cast_unyt_quantity(unit = "erg",     dtype = np.float64)
cast_unyt_quantity_energy_eV         : Cast[unyt_quantity] = cast_unyt_quantity(unit = "eV",      dtype = np.float64)
cast_unyt_quantity_energy_KeV        : Cast[unyt_quantity] = cast_unyt_quantity(unit = "KeV",     dtype = np.float64)
cast_unyt_quantity_energy_GeV        : Cast[unyt_quantity] = cast_unyt_quantity(unit = "GeV",     dtype = np.float64)
cast_unyt_quantity_energy_TeV        : Cast[unyt_quantity] = cast_unyt_quantity(unit = "TeV",     dtype = np.float64)
cast_unyt_quantity_power_si          : Cast[unyt_quantity] = cast_unyt_quantity(unit = "W",       dtype = np.float64)
cast_unyt_quantity_power_imperial    : Cast[unyt_quantity] = cast_unyt_quantity(unit = "hp",      dtype = np.float64)
cast_unyt_quantity_power_cgs         : Cast[unyt_quantity] = cast_unyt_quantity(unit = "erg/s",   dtype = np.float64)
cast_unyt_quantity_power_solar       : Cast[unyt_quantity] = cast_unyt_quantity(unit = "Lsun",    dtype = np.float64)

def cast_unyt_array(unit: str, *args: Any, **kwargs: Any) -> Cast[unyt_array]:
    """
    *args and **kwargs for unyt.unyt_array() may be passed
    (though will only be used if the target value is not already a unyt_array object!)
    """
    def inner(value: Any, _unit: str, *args: Any, **kwargs: Any):
        if isinstance(value, unyt_quantity):
            return unyt_array(value.to(_unit), _unit, *args, **kwargs)
        elif isinstance(value, unyt_array):
            return value.to(_unit)
        else:
            return unyt_array(value, _unit, *args, **kwargs)
    return non_nullable_cast(inner, unit, *args, **kwargs)

cast_unyt_array_mass_si           : Cast[unyt_array] = cast_unyt_array(unit = "kg",      dtype = np.float64)
cast_unyt_array_mass_imperial     : Cast[unyt_array] = cast_unyt_array(unit = "lb",      dtype = np.float64)
cast_unyt_array_mass_cgs          : Cast[unyt_array] = cast_unyt_array(unit = "g",       dtype = np.float64)
cast_unyt_array_mass_solar        : Cast[unyt_array] = cast_unyt_array(unit = "Msun",    dtype = np.float64)
cast_unyt_array_time_milliseconds : Cast[unyt_array] = cast_unyt_array(unit = "ms",      dtype = np.float64)
cast_unyt_array_time_seconds      : Cast[unyt_array] = cast_unyt_array(unit = "s",       dtype = np.float64)
cast_unyt_array_time_minutes      : Cast[unyt_array] = cast_unyt_array(unit = "min",     dtype = np.float64)
cast_unyt_array_time_hours        : Cast[unyt_array] = cast_unyt_array(unit = "hr",      dtype = np.float64)
cast_unyt_array_time_days         : Cast[unyt_array] = cast_unyt_array(unit = "day",     dtype = np.float64)
cast_unyt_array_time_years        : Cast[unyt_array] = cast_unyt_array(unit = "yr",      dtype = np.float64)
cast_unyt_array_time_Gyrs         : Cast[unyt_array] = cast_unyt_array(unit = "Gyr",     dtype = np.float64)
cast_unyt_array_length_si         : Cast[unyt_array] = cast_unyt_array(unit = "m",       dtype = np.float64)
cast_unyt_array_length_imperial   : Cast[unyt_array] = cast_unyt_array(unit = "ft",      dtype = np.float64)
cast_unyt_array_length_cgs        : Cast[unyt_array] = cast_unyt_array(unit = "cm",      dtype = np.float64)
cast_unyt_array_length_solar      : Cast[unyt_array] = cast_unyt_array(unit = "Rsun",    dtype = np.float64)
cast_unyt_array_length_pc         : Cast[unyt_array] = cast_unyt_array(unit = "pc",      dtype = np.float64)
cast_unyt_array_length_kpc        : Cast[unyt_array] = cast_unyt_array(unit = "kpc",     dtype = np.float64)
cast_unyt_array_length_Mpc        : Cast[unyt_array] = cast_unyt_array(unit = "Mpc",     dtype = np.float64)
cast_unyt_array_speed_si          : Cast[unyt_array] = cast_unyt_array(unit = "m/s",     dtype = np.float64)
cast_unyt_array_speed_imperial    : Cast[unyt_array] = cast_unyt_array(unit = "ft/s",    dtype = np.float64)
cast_unyt_array_speed_cgs         : Cast[unyt_array] = cast_unyt_array(unit = "cm/s",    dtype = np.float64)
cast_unyt_array_speed_kms         : Cast[unyt_array] = cast_unyt_array(unit = "km/s",    dtype = np.float64)
cast_unyt_array_speed_Mpc_per_Gyr : Cast[unyt_array] = cast_unyt_array(unit = "Mpc/Gyr", dtype = np.float64)
cast_unyt_array_force_si          : Cast[unyt_array] = cast_unyt_array(unit = "N",       dtype = np.float64)
cast_unyt_array_force_imperial    : Cast[unyt_array] = cast_unyt_array(unit = "lbf",     dtype = np.float64)
cast_unyt_array_force_cgs         : Cast[unyt_array] = cast_unyt_array(unit = "dyn",     dtype = np.float64)
cast_unyt_array_energy_si         : Cast[unyt_array] = cast_unyt_array(unit = "J",       dtype = np.float64)
cast_unyt_array_energy_imperial   : Cast[unyt_array] = cast_unyt_array(unit = "BTU",     dtype = np.float64)
cast_unyt_array_energy_cgs        : Cast[unyt_array] = cast_unyt_array(unit = "erg",     dtype = np.float64)
cast_unyt_array_energy_eV         : Cast[unyt_array] = cast_unyt_array(unit = "eV",      dtype = np.float64)
cast_unyt_array_energy_KeV        : Cast[unyt_array] = cast_unyt_array(unit = "KeV",     dtype = np.float64)
cast_unyt_array_energy_GeV        : Cast[unyt_array] = cast_unyt_array(unit = "GeV",     dtype = np.float64)
cast_unyt_array_energy_TeV        : Cast[unyt_array] = cast_unyt_array(unit = "TeV",     dtype = np.float64)
cast_unyt_array_power_si          : Cast[unyt_array] = cast_unyt_array(unit = "W",       dtype = np.float64)
cast_unyt_array_power_imperial    : Cast[unyt_array] = cast_unyt_array(unit = "hp",      dtype = np.float64)
cast_unyt_array_power_cgs         : Cast[unyt_array] = cast_unyt_array(unit = "erg/s",   dtype = np.float64)
cast_unyt_array_power_solar       : Cast[unyt_array] = cast_unyt_array(unit = "Lsun",    dtype = np.float64)

# Nullables

cast_nullable_bool    : Cast[bool]    = nullable_cast(bool)
cast_nullable_int     : Cast[int]     = nullable_cast(int)
cast_nullable_float   : Cast[float]   = nullable_cast(float)
cast_nullable_Decimal : Cast[Decimal] = nullable_cast(Decimal)
cast_nullable_str     : Cast[str]     = nullable_cast(str)

cast_nullable_list  : Cast[List[Any]]  = nullable_cast(list)
cast_nullable_tuple : Cast[Tuple[Any, ...]] = nullable_cast(tuple)

def cast_nullable_typed_list(*type_casts: Cast[T]) -> NestedCast[List[T]]:
    return NestedCast[List[T]](cast_list, *type_casts, nullable = True)

def cast_nullable_typed_tuple(*type_casts: Cast[T]) -> NestedCast[Tuple[T]]:
    return NestedCast[Tuple[T]](cast_tuple, *type_casts, nullable = True)

def cast_nullable_dict(cast_keys: Union[Cast[K], None] = None, cast_values: Union[Cast[V], None] = None) -> Cast[Dict[K, V]]:
    if cast_keys is None:
        cast_keys = Cast.passthrough()
    if cast_values is None:
        cast_values = Cast.passthrough()
    def cast_nullable_dict_obj(value: Dict[Any, Any]) -> Dict[K, V]:
        return { cast(K, cast_keys(key)): cast(V, cast_values(value[key])) for key in value }
    return nullable_cast(cast_nullable_dict_obj)

def cast_nullable_ndarray(*args: Any, **kwargs: Any) -> Cast[np.ndarray]:
    """
    *args and **kwargs for numpy.array() may be passed
    """
    return nullable_cast(np.array, *args, **kwargs)

cast_nullable_ndarray_bool     : Cast[np.ndarray] = cast_nullable_ndarray(dtype = bool)
cast_nullable_ndarray_int      : Cast[np.ndarray] = cast_nullable_ndarray(dtype = int)
cast_nullable_ndarray_int8     : Cast[np.ndarray] = cast_nullable_ndarray(dtype = np.int8)
cast_nullable_ndarray_int16    : Cast[np.ndarray] = cast_nullable_ndarray(dtype = np.int16)
cast_nullable_ndarray_int32    : Cast[np.ndarray] = cast_nullable_ndarray(dtype = np.int32)
cast_nullable_ndarray_int64    : Cast[np.ndarray] = cast_nullable_ndarray(dtype = np.int64)
#cast_nullable_ndarray_int128   : Cast[np.ndarray] = cast_nullable_ndarray(dtype = np.int128)
#cast_nullable_ndarray_int256   : Cast[np.ndarray] = cast_nullable_ndarray(dtype = np.int256)
cast_nullable_ndarray_float    : Cast[np.ndarray] = cast_nullable_ndarray(dtype = float)
cast_nullable_ndarray_float16  : Cast[np.ndarray] = cast_nullable_ndarray(dtype = np.float16)
cast_nullable_ndarray_float32  : Cast[np.ndarray] = cast_nullable_ndarray(dtype = np.float32)
cast_nullable_ndarray_float64  : Cast[np.ndarray] = cast_nullable_ndarray(dtype = np.float64)
#cast_nullable_ndarray_float80  : Cast[np.ndarray] = cast_nullable_ndarray(dtype = np.float80)
#cast_nullable_ndarray_float96  : Cast[np.ndarray] = cast_nullable_ndarray(dtype = np.float96)
#cast_nullable_ndarray_float128 : Cast[np.ndarray] = cast_nullable_ndarray(dtype = np.float128)
#cast_nullable_ndarray_float256 : Cast[np.ndarray] = cast_nullable_ndarray(dtype = np.float256)
cast_nullable_ndarray_str      : Cast[np.ndarray] = cast_nullable_ndarray(dtype = str)

def cast_nullable_unyt_quantity(unit: str, *args: Any, **kwargs: Any) -> Cast[unyt_quantity]:
    """
    *args and **kwargs for unyt.unyt_quantity() may be passed
    (though will only be used if the target value is not already a unyt_quantity object!)
    """
    def inner(value: Any, _unit: str, *args: Any, **kwargs: Any):
        if isinstance(value, unyt_quantity):
            return value.to(_unit)
        elif isinstance(value, unyt_array):
            return unyt_quantity(value.to(_unit), _unit, *args, **kwargs)
        else:
            return unyt_quantity(value, _unit, *args, **kwargs)
    return nullable_cast(inner, unit, *args, **kwargs)

cast_nullable_unyt_quantity_mass_si           : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "kg",      dtype = np.float64)
cast_nullable_unyt_quantity_mass_imperial     : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "lb",      dtype = np.float64)
cast_nullable_unyt_quantity_mass_cgs          : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "g",       dtype = np.float64)
cast_nullable_unyt_quantity_mass_solar        : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "Msun",    dtype = np.float64)
cast_nullable_unyt_quantity_time_milliseconds : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "ms",      dtype = np.float64)
cast_nullable_unyt_quantity_time_seconds      : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "s",       dtype = np.float64)
cast_nullable_unyt_quantity_time_minutes      : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "min",     dtype = np.float64)
cast_nullable_unyt_quantity_time_hours        : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "hr",      dtype = np.float64)
cast_nullable_unyt_quantity_time_days         : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "day",     dtype = np.float64)
cast_nullable_unyt_quantity_time_years        : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "yr",      dtype = np.float64)
cast_nullable_unyt_quantity_time_Gyrs         : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "Gyr",     dtype = np.float64)
cast_nullable_unyt_quantity_length_si         : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "m",       dtype = np.float64)
cast_nullable_unyt_quantity_length_imperial   : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "ft",      dtype = np.float64)
cast_nullable_unyt_quantity_length_cgs        : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "cm",      dtype = np.float64)
cast_nullable_unyt_quantity_length_solar      : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "Rsun",    dtype = np.float64)
cast_nullable_unyt_quantity_length_pc         : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "pc",      dtype = np.float64)
cast_nullable_unyt_quantity_length_kpc        : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "kpc",     dtype = np.float64)
cast_nullable_unyt_quantity_length_Mpc        : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "Mpc",     dtype = np.float64)
cast_nullable_unyt_quantity_speed_si          : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "m/s",     dtype = np.float64)
cast_nullable_unyt_quantity_speed_imperial    : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "ft/s",    dtype = np.float64)
cast_nullable_unyt_quantity_speed_cgs         : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "cm/s",    dtype = np.float64)
cast_nullable_unyt_quantity_speed_kms         : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "km/s",    dtype = np.float64)
cast_nullable_unyt_quantity_speed_Mpc_per_Gyr : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "Mpc/Gyr", dtype = np.float64)
cast_nullable_unyt_quantity_force_si          : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "N",       dtype = np.float64)
cast_nullable_unyt_quantity_force_imperial    : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "lbf",     dtype = np.float64)
cast_nullable_unyt_quantity_force_cgs         : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "dyn",     dtype = np.float64)
cast_nullable_unyt_quantity_energy_si         : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "J",       dtype = np.float64)
cast_nullable_unyt_quantity_energy_imperial   : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "BTU",     dtype = np.float64)
cast_nullable_unyt_quantity_energy_cgs        : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "erg",     dtype = np.float64)
cast_nullable_unyt_quantity_energy_eV         : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "eV",      dtype = np.float64)
cast_nullable_unyt_quantity_energy_KeV        : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "KeV",     dtype = np.float64)
cast_nullable_unyt_quantity_energy_GeV        : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "GeV",     dtype = np.float64)
cast_nullable_unyt_quantity_energy_TeV        : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "TeV",     dtype = np.float64)
cast_nullable_unyt_quantity_power_si          : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "W",       dtype = np.float64)
cast_nullable_unyt_quantity_power_imperial    : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "hp",      dtype = np.float64)
cast_nullable_unyt_quantity_power_cgs         : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "erg/s",   dtype = np.float64)
cast_nullable_unyt_quantity_power_solar       : Cast[unyt_quantity] = cast_nullable_unyt_quantity(unit = "Lsun",    dtype = np.float64)

def cast_nullable_unyt_array(unit: str, *args: Any, **kwargs: Any) -> Cast[unyt_array]:
    """
    *args and **kwargs for unyt.unyt_array() may be passed
    (though will only be used if the target value is not already a unyt_array object!)
    """
    def inner(value: Any, _unit: str, *args: Any, **kwargs: Any):
        if isinstance(value, unyt_quantity):
            return unyt_array(value.to(_unit), _unit, *args, **kwargs)
        elif isinstance(value, unyt_array):
            return value.to(_unit)
        else:
            return unyt_array(value, _unit, *args, **kwargs)
    return nullable_cast(inner, unit, *args, **kwargs)

cast_nullable_unyt_array_mass_si           : Cast[unyt_array] = cast_nullable_unyt_array(unit = "kg",      dtype = np.float64)
cast_nullable_unyt_array_mass_imperial     : Cast[unyt_array] = cast_nullable_unyt_array(unit = "lb",      dtype = np.float64)
cast_nullable_unyt_array_mass_cgs          : Cast[unyt_array] = cast_nullable_unyt_array(unit = "g",       dtype = np.float64)
cast_nullable_unyt_array_mass_solar        : Cast[unyt_array] = cast_nullable_unyt_array(unit = "Msun",    dtype = np.float64)
cast_nullable_unyt_array_time_milliseconds : Cast[unyt_array] = cast_nullable_unyt_array(unit = "ms",      dtype = np.float64)
cast_nullable_unyt_array_time_seconds      : Cast[unyt_array] = cast_nullable_unyt_array(unit = "s",       dtype = np.float64)
cast_nullable_unyt_array_time_minutes      : Cast[unyt_array] = cast_nullable_unyt_array(unit = "min",     dtype = np.float64)
cast_nullable_unyt_array_time_hours        : Cast[unyt_array] = cast_nullable_unyt_array(unit = "hr",      dtype = np.float64)
cast_nullable_unyt_array_time_days         : Cast[unyt_array] = cast_nullable_unyt_array(unit = "day",     dtype = np.float64)
cast_nullable_unyt_array_time_years        : Cast[unyt_array] = cast_nullable_unyt_array(unit = "yr",      dtype = np.float64)
cast_nullable_unyt_array_time_Gyrs         : Cast[unyt_array] = cast_nullable_unyt_array(unit = "Gyr",     dtype = np.float64)
cast_nullable_unyt_array_length_si         : Cast[unyt_array] = cast_nullable_unyt_array(unit = "m",       dtype = np.float64)
cast_nullable_unyt_array_length_imperial   : Cast[unyt_array] = cast_nullable_unyt_array(unit = "ft",      dtype = np.float64)
cast_nullable_unyt_array_length_cgs        : Cast[unyt_array] = cast_nullable_unyt_array(unit = "cm",      dtype = np.float64)
cast_nullable_unyt_array_length_solar      : Cast[unyt_array] = cast_nullable_unyt_array(unit = "Rsun",    dtype = np.float64)
cast_nullable_unyt_array_length_pc         : Cast[unyt_array] = cast_nullable_unyt_array(unit = "pc",      dtype = np.float64)
cast_nullable_unyt_array_length_kpc        : Cast[unyt_array] = cast_nullable_unyt_array(unit = "kpc",     dtype = np.float64)
cast_nullable_unyt_array_length_Mpc        : Cast[unyt_array] = cast_nullable_unyt_array(unit = "Mpc",     dtype = np.float64)
cast_nullable_unyt_array_speed_si          : Cast[unyt_array] = cast_nullable_unyt_array(unit = "m/s",     dtype = np.float64)
cast_nullable_unyt_array_speed_imperial    : Cast[unyt_array] = cast_nullable_unyt_array(unit = "ft/s",    dtype = np.float64)
cast_nullable_unyt_array_speed_cgs         : Cast[unyt_array] = cast_nullable_unyt_array(unit = "cm/s",    dtype = np.float64)
cast_nullable_unyt_array_speed_kms         : Cast[unyt_array] = cast_nullable_unyt_array(unit = "km/s",    dtype = np.float64)
cast_nullable_unyt_array_speed_Mpc_per_Gyr : Cast[unyt_array] = cast_nullable_unyt_array(unit = "Mpc/Gyr", dtype = np.float64)
cast_nullable_unyt_array_force_si          : Cast[unyt_array] = cast_nullable_unyt_array(unit = "N",       dtype = np.float64)
cast_nullable_unyt_array_force_imperial    : Cast[unyt_array] = cast_nullable_unyt_array(unit = "lbf",     dtype = np.float64)
cast_nullable_unyt_array_force_cgs         : Cast[unyt_array] = cast_nullable_unyt_array(unit = "dyn",     dtype = np.float64)
cast_nullable_unyt_array_energy_si         : Cast[unyt_array] = cast_nullable_unyt_array(unit = "J",       dtype = np.float64)
cast_nullable_unyt_array_energy_imperial   : Cast[unyt_array] = cast_nullable_unyt_array(unit = "BTU",     dtype = np.float64)
cast_nullable_unyt_array_energy_cgs        : Cast[unyt_array] = cast_nullable_unyt_array(unit = "erg",     dtype = np.float64)
cast_nullable_unyt_array_energy_eV         : Cast[unyt_array] = cast_nullable_unyt_array(unit = "eV",      dtype = np.float64)
cast_nullable_unyt_array_energy_KeV        : Cast[unyt_array] = cast_nullable_unyt_array(unit = "KeV",     dtype = np.float64)
cast_nullable_unyt_array_energy_GeV        : Cast[unyt_array] = cast_nullable_unyt_array(unit = "GeV",     dtype = np.float64)
cast_nullable_unyt_array_energy_TeV        : Cast[unyt_array] = cast_nullable_unyt_array(unit = "TeV",     dtype = np.float64)
cast_nullable_unyt_array_power_si          : Cast[unyt_array] = cast_nullable_unyt_array(unit = "W",       dtype = np.float64)
cast_nullable_unyt_array_power_imperial    : Cast[unyt_array] = cast_nullable_unyt_array(unit = "hp",      dtype = np.float64)
cast_nullable_unyt_array_power_cgs         : Cast[unyt_array] = cast_nullable_unyt_array(unit = "erg/s",   dtype = np.float64)
cast_nullable_unyt_array_power_solar       : Cast[unyt_array] = cast_nullable_unyt_array(unit = "Lsun",    dtype = np.float64)
