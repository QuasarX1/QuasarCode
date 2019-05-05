import unittest
from QuasarCode.Games.Spinners import Spinner, ISpinner
from QuasarCode.Games.Dice import NDice, IDice

class Test_Games(unittest.TestCase):
    def test_Spinners(self):
        spinner = Spinner(["Red", "Yellow", "Blue", "Green"])

        for i in range(100):
            print(spinner.Spin())

    def test_Dice(self):
        dice = NDice(6)

        for i in range(100):
            print(dice.Roll())

    self.assertEqual(len(NDice.MultipleDice([6, 6])), 2, "Wrong number of dice produced by MultipleDice.")
    self.assertEqual(len(NDice.MultipleDice([6], noOfDice = 2)), 2, "Wrong number of dice produced by MultipleDice.")

if __name__ == '__main__':
    unittest.main()
