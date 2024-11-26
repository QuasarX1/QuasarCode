from ._console import Console
from ...Tools._stopwatch import IStopwatch, SimpleStopwatch
from ..._global_settings import settings_object as _settings_object

from collections.abc import Sequence

import numpy as np
import datetime



class Stopwatch(IStopwatch):
    """
    Feature rich stopwatch implementation with printing options.
    """

    @staticmethod
    def start_new(name: str|None = None) -> "Stopwatch":
        stopwatch = Stopwatch(name)
        stopwatch.start()
        return stopwatch
    @staticmethod
    def synchronise_start_new(synchronise: IStopwatch, name: str|None = None) -> "Stopwatch":
        stopwatch = Stopwatch()
        stopwatch.synchronise_start(synchronise)
        return stopwatch
    
    @staticmethod
    def new_group(number: int, names: Sequence[str|None]|None = None) -> "tuple[Stopwatch]":
        return tuple([Stopwatch(names[i] if names is not None else None) for i in range(number)])
    @staticmethod
    def start_new_group(number: int, names: Sequence[str|None]|None = None) -> "tuple[Stopwatch]":
        stopwatches = tuple([Stopwatch(names[i] if names is not None else None) for i in range(number)])
        stopwatches[0].start()
        for i in range(1, number):
            stopwatches[i].synchronise_start(stopwatches[0])
        return stopwatches
    @staticmethod
    def synchronise_start_new_group(number: int, synchronise: "IStopwatch", names: Sequence[str|None]|None = None) -> "tuple[Stopwatch]":
        return tuple([Stopwatch.synchronise_start_new(synchronise, names[i] if names is not None else None) for i in range(number)])

    def __init__(self, name: str|None = None):
        self.__name = name if name is not None else "Stopwatch"
        self.__internal_stopwatch = SimpleStopwatch()

    #TODO: add context manager methods for easy time reporting (retain as variable to use time data, otherwise set to print time)

    @staticmethod
    def __strftime(dt: datetime.timedelta|float):
        if isinstance(dt, float):
            dt = datetime.timedelta(seconds = dt)
        return (datetime.datetime(year = 1, month = 1, day = 1) + dt).strftime(_settings_object.time_format_precise)
    
    def reset(self) -> None:
        self.__internal_stopwatch.reset()

    def start(self) -> None:
        self.__internal_stopwatch.start()

    def synchronise_start(self, synchronise: IStopwatch) -> None:
        self.__internal_stopwatch.synchronise_start(synchronise)

    def lap(self) -> float:
        return self.__internal_stopwatch.lap()

    def print_lap(self) -> float:
        dt = self.lap()
        Console.custom_print("|TIME|", f"{self.__name}: LAP {Stopwatch.__strftime(dt)} ({Stopwatch.__strftime(self.get_elapsed_time())})", show_insert = True)
        return dt

    def stop(self) -> float:
        return self.__internal_stopwatch.stop()

    def print_stop(self) -> float:
        dt = self.stop()
        Console.custom_print("|TIME|", f"{self.__name}: LAP {Stopwatch.__strftime(dt)} ({Stopwatch.__strftime(self.get_elapsed_time())}) STOPPED", show_insert = True)
        return dt
    
    def get_start_time(self) -> float:
        return self.__internal_stopwatch.get_start_time()
    
    def get_elapsed_time(self) -> float:
        return self.__internal_stopwatch.get_elapsed_time()
    
    def get_elapsed_time_lap(self) -> float:
        return self.__internal_stopwatch.get_elapsed_time_lap()

    def get_elapsed_time_last_lap(self) -> float:
        return self.__internal_stopwatch.get_elapsed_time_last_lap()

    def __str__(self) -> str:
        return self.__internal_stopwatch.__str__()

    def __repr__(self) -> str:
        if self.running:
            return f"Stopwatch: {self.get_elapsed_time()}"
        elif self.stopped:
            return f"Stopwatch: {self.get_elapsed_time()} (stopped)"
        else:
            return "Stopwatch: not yet started"
        
    def __float__(self):
        return self.__internal_stopwatch.__float__()
        
    def __int__(self):
        return self.__internal_stopwatch.__int__()

    @property
    def running(self) -> bool:
        return self.__internal_stopwatch.running
    @property
    def started(self) -> bool:
        return self.__internal_stopwatch.started
    @property
    def stopped(self) -> bool:
        return self.__internal_stopwatch.stopped

    def __create_print_sting__elapsed_time(self) -> str:
        return f"{self.__name}: {Stopwatch.__strftime(self.get_elapsed_time())}"
    def print_elapsed_time(self, show_insert: bool = True, **kwargs) -> None:
        Console.custom_print("|TIME|", self.__create_print_sting__elapsed_time(), show_insert = show_insert, **kwargs)
    def print_verbose_elapsed_time(self, show_insert: bool = True, verbosity_level: int = -1, **kwargs) -> None:
        Console.custom_print_verbose("|TIME|", self.__create_print_sting__elapsed_time(), show_insert = show_insert, verbosity_level = verbosity_level, **kwargs)
    def print_verbose_debug_elapsed_time(self, show_insert: bool = True, verbosity_level: int = -1, **kwargs) -> None:
        Console.custom_print_verbose_debug("|TIME|", self.__create_print_sting__elapsed_time(), show_insert = show_insert, verbosity_level = verbosity_level, **kwargs)
    def print_debug_elapsed_time(self, show_insert: bool = True, **kwargs) -> None:
        Console.custom_print_debug("|TIME|", self.__create_print_sting__elapsed_time(), show_insert = show_insert, **kwargs)

    def __create_print_sting__elapsed_time_lap(self) -> str:
        return f"{self.__name}: LAP {Stopwatch.__strftime(self.get_elapsed_time_lap())}"
    def print_elapsed_time_lap(self, show_insert: bool = True, **kwargs) -> None:
        Console.custom_print("|TIME|", self.__create_print_sting__elapsed_time_lap(), show_insert = show_insert, **kwargs)
    def print_verbose_elapsed_time_lap(self, show_insert: bool = True, verbosity_level: int = -1, **kwargs) -> None:
        Console.custom_print_verbose("|TIME|", self.__create_print_sting__elapsed_time_lap(), show_insert = show_insert, verbosity_level = verbosity_level, **kwargs)
    def print_verbose_debug_elapsed_time_lap(self, show_insert: bool = True, verbosity_level: int = -1, **kwargs) -> None:
        Console.custom_print_verbose_debug("|TIME|", self.__create_print_sting__elapsed_time_lap(), show_insert = show_insert, verbosity_level = verbosity_level, **kwargs)
    def print_debug_elapsed_time_lap(self, show_insert: bool = True, **kwargs) -> None:
        Console.custom_print_debug("|TIME|", self.__create_print_sting__elapsed_time_lap(), show_insert = show_insert, **kwargs)

    def __create_print_sting__elapsed_time_last_lap(self) -> str:
        return f"{self.__name}: LAP(-1) {Stopwatch.__strftime(self.get_elapsed_time_last_lap())}"
    def print_elapsed_time_last_lap(self, show_insert: bool = True, **kwargs) -> None:
        Console.custom_print("|TIME|", self.__create_print_sting__elapsed_time_last_lap(), show_insert = show_insert, **kwargs)
    def print_verbose_elapsed_time_last_lap(self, show_insert: bool = True, verbosity_level: int = -1, **kwargs) -> None:
        Console.custom_print_verbose("|TIME|", self.__create_print_sting__elapsed_time_last_lap(), show_insert = show_insert, verbosity_level = verbosity_level, **kwargs)
    def print_verbose_debug_elapsed_time_last_lap(self, show_insert: bool = True, verbosity_level: int = -1, **kwargs) -> None:
        Console.custom_print_verbose_debug("|TIME|", self.__create_print_sting__elapsed_time_last_lap(), show_insert = show_insert, verbosity_level = verbosity_level, **kwargs)
    def print_debug_elapsed_time_last_lap(self, show_insert: bool = True, **kwargs) -> None:
        Console.custom_print_debug("|TIME|", self.__create_print_sting__elapsed_time_last_lap(), show_insert = show_insert, **kwargs)
