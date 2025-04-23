from typing import Any

import numpy as np

from ..IO.Caching import Cacheable

class Bins(Cacheable):
    def __init__(self, bin_edges: np.ndarray[tuple[int], np.dtype[np.floating]]) -> None:
        self.__bin_edges: np.ndarray[tuple[int], np.dtype[np.floating]] = bin_edges
        self.__bin_centres: np.ndarray[tuple[int], np.dtype[np.floating]] = (self.__bin_edges[:-1] + self.__bin_edges[1:]) / 2
        self.__bin_widths: np.ndarray[tuple[int], np.dtype[np.floating]] = self.__bin_edges[1:] - self.__bin_edges[:-1]

    def __len__(self) -> int:
        return len(self.__bin_centres)
    
    @property
    def edges(self) -> np.ndarray[tuple[int], np.dtype[np.floating]]:
        """
        Get the bin edges.

        Returns:
            np.ndarray[tuple[int], np.dtype[np.floating]] -> The bin edges.
        """
        return self.__bin_edges
    
    @property
    def centres(self) -> np.ndarray[tuple[int], np.dtype[np.floating]]:
        """
        Get the bin centres.

        Returns:
            np.ndarray[tuple[int], np.dtype[np.floating]] -> The bin centres.
        """
        return self.__bin_centres
    
    @property
    def widths(self) -> np.ndarray[tuple[int], np.dtype[np.floating]]:
        """
        Get the bin widths.

        Returns:
            np.ndarray[tuple[int], np.dtype[np.floating]] -> The bin widths.
        """
        return self.__bin_widths
    
    @classmethod
    def __from_cache_data__(cls, data: dict[str, Any]) -> "Bins":
        """
        Load the object from a cache target.

        Parameters:
            dict[str, Any] data:
                The data to load the object from.
        """
        return Bins(data["bin_edges"])

    def __get_cache_data__(self) -> dict[str, Any]:
        """
        Get the data to be cached.

        Returns:
            dict[str, Any] -> The data to be cached.
        """
        return { "bin_edges": self.__bin_edges }
    
    @staticmethod
    def make_linear_bins(min: float, max: float, number: int, centred_limits: bool = False) -> "Bins":
        """
        Create a set of linear bins.

        Parameters:
            min (float): The minimum value of the bins.
            max (float): The maximum value of the bins.
            number (int): The number of bins to create.
            centred_limits (bool): Whether the limits are for the centre of the outermost bins or the outside edges (default).

        Returns:
            Bins -> The linear bins.
        """
        bin_edges: np.ndarray[tuple[int], np.dtype[np.floating]] = np.linspace(min, max, number + 1) if not centred_limits else np.linspace(min - ((max - min) / (2 * number)), max + ((max - min) / (2 * number)), number + 1)
        return Bins(bin_edges)

    @staticmethod
    def make_logarithmic_bins(min: float, max: float, number: int, centred_limits: bool = False) -> "Bins":
        """
        Create a set of logarithmic bins.

        Parameters:
            min (float): The minimum value of the bins.
            max (float): The maximum value of the bins.
            number (int): The number of bins to create.
            centred_limits (bool): Whether the limits are for the centre of the outermost bins or the outside edges (default).

        Returns:
            Bins -> The logarithmic bins.
        """
        bin_edges: np.ndarray[tuple[int], np.dtype[np.floating]] = np.logspace(np.log10(min), np.log10(max), number + 1) if not centred_limits else np.logspace(np.log10(min - ((max - min) / (2 * number))), np.log10(max + ((max - min) / (2 * number))), number + 1)
        return Bins(bin_edges)
