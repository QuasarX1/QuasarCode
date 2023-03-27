import unittest

import QuasarCode.edp as edp

class TestClass_edp(object):

    def test_standaloneMethod(self):
        def testMethod():
            return 0

        event = edp.Event()
        event += testMethod

        assert event.run()[0] == 0
