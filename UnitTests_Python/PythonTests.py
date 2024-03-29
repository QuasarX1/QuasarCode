import unittest

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

    def test_Cards(self):
        pass#TODO:



from QuasarCode.IO.Text.console import pause

class Test_IO(unittest.TestCase):
    def test_Text(self):
        self.fail("Not Implemented - Sort Input")#TODO: sort inputs
        
        try:
            pause()
            pause(exit = True)
            self.assertTrue(True)#TODO: is this needed for success to be registered?
        except:
            self.fail("The output must be checked.")



class Test_Maths(unittest.TestCase):
    pass#TODO:



from decimal import Decimal
##from QuasarCode.Science.graph import Figure
##from QuasarCode.Science.data import errorString, sigFig
from QuasarCode.Science import Figure, errorString, sigFig

class Test_Science(unittest.TestCase):
    def test_sigFig(self):
        self.assertEqual(Decimal(436784329.828746), sigFig(436784329.828746, 15), "Rounding to 15 sig fig failed.")
        self.assertEqual(Decimal(436784329.82874), sigFig(436784329.828746, 14), "Rounding to 14 sig fig failed.")
        self.assertEqual(Decimal(436784329.8287), sigFig(436784329.828746, 13), "Rounding to 13 sig fig failed.")
        self.assertEqual(Decimal(436784329.828), sigFig(436784329.828746, 12), "Rounding to 12 sig fig failed.")
        self.assertEqual(Decimal(436784329.82), sigFig(436784329.828746, 11), "Rounding to 11 sig fig failed.")
        self.assertEqual(Decimal(436784329.8), sigFig(436784329.828746, 10), "Rounding to 10 sig fig failed.")
        self.assertEqual(Decimal(436784329), sigFig(436784329.828746, 9), "Rounding to 9 sig fig failed.")
        self.assertEqual(Decimal(436784320), sigFig(436784329.828746, 8), "Rounding to 8 sig fig failed.")
        self.assertEqual(Decimal(436784300), sigFig(436784329.828746, 7), "Rounding to 7 sig fig failed.")
        self.assertEqual(Decimal(436784000), sigFig(436784329.828746, 6), "Rounding to 6 sig fig failed.")
        self.assertEqual(Decimal(436780000), sigFig(436784329.828746, 5), "Rounding to 5 sig fig failed.")
        self.assertEqual(Decimal(436700000), sigFig(436784329.828746, 4), "Rounding to 4 sig fig failed.")
        self.assertEqual(Decimal(436000000), sigFig(436784329.828746, 3), "Rounding to 3 sig fig failed.")
        self.assertEqual(Decimal(430000000), sigFig(436784329.828746, 2), "Rounding to 2 sig fig failed.")
        self.assertEqual(Decimal(400000000), sigFig(436784329.828746, 1), "Rounding to 1 sig fig failed.")

    def test_standardForm(self):
        pass#TODO:

    def test_trueRound(self):
        pass#TODO:

    def test_consistancyTest(self):
        pass#TODO:

    def test_GraphAndErrorString(self):
        x = np.array([1.3, 2.1, 2.8, 3.9, 5.2])
        y = np.array([3.4, 4.6, 7.2, 8.5, 11.2])

        dx = np.array([1, 1, 1, 1, 1])
        dy = np.array([1, 1, 1, 1, 1])

        testGraph = Figure(x, y, dx, dy, size = None, title = "A test graph", xLabel = "X-Axis", yLabel = "Y-Axis", saveName = "testingFigure.png")
        testGraph.createFitLine()
        testGraph.plot()
        testGraph.save()
        #testGraph.show()# TODO: window hangs

        m = testGraph.fit.fitVariables["m"]
        c = testGraph.fit.fitVariables["c"]

        self.assertEqual("2.0435922040733323", str(m[0]), "The value calculated for the gradient does not match the expected value.")
        self.assertEqual("0.7481821730455976", str(m[1]), "The error calculated for the gradient does not match the expected value.")
        self.assertEqual("0.7266078556762237", str(c[0]), "The value calculated for the intercept does not match the expected value.")
        self.assertEqual("2.505349774682801", str(c[1]), "The error calculated for the intercept does not match the expected value.")

        self.assertEqual("2.0435922040733323 ± 0.7", errorString(m[0], m[1]), "The normalised value and error calculated for the gradient does not match the expected value.")
        self.assertEqual("0.7266078556762237 ± 3.0", errorString(c[0], c[1]), "The normalised value and error calculated for the intercept does not match the expected value.")



class Test_Tools(unittest.TestCase):
    pass#TODO:
        
        
if __name__ == '__main__':
    unittest.main()