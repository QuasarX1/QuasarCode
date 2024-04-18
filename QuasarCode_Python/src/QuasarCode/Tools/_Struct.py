from typing import Union

class Struct(object):
    """
    Structure type definition.
    Allows a number of public instance attributes to be declared and populated from the constructor.

    Constructor Design Order:
        1.) Declare all public attributes first.
        2.) super().__init__(**kwargs)

    To specify a human readable type name for errors, overload: _get_typename(self) -> Union[str, None]
    To specify type casts for attributes, set fields to an instance of TypeCastAutoProperty
    """
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
            except AttributeError as e:
                raise AttributeError(f"{self._get_typename if self._get_typename is not None else type(self).__qualname__} struct defines no public field named \"{key}\".") from e

    @staticmethod
    def _get_typename() -> Union[str, None]:
        """
        Overload this to specify a string to appear in the error message provided when attempting to initalise a nonexistant attribute.
        """
        return None
