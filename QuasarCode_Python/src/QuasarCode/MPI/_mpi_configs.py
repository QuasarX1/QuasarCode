from QuasarCode._global_settings import settings_object as __settings_object
from QuasarCode.MPI import _raise_mpi_error

if not __settings_object.mpi_avalible:
    _raise_mpi_error()

from mpi4py import MPI

class _MPI_Config(object):
    __singleton: "_MPI_Config|None" = None
    __update: bool = True

    @staticmethod
    def _is_singleton_avalible() -> bool:
        return _MPI_Config.__singleton is not None

    @staticmethod
    def _get_singleton() -> "_MPI_Config|None":
        return _MPI_Config.__singleton

    def __init__(self, comm: MPI.Intracomm) -> None:
        if _MPI_Config.__update:
            _MPI_Config.__update = False
            _MPI_Config.__singleton = self
            self.__MPI_COMM: MPI.Intracomm = comm
            self.__MPI_COMM_SIZE: int = int(self.__MPI_COMM.Get_size())
            self.__MPI_RANK: int = self.__MPI_COMM.Get_rank()

        else:
            raise RuntimeError("Only one instance of the MPI_Config object may exist. Change configuration using the update method.")

    @property
    def comm(self) -> MPI.Intracomm:
        return self.__MPI_COMM

    @property
    def comm_size(self) -> int:
        return self.__MPI_COMM_SIZE

    @property
    def rank(self) -> int:
        return self.__MPI_RANK

    def update(self, comm) -> None:
        _MPI_Config.__update(comm)

    @staticmethod
    def __update(comm) -> None:
        _MPI_Config.__update = True
        _MPI_Config(comm)

if not _MPI_Config._is_singleton_avalible():
    _MPI_Config(MPI.COMM_WORLD)

mpi_config: _MPI_Config = _MPI_Config._get_singleton()
