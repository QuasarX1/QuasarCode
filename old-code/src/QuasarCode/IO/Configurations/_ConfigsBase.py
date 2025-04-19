from abc import ABC, abstractmethod
import copy
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

    def __internal_get_item(self, *keys: List[str]):
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

    def __getitem__(self, *keys: List[str]):
        #return copy.copy(self.__internal_get_item(*keys))
        return self.__internal_get_item(*keys)

    #@__ensure_writable
    #def __setitem__(self, key: str, value):
    #    print("HERE")

    def __getattr__(self, key: str):
        #return copy.copy(self.__internal_get_item(key))
        return self.__internal_get_item(key)

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
            self.__data[key].lock()

    @property
    def writable(self):
        return self.__writable

    def _get_keys(self) -> Tuple[Union[str, Dict[str, Tuple]]]:
        print("WARNING: this method is depreciated and will be removed in a future update! Use object.keys instead.")
        #return ((self.__data[key]._get_keys() if key in self.__sub_mapping_keys else key) for key in self.__data)
        return list(self.__data.keys())

    @property
    def keys(self):
        return list(self.__data.keys())

class ConfigsBase(_Mapping, ABC):
    def __init__(self, writable: bool = True, filepath: str = None):
        self.__stringify_storage = None
        self.__stringify_indent = None

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
        highrarchy = self

        self.__stringify_storage = ""
        self.__stringify_indent = 0
        def recursive_writer(sub_highrarchy):
            all_keys = sub_highrarchy.keys

            if len(all_keys) == 0:
                return# There is nothing to display here

            non_mapping_key_indexes = [i for i, key in enumerate(all_keys) if not isinstance(sub_highrarchy[key], _Mapping)]
            if len(non_mapping_key_indexes) > 0:
                max_key_length = max([len(all_keys[i]) for i in non_mapping_key_indexes])

                # Display non-mapables
                for key_index in non_mapping_key_indexes:
                    key = all_keys[key_index]
                    value = sub_highrarchy[key]

                    insert_value = ('"'+value+'"') if isinstance(value, str) else value
                    self.__stringify_storage += (" " * self.__stringify_indent) + f"{key}{' ' * (max_key_length - len(key))} = {insert_value}\n"

            # Recursivley display mappables
            for key in (all_keys if len(non_mapping_key_indexes) == 0 else [key for i, key in enumerate(all_keys) if i not in non_mapping_key_indexes]):
                value = sub_highrarchy[key]

                self.__stringify_storage += (" " * self.__stringify_indent) + "\n"
                self.__stringify_storage += (" " * self.__stringify_indent) + f"{key}:\n"
                self.__stringify_indent += 4
                recursive_writer(value)
                self.__stringify_indent -= 4

        recursive_writer(highrarchy)
        return self.__stringify_storage.lstrip("\n")

    def __repr__(self):
        return "Configuration Object. Items as follows:\n\n" + self.__str__()
