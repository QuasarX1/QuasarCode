from copy import copy
import pytest

from QuasarCode.IO.Text.console import pause
from QuasarCode.IO.Configurations import PropertiesConfig, JsonConfig, YamlConfig

class TestClass_IO_Text(object):
    def test_Text(self):
        assert False
        self.fail("Not Implemented - Sort Input")#TODO: sort inputs
        
        try:
            pause()
            pause(exit = True)
            self.assertTrue(True)#TODO: is this needed for success to be registered?
        except:
            self.fail("The output must be checked.")

class TestClass_IO_Configurations(object):
    def test_a_test(self):
        d = Ex()
        d.add_item("inner", Ex())
        d.inner.add_item("value", "Hello World!")
        print(d.inner.value)
        d.inner.value = 1
        print(d.inner.value)
        
        d.writable = False

        d.inner.value = 2
        print(d.inner.value)
        return






    def test_ConfigBase(self):
        cfg = PropertiesConfig.from_file("testconfig.properties")
        print(cfg)

        assert cfg.writable == False
        print(cfg.value1)
        assert cfg.value1 == "a string of text"
        print(cfg["value1"])
        assert cfg["value1"] == "a string of text"
        cfg.value1 = 0
        print(cfg.value1)
        assert cfg.value1 == "a string of text", "Value was changed inside non-writable object."

    def test_ConfigBase_writable(self):
        cfg = PropertiesConfig.from_file("testconfig.properties", writable = True)
        print(cfg)

        assert cfg.writable == True
        print(cfg.value1)
        assert cfg.value1 == "a string of text"
        print(cfg["value1"])
        assert cfg["value1"] == "a string of text"
        cfg.value1 = 0
        print(cfg.value1)
        assert cfg.value1 == 0

    def test_PropertiesConfig(self):
        cfg = PropertiesConfig.from_file("testconfig.properties")
        print(cfg)

        print(cfg.value1)
        assert cfg.value1 == "a string of text"
        print(cfg.value2)
        assert cfg.value2 == "100"
        print(cfg.value3)
        assert cfg.value3 == "more text"

    def test_JsonConfig(self):
        cfg = JsonConfig.from_file("testconfig.json", True, -1)
        print(cfg)

        print(cfg.value1)
        assert cfg.value1 == "a string of text"
        print(cfg.value2)
        assert cfg.value2 == 100
        print(cfg.value3)
        assert cfg.value3 == "more text"

        print(cfg.value4)
        print(cfg.value4.sub_value1)
        assert cfg.value4.sub_value1 == "a nested value"
        print(cfg.value4.sub_value2)
        assert cfg.value4.sub_value2 == 2.8

    def test_YamlConfig(self):
        cfg = YamlConfig.from_file("testconfig.yaml", True, True, -1)
        print(cfg)

        print(cfg.value1)
        assert cfg.value1 == "a string of text"
        print(cfg.value2)
        assert cfg.value2 == 100
        print(cfg.value3)
        assert cfg.value3 == "more text"

        print(cfg.value4)
        print(cfg.value4.sub_value1)
        assert cfg.value4.sub_value1 == "a nested value"
        print(cfg.value4.sub_value2)
        assert cfg.value4.sub_value2 == 2.8

        print(cfg.value4.value4_1.sub_sub_value1)
        assert cfg.value4.value4_1.sub_sub_value1 == "double nest test"





class Ex(object):
    def __init__(self):
        self.__data = {}
        self.writable = True

    def add_item(self, key: str, value):
        self.__data[key] = value

    def __getitem__(self, *keys):
        if keys[0] in self.__data:
            value = self.__data[keys[0]]
            if len(keys) > 1:
                if isinstance(value, Ex):
                    return value[keys[1:]] if self.writable else copy(value[keys[1:]])
                else:
                    raise TypeError(f"Value of {keys[0]} is a root node and cannot be automatically indexed further.")
            else:
                return value if self.writable else copy(value)
        else:
            raise AttributeError(f"{keys[0]} is not a valid attribute or config name.")

    def __getattr__(self, key: str):
        return self[key]

    def __setattr__(self, key: str, value):
        super().__setattr__(key, value)
        #if key != "_Mapping__data" and key in self.__data:
        #    self[key] = value