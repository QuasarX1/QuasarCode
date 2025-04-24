from ..Tools._Struct import Struct
from ..Tools._autoproperty import TypedAutoProperty, NullableTypedAutoProperty
from ..Tools._typeshield import TypeShield

from typing import Union

class VersionInfomation_Delta(Struct):
    major    = TypedAutoProperty[int](TypeShield[int](int))
    minor    = TypedAutoProperty[int](TypeShield[int](int))
    revision = TypedAutoProperty[int](TypeShield[int](int))
    alpha    = TypedAutoProperty[int](TypeShield[int](int))
    beta     = TypedAutoProperty[int](TypeShield[int](int))

class VersionInfomation(Struct):
    major    = NullableTypedAutoProperty[Union[int, None]](TypeShield[Union[int, None]](int, type(None)), default_value = 0)
    minor    = NullableTypedAutoProperty[Union[int, None]](TypeShield[Union[int, None]](int, type(None)), default_value = 0)
    revision = NullableTypedAutoProperty[Union[int, None]](TypeShield[Union[int, None]](int, type(None)), default_value = 0)
    alpha    = NullableTypedAutoProperty[Union[int, None]](TypeShield[Union[int, None]](int, type(None)), default_value = 0)
    beta     = NullableTypedAutoProperty[Union[int, None]](TypeShield[Union[int, None]](int, type(None)), default_value = 0)

    @property
    def is_alpha(self) -> bool:
        return (not self.is_beta) and (self.alpha is not None) and (self.alpha > 0)

    @property
    def is_beta(self) -> bool:
        return (self.beta is not None) and (self.beta > 0)

    def to_string(self, minimum_length = False):
        result = ""
        if self.is_alpha:
            result = f"alpha{self.alpha}"
        elif self.is_beta:
            result = f"beta{self.beta}"
        if not minimum_length or len(result) > 0 or (self.revision is not None and self.revision > 0):
            result = f"{self.revision if self.revision is not None else 0}" + (f".{result}" if len(result) > 0 else "")
        if not minimum_length or len(result) > 0 or (self.minor is not None and self.minor > 0):
            result = f"{self.minor if self.minor is not None else 0}" + (f".{result}" if len(result) > 0 else "")
        result = f"{self.major if self.major is not None else 0}" + (f".{result}" if len(result) > 0 else "")

        return result

    def __str__(self):
        return self.to_string(minimum_length = False)
    
    @staticmethod
    def from_string(value: str) -> "VersionInfomation":
        elements = value.split(".")
        if len(elements) == 0:
            elements = ["0"]
        elif len([e for e in elements if e == ""]) > 0:
            raise ValueError(f"{value} is not a valid version number string (some components blank).")
        elif len(elements) > 4:
            raise ValueError(f"{value} is not a valid version number string (too many components).")
        converted_elements = [int(e) for e in elements[:3]]
        if len(converted_elements) < 3:
            converted_elements.extend([0] * (3 - len(converted_elements)))
        converted_elements.append(int(elements[3][5:]) if len(elements) == 4 and elements[3][:5] == "alpha" else 0)
        converted_elements.append(int(elements[3][4:]) if len(elements) == 4 and elements[3][:4] == "beta" else 0)
        return VersionInfomation(
               major = converted_elements[0],
               minor = converted_elements[1],
            revision = converted_elements[2],
               alpha = converted_elements[3],
                beta = converted_elements[4]
        )

    @staticmethod
    def from_int(value: int) -> "VersionInfomation":
        if value < 0:
            raise ValueError("Can't have a negitive version number.")
        return VersionInfomation(
               major = value,
               minor = 0,
            revision = 0,
               alpha = 0,
                beta = 0
        )
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, int):
            return self.major == value and self.minor in (0, None) and self.revision in (0, None) and self.alpha is None and self.beta is None
        elif isinstance(value, VersionInfomation):
            return self.major == value.major and self.minor == value.minor and self.revision == value.revision and self.alpha == value.alpha and self.beta == value.beta
        else:
            return False
        
    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)
    
    def __sub__(self, value: Union["VersionInfomation", int]) -> VersionInfomation_Delta:
        if isinstance(value, int):
            return VersionInfomation_Delta(
                   major = (self.major if self.major is not None else 0) - value,
                   minor = 0,
                revision = 0,
                   alpha = 0,
                    beta = 0
            )
        elif isinstance(value, VersionInfomation):
            return VersionInfomation_Delta(
                   major = (self.major    if self.major    is not None else 0) - (value.major    if value.major    is not None else 0),
                   minor = (self.minor    if self.minor    is not None else 0) - (value.minor    if value.minor    is not None else 0),
                revision = (self.revision if self.revision is not None else 0) - (value.revision if value.revision is not None else 0),
                   alpha = (self.alpha    if self.alpha    is not None else 0) - (value.alpha    if value.alpha    is not None else 0),
                    beta = (self.beta     if self.beta     is not None else 0) - (value.beta     if value.beta     is not None else 0)
            )
        else:
            raise TypeError(f"Unsupported operation between VersionInfomation and object of type {type(value)}.")
    
    def __add__(self, value: VersionInfomation_Delta) -> "VersionInfomation":
        if isinstance(value, int):
            if (self.major if self.major is not None else 0) + value < 0:
                raise ValueError(f"Unable to subtract {-value} from a major version of {(self.major if self.major is not None else 0)}.")
            
            return VersionInfomation(
                   major = (self.major if self.major is not None else 0) + value,
                   minor = 0,
                revision = 0,
                   alpha = 0,
                    beta = 0
            )
        
        elif isinstance(value, VersionInfomation):
            new_major    = (self.major    if self.major    is not None else 0) + value.major,
            new_minor    = (self.minor    if self.minor    is not None else 0) + value.minor,
            new_revision = (self.revision if self.revision is not None else 0) + value.revision,
            new_alpha    = (self.alpha    if self.alpha    is not None else 0) + value.alpha,
            new_beta     = (self.beta     if self.beta     is not None else 0) + value.beta

            if new_major < 0:    raise ValueError(f"Unable to subtract {-value} from a major version of {   (self.major    if self.major    is not None else 0)}.")
            if new_minor < 0:    raise ValueError(f"Unable to subtract {-value} from a minor version of {   (self.minor    if self.minor    is not None else 0)}.")
            if new_revision < 0: raise ValueError(f"Unable to subtract {-value} from a revision version of {(self.revision if self.revision is not None else 0)}.")
            if new_alpha < 0:    raise ValueError(f"Unable to subtract {-value} from a alpha version of {   (self.alpha    if self.alpha    is not None else 0)}.")
            if new_beta < 0:     raise ValueError(f"Unable to subtract {-value} from a beta version of {    (self.beta     if self.beta     is not None else 0)}.")

            return VersionInfomation_Delta(
                   major = new_major,
                   minor = new_minor,
                revision = new_revision,
                   alpha = new_alpha,
                    beta = new_beta
            )
        
        else:
            raise TypeError(f"Unsupported operation between VersionInfomation and object of type {type(value)}.")
