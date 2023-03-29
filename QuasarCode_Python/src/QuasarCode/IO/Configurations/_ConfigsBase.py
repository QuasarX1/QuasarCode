from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Union

class _Mapping(object):
    def __init__(self):
        self.__writable = True
        self.__data = {}
        self.__sub_mapping_keys = []

    def __ensure_writable(func):
        def wrapper(self, *args, **kwargs):
            if self.__writable:
                return func(self, *args, **kwargs)
            else:
                raise RuntimeError("Unable to write to a non-writable configuration map.")
        return wrapper

    def __getitem__(self, *keys: List[str]):
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

    #@__ensure_writable
    #def __setitem__(self, key: str, value):
    #    print("HERE")

    def __getattr__(self, key: str):
        #print(key)
        return self[key]

    #def __setattr__(self, key: str, value):
    #    super().__setattr__(key, value)
    #    if key != "_Mapping__data" and key in self.__data:
    #        self[key] = value

    @__ensure_writable
    def add_item(self, name: str, value):
        self.__data[name] = value

    @__ensure_writable
    def add_group(self, name: str):
        self.__data[name] = _Mapping()
        self.__sub_mapping_keys.append(name)

    def lock(self):
        self.__writable = False
        for key in self.__sub_mapping_keys:
            self.__data[key]._lock()

    @property
    def writable(self):
        return self.__writable

    def _get_keys(self) -> Tuple[Union[str, Dict[str, Tuple]]]:
        ((self.__data[key]._get_keys() if key in self.__sub_mapping_keys else key) for key in self.__data)

class ConfigsBase(_Mapping, ABC):
    def __init__(self, writable: bool = True, filepath: str = None):
        super().__init__()

        if filepath is not None:
            self.read(filepath)

        if not writable:
            self.lock()

    @abstractmethod
    def read(self, filepath: str):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def from_file(filepath: str, writable: bool = False, *args, **kwargs):
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
