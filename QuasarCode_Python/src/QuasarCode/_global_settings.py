import os

class _Settings(object):
    __singleton = None

    @staticmethod
    def _is_singleton_avalible():
        return _Settings.__singleton is not None

    @staticmethod
    def _get_singleton():
        return _Settings.__singleton

    __attribute_initial_values = {
                       "verbose" : False,
               "verbosity_level" : -1,
                         "debug" : False,
                  "mpi_avalible" : False,
                         "slurm" : "SLURM_JOB_ID" in os.environ,
               "datetime_format" : r"%d/%m/%Y, %H:%M:%S",
                   "date_format" : r"%d/%m/%Y",
                   "time_format" : r"%H:%M:%S",
           "time_format_precise" : "%H:%M:%S[%f\u03BCs]",
        "cuda_threads_per_block" : 512,
    }

    def __init__(self):
        if not _Settings._is_singleton_avalible():
            _Settings.__singleton = self
            self.__setting_values = _Settings.__attribute_initial_values.copy()
            self.__verbosity_level_cache: int = self.__setting_values["verbosity_level"]

        else:
            raise RuntimeError("Only one instance of the __Settings object may exist.")

    def __getattr__(self, name: str):
        if name in self.__setting_values:
            return self.__setting_values[name]
        else:
            raise AttributeError(f"{name} is not a valid attribute or setting name.")

    @property
    def setting_names(self):
        return list(self.__setting_values.keys())

    def _set_verbose(self, state: bool, level: int|None):
        self.__setting_values["verbose"] = state
        if state:
            if level is None:
                self.__setting_values["verbosity_level"] = 0
            else:
                self.__setting_values["verbosity_level"] = level
        else:
            self.__setting_values["verbosity_level"] = -1
    def enable_verbose(self, level: int = 0):
        self._set_verbose(True, level)
    def disable_verbose(self):
        if self.verbose:
            self.__verbosity_level_cache = self.verbosity_level
        self._set_verbose(False)
    def toggle_verbose(self):
        if self.verbose:
            self.__verbosity_level_cache = self.verbosity_level
        self._set_verbose(not self.verbose, level = self.__verbosity_level_cache)

    def _set_debug(self, state: bool): self.__setting_values["debug"] = state
    def enable_debug(self): self._set_debug(True)
    def disable_debug(self): self._set_debug(False)
    def toggle_debug(self): self._set_debug(not self.debug)

    def _set_mpi_avalible(self):
        self.__setting_values["mpi_avalible"] = True

    def set_cuda_threads_per_block(self, value: int):
        self.__setting_values["cuda_threads_per_block"] = value

if not _Settings._is_singleton_avalible():
    _Settings()

settings_object = _Settings._get_singleton()
