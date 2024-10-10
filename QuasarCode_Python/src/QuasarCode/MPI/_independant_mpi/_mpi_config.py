from typing import cast

from QuasarCode._global_settings import settings_object as __settings_object
from QuasarCode.MPI import _raise_mpi_error
from .._MPI_Config_Base import _MPI_Config_Base

if not __settings_object.mpi_avalible:
    _raise_mpi_error()

from mpi4py import MPI



class _MPI_Config(_MPI_Config_Base[MPI.Intracomm]):
    """
    MPI Configuration

    (MPI enabled version)

    (readonly) comm

    (readonly) comm_size

    (readonly) rank

    (set; get) root

    (readonly) is_root

    check_is_root(int|None)

    update(comm-type, int|None)
    """

    def __init__(self, comm: MPI.Intracomm) -> None:
        super().__init__(
            comm = comm,
            size = comm.Get_size(),
            rank = comm.Get_rank(),
            root = 0
        )

if not _MPI_Config._is_singleton_avalible():
    _MPI_Config(MPI.COMM_WORLD)

mpi_config: _MPI_Config = cast(_MPI_Config, _MPI_Config._get_singleton())
