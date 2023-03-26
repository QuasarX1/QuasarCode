class _Settings(object):
    __singleton = None

    @staticmethod
    def _is_singleton_avalible():
        return _Settings.__singleton is not None

    @staticmethod
    def _get_singleton():
        return _Settings.__singleton

    __attribute_initial_values = {
        "verbose": False,
        "debug": False,
        "mpi_avalible": False,
        "cuda_threads_per_block": 512,
    }

    def __init__(self):
        if not _Settings._is_singleton_avalible():
            _Settings.__singleton = self
            self.__setting_values = _Settings.__attribute_initial_values.copy()

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

    def _set_verbose(self, state: bool): self.__setting_values["verbose"] = state
    def enable_verbose(self): self._set_verbose(True)
    def disable_verbose(self): self._set_verbose(False)
    def toggle_verbose(self): self._set_verbose(not self.verbose)

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
