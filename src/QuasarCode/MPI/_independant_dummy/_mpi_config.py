from typing import cast
import warnings

from QuasarCode._global_settings import settings_object as __settings_object
from .._MPI_Config_Base import _MPI_Config_Base

if __settings_object.mpi_avalible:
    warnings.warn("Attempted to load MPI configuration type when mpi4py module is avalible.")



class _MPI_Config(_MPI_Config_Base[None]):
    """
    MPI Configuration

    (MPI disabled version)

    (readonly) comm

    (readonly) comm_size

    (readonly) rank

    (set; get) root

    (readonly) is_root

    check_is_root(int|None)

    update(comm-type, int|None)
    """

    def __init__(self, comm: None) -> None:
        super().__init__(
            comm = None,
            size = 1,
            rank = 0,
            root = 0
        )

if not _MPI_Config._is_singleton_avalible():
    _MPI_Config(None)

mpi_config: _MPI_Config = cast(_MPI_Config, _MPI_Config._get_singleton())
