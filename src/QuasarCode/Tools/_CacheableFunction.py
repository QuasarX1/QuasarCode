from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Generic, TypeVar, ParamSpec, Concatenate, Iterable, TypeVarTuple, Callable
from numbers import Number, Real

import numpy as np
from scipy.stats import norm

from ..Tools._Struct import CacheableStruct
from ..Tools._autoproperty import AutoProperty_NonNullable

T = TypeVar("T", bound = "CacheableFunction")
P = ParamSpec("P")
R = TypeVar("R")

class CacheableFunction(CacheableStruct, Generic[P, R], ABC, Callable[P, R]):
    constants = AutoProperty_NonNullable[dict[str, Any]]() # P.kwargs
    def __init__(self, cacheable_attributes: tuple[str, ...]|None = None, **kwargs) -> None:
        super().__init__(
            cacheable_attributes = (*(cacheable_attributes if cacheable_attributes is not None else tuple()), "constants"),
            **kwargs
        )
    @classmethod
    def new(cls: type[T], **constants: P.kwargs) -> T:
        """
        Create a new instance of the function using the provided constants.
        """
        instance = cls()
        instance.constants = constants
        return instance
    def __call__(self, *args: P.args) -> R:
        return self.function(*args, **self.constants)
    @abstractmethod
    def function(self, *args: P.args, **kwargs: P.kwargs) -> R:
        """
        The functional form to be implemented by the subclass.
        """
        raise NotImplementedError("Subclasses must implement the 'function' method.")

class PolynomialFunction(CacheableFunction[[Real|int|float], Real|int|float]):
    @classmethod
    def new(cls, *constant_terms: Real|int|float) -> "PolynomialFunction": # type: ignore[override]
        """
        Create a new instance of the function using the provided constants.
        """
        return super().new(**{f"{i}": constant_terms[i] for i in range(len(constant_terms))})
    def function(self, x: Real|int|float, **constants: Real|int|float) -> Real|int|float:
        """
        Evaluate the polynomial function at a given point x using the provided constants.
        """
        number_of_terms = len(constants)
        return sum([x**(number_of_terms - 1 - i) * constants[f"{i}"] for i in range(number_of_terms)]) # type: ignore[return-value]

class LinearFunction(PolynomialFunction):
    @classmethod
    def new(cls, gradient: Real|int|float, intercept: Real|int|float) -> "LinearFunction": # type: ignore[override]
        """
        Create a new instance of the function using the provided constants.
        """
        return super().new(gradient, intercept) # type: ignore[return-value]

A = TypeVar("A", Real|int|float, np.ndarray[Any, np.dtype[np.integer|np.floating]])
class GaussianFunction(CacheableFunction[[A], A]):
    @classmethod
    def new(cls, mean: Real|int|float, standard_deviation: Real|int|float, height_multiplier: Real|int|float) -> "GaussianFunction": # type: ignore[override]
        """
        Create a new instance of the function using the provided constants.
        """
        return super().new(mean = mean, standard_deviation = standard_deviation, height_multiplier = height_multiplier)
    def function(self, x: A, mean: Real|int|float, standard_deviation: Real|int|float, height_multiplier: Real|int|float) -> A:
        """
        Evaluate the Gaussian function at a given point x using the provided constants.
        """
        return norm(loc = mean, scale = standard_deviation).pdf(x) * height_multiplier
