import numpy as np
from decimal import Decimal

def consistancyTest(a, b, aErr, bErr = 0):
    """
    Performs a consistancy test to determine the integer number of sigma within which \
two values lie relitive to each other and their errors.
    """
    sigma = 0
    consistant = False
    while not consistant:
        sigma += 1
        checkValue = np.abs(b - a) - sigma * np.sqrt(bErr**2 + aErr**2)
        #print(checkValue)
        consistant = checkValue <= 0
    return sigma

def errorString(value: float, error: float, units: str = None, normalise: bool = True):#TODO: sort normalisation for value
    """
    Formats a number and its error as a single string
    """
    if normalise:
        error = sigFig(error, 1)

    if units is None:
        return "{} \u00B1 {}".format(value, float(error))
    else:
        return "({} \u00B1 {}) {}".format(value, error, units)

def sigFig(num: Decimal, digits: int):
    """
    Rounds a number to a set number of significant figures
    """
    num = Decimal(num)

    if num >= 1:
        power = 0
        while num > 10:
            power += 1
            num /= 10

    else:
        power = 0
        while num < 1:
            power -= 1
            num *= 10

    # Return number to 10^digits * 10^0
    num = trueRound(num * 10**(Decimal(digits - 1)), 0) * 10**-(Decimal(digits - 1)) * 10**Decimal(power)

    return num

def standardForm(num: Decimal):
    """
    Determines the value and power for the standard form representation of a number
    """
    num = Decimal(num)

    if num >= 1:
        power = 0
        while num > 1:
            power += 1
            num /= 10

    else:
        power = 0
        while num < 1:
            power -= 1
            num *= 10

    return num, power

def trueRound(number: Decimal, nDigits: int = None):
    """
    Rounds a number according to common rounding principles.
    i.e. flaw if next digit less than 5 or celing if more than or equal to 5
    """
    number = Decimal(number)

    if nDigits is None:
        nDigits = 0

    normal = number * 10**nDigits

    rest = normal - int(normal)

    if rest >= 0.5:
        return (normal - rest + 1) * 10**-nDigits
    else:
        return (normal - rest) * 10**-nDigits