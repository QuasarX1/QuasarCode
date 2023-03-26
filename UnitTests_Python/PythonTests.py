import unittest

#import edp
import games
import q_io
import mpi
import science
import tools







import QuasarCode.edp as edp

class Test_edp(unittest.TestCase):
    #def test_testNameHere(self):
    #    self.fail("Not implemented")

    def test_standaloneMethod(self):
        def testMethod():
            return 0

        event = edp.Event()
        event += testMethod

        self.assertEqual(event.run()[0], 0, "Method should have returned 0")

if __name__ == '__main__':
    unittest.main()