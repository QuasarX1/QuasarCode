import numpy as np
from typing import Union, List, Tuple

from QuasarCode.Tools import AutoProperty, TypedAutoProperty, TypeCastAutoProperty, TypeShield, NestedTypeShield, Cast, NestedCast, cast_ndarray_float64

class Test_AutoProperty(object):
    def test_standard(self):

        class T(object):
            a = AutoProperty()
            b = AutoProperty(allow_uninitialised = True)

        t = T()

        try:
            _ = t.a
            raise AssertionError("Attempt to access uninitialised property succeeded.")
        except ValueError:
            pass

        t.a = 1

        assert t.a == 1, "Failed to read expected value of property."
        assert t.b is None, "Failed to retrive uninitialised value of None."

        t.b = 2
        assert t.b == 2, "Failed to read expected value of property."

        del t.a
        del t.b

        try:
            _ = t.a
            raise AssertionError("Attempt to access uninitialised (deleted) property succeeded.")
        except ValueError:
            pass
        assert t.b is None, "Failed to retrive uninitialised (deleted) value of None."

        t.a = 10
        t.b = 20

        assert t.a == 10, "Failed to read expected value of property (re-initialised after deletion)."
        assert t.b == 20, "Failed to read expected value of property (re-initialised after deletion)."

    def test_type_check(self):

        class T(object):
            a = TypedAutoProperty[int](TypeShield[int](int, np.int8, np.int16, np.int32, np.int64))
            b = TypedAutoProperty[Tuple[List[Union[int, float, bool]]]](NestedTypeShield[Tuple[List[Union[int, float, bool]]]]([tuple], [list], [int, float, bool]))

        t = T()

        #TODO: move test to TypeShield tests!
        assert str(NestedTypeShield[Tuple[List[Union[int, float, bool]]]]([tuple], [list], [int, float, bool])) == "TypeShield(tuple -> list -> {int, float, bool})", "Failed to generate correct type string."

        try:
            _ = t.a
            raise AssertionError("Attempt to access uninitialised property succeeded.")
        except ValueError:
            pass

        try:
            _ = t.b
            raise AssertionError("Attempt to access uninitialised property succeeded.")
        except ValueError:
            pass

        t.a = 1
        t.b = ([1, 2.5, True], [False, 1.8, -100])

        assert t.a == 1, "Failed to read expected value of property."
        assert t.b == ([1, 2.5, True], [False, 1.8, -100]), "Failed to read expected value of property."

        try:
            t.a = "2"
            raise AssertionError("Attempt to access uninitialised property succeeded.")
        except TypeError:
            pass

        try:
            t.b = (["1", 2.5, True], [False, 1.8, -100])
            raise AssertionError("Attempt to assign value with inappropriate left hand branch type succeeded.")
        except TypeError:
            pass

        assert t.a == 1, "Failed to read expected value of property."
        assert t.b == ([1, 2.5, True], [False, 1.8, -100]), "Failed to read expected value of property."

        try:
            t.b = ([1, "2.5", True], "[False, 1.8, -100]")
        except TypeError:
            raise AssertionError("Attempt to assign value with inappropriate type but valid left hand branch failed.\nTHIS IS UNEXPECTED BEHAVIOUR AS ONLY LHS IS CHECKED!!!")

        
        assert t.b == ([1, "2.5", True], "[False, 1.8, -100]"), "Failed to read expected value of property."

    def test_type_cast(self):

        class T(object):
            a = TypeCastAutoProperty[np.ndarray](cast_ndarray_float64)
            b = TypeCastAutoProperty[str](Cast[str](str, nullable = True))
            c = TypeCastAutoProperty[str](NestedCast[List[Tuple[float, ...]]](list, tuple, float))
            d = TypeCastAutoProperty[str](NestedCast[List[np.ndarray]](list, cast_ndarray_float64))
            e = TypeCastAutoProperty[str](NestedCast[np.ndarray](cast_ndarray_float64))

        t = T()

        try:
            _ = t.a
            raise AssertionError("Attempt to access uninitialised property succeeded.")
        except ValueError:
            pass

        try:
            _ = t.c
            raise AssertionError("Attempt to access uninitialised property succeeded.")
        except ValueError:
            pass

        t.a = [[1, 2, 3], [4, 5, 6]]
        t.c = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype = int)
        t.d = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        t.e = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        assert (t.a == np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype = np.float64)).all(), "Failed to read expected value of property."
        assert t.b is None, "Failed to retrive uninitialised value of None."
        assert t.c == [(1.0, 2.0, 3.0),
                       (4.0, 5.0, 6.0),
                       (7.0, 8.0, 9.0)], "Failed to read expected value of property."
        assert (t.d[0] == np.array([1, 2, 3], dtype = np.float64)).all(), "Failed to read expected value of property."
        assert (t.d[1] == np.array([4, 5, 6], dtype = np.float64)).all(), "Failed to read expected value of property."
        assert (t.d[2] == np.array([7, 8, 9], dtype = np.float64)).all(), "Failed to read expected value of property."
        assert isinstance(t.d, list)
        assert (t.e == np.array([[1, 2, 3],
                                [4, 5, 6],
                                [7, 8, 9]], dtype = np.float64)).all(), "Failed to read expected value of property."

        t.b = 2
        assert t.b == "2", "Failed to read expected value of property."
