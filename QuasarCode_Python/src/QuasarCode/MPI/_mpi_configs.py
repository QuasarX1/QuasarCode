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
            self.__MPI_ROOT_RANK: int = 0

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

    @property
    def root(self) -> int:
        return self.__MPI_ROOT_RANK
    @root.setter
    def _(self, rank: int) -> None:
        self.__MPI_ROOT_RANK = rank

    def update(self, comm: MPI.Intracomm, root: int|None = None) -> None:
        _MPI_Config.__update(comm, self.root if root is None else root)

    @staticmethod
    def __update(comm: MPI.Intracomm, root: int) -> None:
        _MPI_Config.__update = True
        instance = _MPI_Config(comm)
        instance.root = root

if not _MPI_Config._is_singleton_avalible():
    _MPI_Config(MPI.COMM_WORLD)

mpi_config: _MPI_Config = _MPI_Config._get_singleton()
