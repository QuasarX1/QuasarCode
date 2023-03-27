import pytest

from QuasarCode.IO.Text.console import pause

class TestClass_IO(object):
    def test_Text(self):
        assert False
        self.fail("Not Implemented - Sort Input")#TODO: sort inputs
        
        try:
            pause()
            pause(exit = True)
            self.assertTrue(True)#TODO: is this needed for success to be registered?
        except:
            self.fail("The output must be checked.")
