from ._ConfigsBase import ConfigsBase

class MappingConfigBase(ConfigsBase):
    def __init__(self, comment_char: str, assignment_char: str, writable: bool = True, filepath: str = None):
        self.__comment_char = comment_char
        self.__assignment_char = assignment_char
        super().__init__(writable = writable, filepath = filepath)

    @property
    def comment(self) -> str:
        return self.__comment_char

    @property
    def assignment(self) -> str:
        return self.__assignment_char

    def read(self, filepath: str):
        with open(filepath, "r") as file:
            for line in file.readlines():
                line = line.rstrip("\n").strip()
                if line != "" and line[0] != self.__comment_char:
                    self.add_item(*line.split(self.__comment_char, 1)[0].split(self.__assignment_char))

def make_custom_mapping(comment_char: str, assignment_char: str):
    class CustomMappingConfig(MappingConfigBase):
        def __init__(self, writable: bool = True, filepath: str = None):
            super().__init__(comment_char = comment_char,
                            assignment_char = assignment_char,
                            writable = writable,
                            filepath = filepath)

        @staticmethod
        def from_file(filepath: str, writable: bool = False):
            return CustomMappingConfig(writable, filepath)
    
    return CustomMappingConfig

class PropertiesConfig(MappingConfigBase):
    def __init__(self, writable: bool = True, filepath: str = None):
        super().__init__(comment_char = "#",
                         assignment_char = "=",
                         writable = writable,
                         filepath = filepath)

    @staticmethod
    def from_file(filepath: str, writable: bool = False):
        return PropertiesConfig(writable, filepath)
