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
        print(cfg.value4.sub_value2_longer)
        assert cfg.value4.sub_value2_longer == 2.8

        print(cfg.value4.value4_1.sub_sub_value1)
        assert cfg.value4.value4_1.sub_sub_value1 == "double nest test"
    
    def test_YamlConfigDisplay(self):
        cfg = YamlConfig.from_file("testconfig_2.yaml", True, True, -1)
        print(cfg)
        no_indent = ""
        indent_spaces = "    "
        assert cfg.__str__() == f"""\
files:
{indent_spaces}
    input:
        simulation_snapshots = "filepath"
        snapshot_file        = "file.txt"
{indent_spaces}{indent_spaces}
        zero_metalicity_filters:
{indent_spaces}{indent_spaces}{indent_spaces}
            high_mass_halos:
                field_name    = "gas.last_halo_masses"
                min           = None
                include_lower = True
                max           = None
                include_upper = True
{indent_spaces}
    output:
{indent_spaces}{indent_spaces}
        raw_data:
            prefix                         = "SpecWizard_data"
            sightline_locations_prefix     = "rays"
            sightline_velocity_info_prefix = "ray_velocity_information"
            optical_depth_prefix           = "optical_depth"
{indent_spaces}{indent_spaces}
        hdf5:
            file_name = "data"
{indent_spaces}{indent_spaces}
        image:
            file_prefix = "SpecWizard_pixel_optical_depths"
            file_type   = "png"
{indent_spaces}{indent_spaces}
        graph:
            file_name = "SpecWizard_ray_absorbtion"
            file_type = "png"
{no_indent}
ray_properties:
    axis                       = "z"
    spacing_mpc                = 1.0
    depth_fraction_start       = 0.0
    depth_fraction_end         = 1.0
    velocity_element_depth_kms = 1.0
{no_indent}
elements:
{indent_spaces}
    hydrogen_1:
        element_name = "Hydrogen"
        ion_symbol   = "H I"
{indent_spaces}
    carbon_3:
        element_name = "Carbon"
        ion_symbol   = "C III"
{indent_spaces}
    carbon_4:
        element_name = "Carbon"
        ion_symbol   = "C IV"
{indent_spaces}
    oxygen_6:
        element_name = "Oxygen"
        ion_symbol   = "O VI"
{indent_spaces}
    silicon_3:
        element_name = "Silicon"
        ion_symbol   = "Si III"
{indent_spaces}
    silicon_4:
        element_name = "Silicon"
        ion_symbol   = "Si IV"
{indent_spaces}
    magnesium:
        element_name = "Magnesium"
        ion_symbol   = "MgII"
{no_indent}
parallelization:
    run_parallel = False
    cpus         = 64
"""





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