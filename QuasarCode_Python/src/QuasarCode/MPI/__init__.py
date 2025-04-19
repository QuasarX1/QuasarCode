import warnings

from .._global_settings import settings_object as __settings_object



# Try to load the mpi4py package and catch any errors
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



# Load the stuff that dosen't depend on the rest of the package
if __settings_object.mpi_avalible:
    from ._independant_mpi._mpi_config import mpi_config as MPI_Config
    def get_mpi_rank() -> int:
        return MPI_Config.rank
else:
    from ._independant_dummy._mpi_config import mpi_config as MPI_Config
    # This dummy function needs to be here to avoid circular imports when all that is needed is the current rank
    def get_mpi_rank() -> int:
        return 0



# Now import stuff that has dependancies from elsewhere in tha package
if __settings_object.mpi_avalible:
    from ._dependant_mpi import *
else:
    # Load everything else from the _dummy subpackage instead
    from ._dependant_dummy import *
