import unittest
from QuasarCode.Games.Spinners import Spinner, ISpinner

class Test_Games(unittest.TestCase):
    def test_Spinners(self):
        spinner = Spinner(["Red", "Yellow", "Blue", "Green"])

        for i in range(100):
            print(spinner.Spin())

if __name__ == '__main__':
    unittest.main()
