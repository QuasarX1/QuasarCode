from QuasarCode._global_settings import settings_object as __settings_object
from QuasarCode.MPI import _raise_mpi_error

if not __settings_object.mpi_avalible:
    _raise_mpi_error()

from mpi4py import MPI

class __MPI_Config(object):
    __singleton = None
    __update = True

    @staticmethod
    def _is_singleton_avalible():
        return __MPI_Config.__singleton is not None

    @staticmethod
    def _get_singleton():
        return __MPI_Config.__singleton

    def __init__(self, comm):
        if __MPI_Config.__update:
            __MPI_Config.__update = False
            __MPI_Config.__singleton = self
            self.__MPI_COMM = comm
            self.__MPI_COMM_SIZE = int(self.__MPI_COMM.Get_size())
            self.__MPI_RANK = self.__MPI_COMM.Get_rank()

        else:
            raise RuntimeError("Only one instance of the MPI_Config object may exist. Change configuration using the update method.")

    @property
    def comm(self):
        return self.__MPI_COMM

    @property
    def comm_size(self):
        return self.__MPI_COMM_SIZE

    @property
    def rank(self):
        return self.__MPI_RANK

    def update(self, comm):
        __MPI_Config.__update(comm)

    @staticmethod
    def __update(comm):
        __MPI_Config.__update = True
        __MPI_Config(comm)

if not __MPI_Config._is_singleton_avalible():
    __MPI_Config(MPI.COMM_WORLD)

mpi_config = __MPI_Config._get_singleton()
