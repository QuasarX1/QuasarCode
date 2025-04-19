from ._CheckpointBase import CheckpointBase

class CheckpointState(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initialised = False
        self.__checkpoint_index = -1
        self.__checkpoint_data = None

    @property
    def checkpoint_index(self):
        if not self.__initialised:
            raise RuntimeError("This object has not been initialised yet.")
        return self.__checkpoint_index

    @property
    def checkpoint_data(self):
        if not self.__initialised:
            raise RuntimeError("This object has not been initialised yet.")
        return self.__checkpoint_data

    @checkpoint_data.setter
    def checkpoint_data(self, value):
        if not self.__initialised:
            raise RuntimeError("This object has not been initialised yet.")
        self.__checkpoint_data = value

    def initialise(self, from_checkpoint: dict = None):
        if from_checkpoint is not None:
            self.__checkpoint_index = from_checkpoint["index"]
            self.__checkpoint_data = from_checkpoint["data"]
            for i in range(len(from_checkpoint["metadata_keys"])):
                self[from_checkpoint["metadata_keys"][i]] = from_checkpoint["metadata_values"][i]
        self.__initialised = True

    def serialise(self):
        serialised = {}
        serialised["index"] = self.__checkpoint_index
        serialised["data"] = self.__checkpoint_data
        serialised["metadata_keys"] = list(self.keys())
        serialised["metadata_values"] = list(self.values())
        return serialised

    def increment_index(self):
        self.__checkpoint_index += 1
