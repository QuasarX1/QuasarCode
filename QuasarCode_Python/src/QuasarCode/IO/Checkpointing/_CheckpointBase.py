from ... import Settings
from ...MPI import get_mpi_rank
import os
import sys
from abc import ABC, abstractmethod
import uuid

class CheckpointBase(ABC):
    def __init__(self, filepath: str, checkpoint_file_extension = "checkpoint", backup_file_extension = "backup"):
        self.__filepath = filepath
        self.__file_extension = checkpoint_file_extension if not Settings.mpi_avalible else f"{checkpoint_file_extension}.{get_mpi_rank()}"
        self.__backup_extension = f"{checkpoint_file_extension}.{backup_file_extension}" if not Settings.mpi_avalible else f"{checkpoint_file_extension}.{backup_file_extension}.{get_mpi_rank()}"

        self.__checkpoint_file = f"{self.__filepath}.{self.__file_extension}"
        self.__backup_file = f"{self.__filepath}.{self.__backup_extension}"

        self._update_file_avalibility()

    @property
    def checkpoint_file(self):
        return self.__checkpoint_file

    @property
    def backup_file(self):
        return self.__backup_file

    @property
    def checkpoint_avalible(self):
        return  self.__checkpoint_avalible

    @property
    def backup_avalible(self):
        return  self.__checkpoint_avalible

    def _update_file_avalibility(self):
        self.__checkpoint_avalible = os.path.exists(self.__checkpoint_file)
        self.__backup_avalible = os.path.exists(self.__backup_file)

    @abstractmethod
    def _read_file(self, filepath):
        raise NotImplementedError("Must be overridden by a child class.")

    def read_checkpoint(self):
        if not self.__checkpoint_avalible:
            raise FileNotFoundError("There is no current checkpoint to read.")
        return self._read_file(self.__checkpoint_file)

    def read_backup(self):
        if not self.__backup_avalible:
            raise FileNotFoundError("There is no backup checkpoint to read.")
        return self._read_file(self.__backup_file)

    @abstractmethod
    def _write_file(self, filepath, data, *args, **kwargs):
        raise NotImplementedError("Must be overridden by a child class.")

    def write_checkpoint(self, data, *args, **kwargs):
        if self.__checkpoint_avalible:
            self._move_to_backup()
        return self._write_file(self.__checkpoint_file, data, *args, **kwargs)
        self._update_file_avalibility()

    def _move_to_backup(self):
        if not self.__checkpoint_avalible:
            raise FileNotFoundError("No checkpoint to backup.")

        tempfile_exists = False
        if self.__backup_avalible:
            tempfile_name = f".QCtempcheckpointbackupfile-{str(uuid.uuid4())}"
            os.rename(self.__backup_file, tempfile_name)
            tempfile_exists = True

        self._update_file_avalibility()
        try:
            os.rename(self.__checkpoint_file, self.__backup_file)
            self._update_file_avalibility()
            if self.__checkpoint_avalible:
                raise FileExistsError("Failed to create backup from existing checkpoint.")
        except:
            if tempfile_exists:
                os.rename(tempfile_name, self.__backup_file)
                tempfile_exists = False
        finally:
            if tempfile_exists:
                os.remove(tempfile_name)
            self._update_file_avalibility()

    def remove_checkpoint(self):
        os.remove(self.__checkpoint_file)
        self._update_file_avalibility()

    def remove_backup(self):
        os.remove(self.__backup_file)
        self._update_file_avalibility()
