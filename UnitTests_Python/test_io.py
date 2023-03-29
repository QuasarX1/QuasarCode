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
    def test_ConfigBase(self):
        cfg = PropertiesConfig.from_file("testconfig.properties")
        assert cfg.writable == False
        print(cfg.value1)
        assert cfg.value1 == "a string of text"
        print(cfg["value1"])
        assert cfg["value1"] == "a string of text"
        cfg.value1 = 0
        print(cfg.value1)
        assert cfg.value1 == "a string of text"

    def test_ConfigBase_writable(self):
        cfg = PropertiesConfig.from_file("testconfig.properties", writable = True)
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
        print(cfg.value1)
        assert cfg.value1 == "a string of text"
        print(cfg.value2)
        assert cfg.value2 == "100"
        print(cfg.value3)
        assert cfg.value3 == "more text"

    def test_JsonConfig(self):
        cfg = JsonConfig.from_file("testconfig.json", True, -1)
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
