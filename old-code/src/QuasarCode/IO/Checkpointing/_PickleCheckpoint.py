import pickle

from . import CheckpointBase

class PickleCheckpoint(CheckpointBase):
    """
    WARNING: This class uses pickle binary files. These are INSECURE and may be altered maliciously!
             Use with caution and never load pickle files that you didn't create yourself.
    """

    def _read_file(self, filepath):
        print("READING")
        data = None
        with open(filepath, "rb") as file:
            data = pickle.load(file)
        return data

    def _write_file(self, filepath, data, *args, **kwargs):
        with open(filepath, "wb") as file:
            pickle.dump(data, file)
