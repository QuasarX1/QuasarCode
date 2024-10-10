from abc import ABC
from typing import TypeVar, Generic



T = TypeVar("T")

class _MPI_Config_Base(ABC, Generic[T]):
    __singleton: "_MPI_Config_Base|None" = None
    __update: bool = True

    @staticmethod
    def _is_singleton_avalible() -> bool:
        return _MPI_Config_Base.__singleton is not None

    @staticmethod
    def _get_singleton() -> "_MPI_Config_Base|None":
        return _MPI_Config_Base.__singleton
    
    def __init__(self, comm: T, size: int, rank: int, root: int) -> None:
        if _MPI_Config_Base.__update:
            _MPI_Config_Base.__update = False
            _MPI_Config_Base.__singleton = self
            self.__MPI_COMM: T = comm
            self.__MPI_COMM_SIZE: int = size
            self.__MPI_RANK: int = rank
            self.__MPI_ROOT_RANK: int = root

        else:
            raise RuntimeError("Only one instance of the MPI_Config object may exist. Change configuration using the update method.")

    @property
    def comm(self) -> T:
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
    def root(self, rank: int) -> None:
        if not isinstance(rank, int):
            raise TypeError(f"Type of argument provided for parameter \"rank\" is {type(rank)} not int.")
        if rank < 0 or rank >= self.comm_size:
            raise ValueError(f"Argument provided for parameter \"rank\" was {rank} which is outside the valid range 0 -> {self.comm_size - 1}")
        self.__MPI_ROOT_RANK = rank

    @property
    def is_root(self) -> bool:
        return self.rank == self.root
    def check_is_root(self, root: int|None = None) -> bool:
        """
        Equivilant of root_rank == current_rank but allows for the default case where root_rank is the configured root rank for the default communicator.
        """
        return self.rank == (self.root if root is None else root)

    def update(self, comm: T, root: int|None = None) -> None:
        _MPI_Config_Base.__update(comm, self.root if root is None else root)

    @classmethod
    def __update(cls, comm: T, root: int) -> None:
        _MPI_Config_Base.__update = True
        instance = cls(comm)
        instance.root = root
