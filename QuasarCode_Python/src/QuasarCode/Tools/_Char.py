from typing import Union, List, Tuple, Iterable, Any

class Char(str):
    def __new__(cls, object: Union["Char", str]):
        if not isinstance(object, str):
            raise TypeError(f"{type(object)} is neither Char or str.")
        if len(object) != 1:
            raise ValueError(f"{object} is not a valid character or character string.")
        str.__new__(cls, object)

    @staticmethod
    def from_string(value: str) -> Tuple["Char", ...]:
        """
        Create a sequence of characters from a string.
        """
        return tuple(Char(c) for c in value)

    @staticmethod
    def to_string(*chars: Union["Char", str, Iterable[Union["Char", str]]]) -> str:
        """
        Create a string from a sequence of characters.
        """
        return "".join([c if isinstance(c, str) and len(c) == 1 else Char.to_string(*c) for c in chars])
