import unittest
import QuasarCode.Maths as Maths
import QuasarCode.Maths.stringMaths as stringMaths

class Test_stringMaths(unittest.TestCase):
    def best_case(self):
        equ = stringMaths.MathsParse("1 + 2 - 3 * 4 / -6")
        self.assertEqual(equ.run(), 1.5)

if __name__ == '__main__':
    unittest.main()
