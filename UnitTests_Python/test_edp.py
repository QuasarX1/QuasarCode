import unittest
import QuasarCode.edp as edp

class Test_edp(unittest.TestCase):
    def standalone_method(self):
        def testMethod():
            return 0

        event = edp.Event()
        event += testMethod

        self.assertEqual(event.run()[0], 0, "Method should have returned 0")

if __name__ == '__main__':
    unittest.main()
