import pytest
import sys

from QuasarCode.IO.Text.console import print_info, print_verbose_info, print_debug
from QuasarCode.Tools import ScriptWrapper

class TestClass_Tools(object):
    def test_ScriptWrapper(self):
        assert True
        def testing_function():
            print_info("SUCCESS")
            print_verbose_info("FAIL")
            print_debug("SUCCESS")
            assert True

        sys.argv.append("-d")
        wrapper = ScriptWrapper("filename.py", "author", "0.0.0", "edit_date", "description", [], [], [], [])
        
        wrapper.run(testing_function)
