import time
from abc import ABC, abstractmethod



class StopwatchNotStartedError(Exception):
    pass
class StopwatchStartedError(Exception):
    pass
class StopwatchStoppedError(Exception):
    pass



class IStopwatch(ABC):
    """
    Interface for stopwatch types.
    """

    @staticmethod
    @abstractmethod
    def start_new(*args, **kwargs) -> "IStopwatch":
        raise NotImplementedError()
    @staticmethod
    @abstractmethod
    def synchronise_start_new(synchronise: "IStopwatch", *args, **kwargs) -> "IStopwatch":
        raise NotImplementedError()
    
    @staticmethod
    @abstractmethod
    def new_group(number: int, *args, **kwargs) -> "tuple[IStopwatch]":
        raise NotImplementedError()
    @staticmethod
    @abstractmethod
    def start_new_group(number: int, *args, **kwargs) -> "tuple[IStopwatch]":
        raise NotImplementedError()
    @staticmethod
    @abstractmethod
    def synchronise_start_new_group(number: int, synchronise: "IStopwatch", *args, **kwargs) -> "tuple[IStopwatch]":
        raise NotImplementedError()

    @abstractmethod
    def reset(self) -> None:
        """
        Reset the stopwatch state.
        """
        raise NotImplementedError()
    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError()
    @abstractmethod
    def synchronise_start(self, synchronise: "IStopwatch") -> None:
        raise NotImplementedError()
    @abstractmethod
    def lap(self) -> float:
        """
        Record the time of the call and returns the number of seconds since the last `lap` or `start` call.
        """
        raise NotImplementedError()
    @abstractmethod
    def stop(self) -> float:
        """
        Stop the stopwatch.
        Record the time of the call and returns the number of seconds since the last `lap` or `start` call.
        """
        raise NotImplementedError()
    @abstractmethod
    def get_start_time(self) -> float:
        raise NotImplementedError()
    @abstractmethod
    def get_elapsed_time(self) -> float:
        """
        Return the time in seconds since the stopwatch was started.
        """
        raise NotImplementedError()
    @abstractmethod
    def get_elapsed_time_lap(self) -> float:
        """
        Return the time in seconds since the last lap or stopwatch was started.
        """
        raise NotImplementedError()
    @abstractmethod
    def get_elapsed_time_last_lap(self) -> float:
        """
        Return the time in seconds of the last complete lap.

        Returns 0.0 if neither `lap` or `stop` have been called.
        """
        raise NotImplementedError()

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError()
    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError()
    @abstractmethod
    def __float__(self) -> float:
        raise NotImplementedError()
    @abstractmethod
    def __int__(self) -> int:
        raise NotImplementedError()

    @property
    @abstractmethod
    def running(self) -> bool:
        raise NotImplementedError()
    @property
    @abstractmethod
    def started(self) -> bool:
        raise NotImplementedError()
    @property
    @abstractmethod
    def stopped(self) -> bool:
        raise NotImplementedError()

    @property
    @abstractmethod
    def start_time(self) -> float|None:
        raise NotImplementedError()
    @property
    @abstractmethod
    def lap_times(self) -> tuple[float]:
        raise NotImplementedError()
    @property
    @abstractmethod
    def stop_time(self) -> float|None:
        raise NotImplementedError()
    


