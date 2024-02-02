from ._ConfigsBase import ConfigsBase

class PropertiesConfig(ConfigsBase):
    def __init__(self, writable: bool = True, filepath: str = None):
        super().__init__(writable = writable, filepath = filepath)

    def read(self, filepath: str):
        with open(filepath, "r") as file:
            for line in file.readlines():
                line = line.rstrip("\n").strip()
                if line != "" and line[0] != "#":
                    self.add_item(*line.split("#", 1)[0].split("="))

    @staticmethod
    def from_file(filepath: str, writable: bool = False):
        return PropertiesConfig(writable, filepath)
