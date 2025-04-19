from ._CheckpointBase import CheckpointBase
from ._PickleCheckpoint import PickleCheckpoint
from ._CheckpointState import CheckpointState

class CheckpointController(object):
    def __init__(self, empty_data_structure: object, filepath: str, checkpointType: type = PickleCheckpoint, **kwargs):
        if CheckpointBase not in checkpointType.mro():
            raise TypeError("Checkpoint type idoes not inherit from the class CheckpointBase.")

        self.__checkpoint_handeler = checkpointType(filepath, **kwargs)
        self.__current_state = CheckpointState()
        
        if self.__checkpoint_handeler.checkpoint_avalible:
            self.__current_state.initialise(from_checkpoint = self.__checkpoint_handeler.read_checkpoint())

        else:
            self.__current_state.initialise()
            self.__current_state.checkpoint_data = empty_data_structure

    @property
    def data(self):
        return self.__current_state.checkpoint_data

    @data.setter
    def data(self, value):
        self.__current_state.checkpoint_data = value

    @property
    def state(self):
        return self.__current_state

    def checkpoint(self):
        self.__current_state.increment_index()
        self.__checkpoint_handeler.write_checkpoint(self.__current_state.serialise())

    def restore_backup(self):
        if not self.__checkpoint_handeler.backup_avalible:
            raise FileNotFoundError("No backup to restore from.")
        self.__current_state = CheckpointState()
        self.__current_state.initialise(from_checkpoint = self.__checkpoint_handeler.read_backup())

    def remove_checkpoint(self):
        self.__checkpoint_handeler.remove_checkpoint()

    def remove_backup(self):
        self.__checkpoint_handeler.remove_backup()