class SimpleStopwatch(IStopwatch):
    """
    Basic stopwatch implementation for easy timing.
    """

    @staticmethod
    def start_new() -> "SimpleStopwatch":
        stopwatch = SimpleStopwatch()
        stopwatch.start()
        return stopwatch
    @staticmethod
    def synchronise_start_new(synchronise: IStopwatch) -> "SimpleStopwatch":
        stopwatch = SimpleStopwatch()
        stopwatch.synchronise_start(synchronise)
        return stopwatch
    
    @staticmethod
    def new_group(number: int) -> "tuple[SimpleStopwatch]":
        return tuple([SimpleStopwatch() for _ in range(number)])
    @staticmethod
    def start_new_group(number: int) -> "tuple[SimpleStopwatch]":
        stopwatches = tuple([SimpleStopwatch() for _ in range(number)])
        stopwatches[0].start()
        for i in range(1, number):
            stopwatches[i].synchronise_start(stopwatches[0])
        return stopwatches
    @staticmethod
    def synchronise_start_new_group(number: int, synchronise: "IStopwatch") -> "tuple[SimpleStopwatch]":
        return tuple([SimpleStopwatch.synchronise_start_new(synchronise) for _ in range(number)])

    def __init__(self):
        self.__running:   bool
        self.__lap_times: list[float]
        self.__stop_time: float|None

        self.reset()

    def reset(self) -> None:
        self.__running   = False
        self.__lap_times = []
        self.__stop_time = None

    def start(self) -> None:
        if self.__running:
            raise StopwatchStartedError("Attempted to restart stopwatch without first stopping or manually resetting.")
        self.reset()
        self.__running = True
        # Get the start time just before execution returns to the calling scope
        self.__lap_times.append(time.time())

    def synchronise_start(self, synchronise: IStopwatch) -> None:
        if self.__running:
            raise StopwatchStartedError("Attempted to restart stopwatch without first stopping or manually resetting.")
        self.reset()
        self.__running = True
        # Get the start time just before execution returns to the calling scope
        self.__lap_times.append(synchronise.get_start_time())

    def lap(self) -> float:
        # Ask for the time immediately after call
        t = time.time()
        # Now do validation
        if self.__stop_time is not None:
            raise StopwatchStoppedError("Unable to lap a stopped stopwatch.")
        elif not self.__running:
            raise StopwatchNotStartedError("Unable to lap a stopwatch that has not yet been started.")
        # Then do logic
        self.__lap_times.append(t)
        return t - self.__lap_times[-2]

    def stop(self) -> float:
        # Ask for the time immediately after call
        t = time.time()
        # Now do validation
        if self.__stop_time is not None:
            raise StopwatchStoppedError("Unable to stop an already stopped stopwatch.")
        elif not self.__running:
            raise StopwatchNotStartedError("Unable to stop a stopwatch that has not yet been started.")
        # Then do logic
        self.__running = False
        self.__lap_times.append(t)
        self.__stop_time = t
        return t - self.__lap_times[-2]
    
    def get_start_time(self) -> float:
        if not self.__running and self.__stop_time is None:
            raise StopwatchNotStartedError("Unable to get start time of a stopwatch that has not yet been started.")
        return self.__lap_times[0]
    
    def get_elapsed_time(self) -> float:
        t = time.time()
        if self.__running:
            return t - self.__lap_times[0]
        elif self.__stop_time is not None:
            return self.__stop_time - self.__lap_times[0]
        else:
            return 0.0
    
    def get_elapsed_time_lap(self) -> float:
        t = time.time()
        if self.__running:
            return t - self.__lap_times[-1]
        elif self.__stop_time is not None:
            return self.__stop_time - self.__lap_times[-1]
        else:
            return 0.0
    
    def get_elapsed_time_last_lap(self) -> float:
        if not self.started:
            raise StopwatchNotStartedError("Unable to get lap information from a stopwatch that has not yet been started.")
        if len(self.__lap_times) < 2:
            return 0.0
        else:
            return self.__lap_times[-1] - self.__lap_times[-2]

    def __str__(self) -> str:
        t = time.time()
        return str(t - self.__lap_times[-1])

    def __repr__(self) -> str:
        t = time.time()
        if self.__running:
            return f"SimpleStopwatch: {t - self.__lap_times[0]}"
        elif self.__stop_time is not None:
            return f"SimpleStopwatch: {self.__stop_time - self.__lap_times[0]} (stopped)"
        else:
            return "SimpleStopwatch: not yet started"
        
    def __float__(self):
        return self.get_elapsed_time()
        
    def __int__(self):
        return int(self.get_elapsed_time())

    @property
    def running(self) -> bool:
        return self.__running
    @property
    def started(self) -> bool:
        return self.__running or self.__stop_time is not None
    @property
    def stopped(self) -> bool:
        return self.__stop_time is not None

    @property
    def start_time(self) -> float|None:
        if not self.started:
            return None
        else:
            return self.__lap_times[0]
    @property
    def lap_times(self) -> tuple[float]:
        if not self.started:
            return tuple()
        elif not self.stopped:
            return tuple(self.__lap_times[1:])
        else:
            return tuple(self.__lap_times[1:-1])
    @property
    def stop_time(self) -> float|None:
        if not self.stopped:
            return None
        else:
            return self.__lap_times[-1]
