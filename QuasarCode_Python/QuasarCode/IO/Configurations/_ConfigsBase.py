from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Union

class _Mapping(object):
    def __init__(self):
        self.__wratable = True
        self.__data = {}
        self.__sub_mapping_keys = []

    def __index__(self, *keys: List[str]):
        if keys[0] in self.__data:
            value = self.__data[keys[0]]
            if len(keys) > 1:
                if isinstance(value, _Mapping):
                    return value[keys[1:]]
                else:
                    raise TypeError(f"Value of {keys[0]} is a root node and cannot be automatically indexed further.")
            else:
                return value
        else:
            raise AttributeError(f"{keys[0]} is not a valid attribute or config name.")

    def __getattr__(self, name: str):
        return self[name]

    def __ensure_writable(func):
        def wrapper(self, *args, **kwargs):
            if self.__wratable:
                return func(*args, **kwargs)
            else:
                raise RuntimeError("Unable to write to a constructed configuration map.")
        return wrapper

    @__ensure_writable
    def _add_mapping(self, name: str, value):
        self.__data[name] = value

    @__ensure_writable
    def _new_sub_mapping(self, name: str):
        self.__data[name] = _Mapping()
        self.__sub_mapping_keys.append(name)

    def _lock(self):
        self.__writable = False
        for key in self.__sub_mapping_keys:
            self.__data[key]._lock()

    def _get_keys(self) -> Tuple[Union[str, Dict[str, Tuple]]]:
        ((self.__data[key]._get_keys() if key in self.__sub_mapping_keys else key) for key in self.__data)

class ConfigsBase(_Mapping, ABC):
    def __init__(self, filepath: str):
        super().__init__()

        self.read(filepath)

        self._lock()

    @abstractmethod
    def read(self, filepath: str):
        raise NotImplementedError()

    def __str__(self):
        highrarchy = self._get_keys()

        result = ""
        indent = 0
        def recursive_writer(sub_highrarchy):
            nested_item_indexes = []
            for index, value in enumerate(sub_highrarchy):
                if isinstance(value, dict):
                    nested_item_indexes.append(index)
                else:
                    result += (" " * indent) + value + "\n"

            for index in nested_item_indexes:
                value = sub_highrarchy[index]
                result += (" " * indent) + "\n"
                result += (" " * indent) + f"{list(value.keys())[0]}:\n"
                indent += 4
                recursive_writer(list(value.values[0]))
                indent -= 4

    def __repr__(self):
        return "Configuration Object. Items as follows:\n\n" + self.__str__()
