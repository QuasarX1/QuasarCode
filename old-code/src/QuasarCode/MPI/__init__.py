import warnings

from .._global_settings import settings_object as __settings_object

try:
    from mpi4py import MPI
    __settings_object._set_mpi_avalible()
    _display_mpi_warning = lambda *args, **kwargs: None
    _raise_mpi_error = lambda *args, **kwargs: None
except:
    def _display_mpi_warning(*args, **kwargs):
        warnings.warn("Either mpi4py is not avalible, the program was not started for use with MPI or mpi4py failed to install/load correctly. Disabling optional MPI functionality. Non-optional MPI functionality is not avalible.", ImportWarning)
    def _raise_mpi_error(*args, **kwargs):
        raise ImportError("Either mpi4py is not avalible, the program was not started for use with MPI or mpi4py failed to install/load correctly.")

if __settings_object.mpi_avalible:
    from ._mpi_configs import mpi_config as MPI_Config

    def get_mpi_rank():
        return MPI_Config.rank

else:
    def get_mpi_rank():
        return 0
