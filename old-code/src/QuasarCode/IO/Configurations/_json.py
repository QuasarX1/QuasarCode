import json

from ._ConfigsBase import ConfigsBase

class JsonConfig(ConfigsBase):
    def __init__(self, writable: bool = True, filepath: str = None, expand_maps: bool = True, map_expansion_limit: int = -1):
        if map_expansion_limit < -1 or map_expansion_limit == 0:
            raise ValueError(f"paramiter map_expansion_limit cannot have a value of {map_expansion_limit}. It must be either a positive, non-zero integer, or -1 to indicate no limit.")
        self.__expand_maps = expand_maps
        self.__map_expansion_limit = map_expansion_limit
        super().__init__(writable = writable, filepath = filepath)

    def read(self, filepath: str):
        with open(filepath, "r") as file:
            json_data = json.load(file)

            if not isinstance(json_data, dict):
                raise RuntimeError("Invalid configuration file format. JSON configuration files must be a map/dictionary at the highest level.")

            def recursivley_add_mappings(root, data, n_further_expansions):
                for key in data:
                    if n_further_expansions != 0 and isinstance(data[key], dict):
                        root.add_group(key)
                        recursivley_add_mappings(root[key], data[key], n_further_expansions if n_further_expansions == -1 else n_further_expansions - 1)
                    else:
                        root.add_item(key, data[key])

            recursivley_add_mappings(self, json_data, self.__map_expansion_limit if self.__expand_maps else 0)

    @staticmethod
    def from_file(filepath: str, writable: bool = False, expand_maps: bool = True, map_expansion_limit: int = -1):
        return JsonConfig(writable, filepath, expand_maps, map_expansion_limit)
