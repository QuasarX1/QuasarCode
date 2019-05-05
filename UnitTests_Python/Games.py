import unittest
from QuasarCode.Games.Spinners import Spinner, ISpinner
from QuasarCode.Games.Dice import NDice, IDice, Dice6, Dice8, Dice12

class Test_Games(unittest.TestCase):
    def test_Spinners(self):
        spinner = Spinner(["Red", "Yellow", "Blue", "Green"])

        for i in range(100):
            print(spinner.Spin())

    def test_Dice(self):
        dice = NDice(6)

        for i in range(100):
            print(dice.Roll())
        print()

        self.assertEqual(len(NDice.MultipleDice([6, 6])), 2, "Wrong number of dice produced by MultipleDice.")
        self.assertEqual(len(NDice.MultipleDice([6], noOfDice = 2)), 2, "Wrong number of dice produced by MultipleDice.")

        dice6 = Dice6()
        dice8 = Dice8()
        dice12 = Dice12()

        print(dice6.Roll())

        print(dice8.Roll())

        print(dice12.Roll())

if __name__ == '__main__':
    unittest.main()
