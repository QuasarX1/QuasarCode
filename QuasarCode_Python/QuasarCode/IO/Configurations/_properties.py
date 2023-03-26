from ._ConfigsBase import ConfigsBase

class PropertiesConfig(ConfigsBase):
    def read(self, filepath: str):
        with open(filepath, "r") as file:
            for line in file.readlines():
                line = line.rstrip("\n", 1).strip()
                if line[0] != "#" and line != "":
                    self._add_mapping(*line.split("#", 1)[0].split("="))
