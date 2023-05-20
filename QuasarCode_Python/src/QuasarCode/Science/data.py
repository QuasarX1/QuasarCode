import numpy as np
from decimal import Decimal

#def consistancyTest(a, b, aErr, bErr = 0):
#    """
#    Performs a consistancy test to determine the integer number of sigma within which \
#two values lie relitive to each other and their errors.
#    """
#    sigma = 0
#    consistant = False
#    while not consistant:
#        sigma += 1
#        checkValue = np.abs(b - a) - sigma * np.sqrt(bErr**2 + aErr**2)
#        #print(checkValue)
#        consistant = checkValue <= 0
#    return sigma

def consistancy_test(a, b, aErr, bErr = 0):#TODO: fully test this aproach
    """
    Performs a consistancy test to determine the integer number of sigma within which \
two values lie relitive to each other and their errors.
    """
    return int(np.ceil(np.abs(b - a) / np.sqrt(bErr**2 + aErr**2)))

def is_consistant(a, b, aErr, bErr, sigma):
    """
    Convenience method for checking if two values are consistant within a given sigma value
    """
    return consistancy_test(a, b, aErr, bErr) <= sigma

def error_string(value: float, error: float, units: str = None, normalise: bool = True):#TODO: sort normalisation for value
    """
    Formats a number and its error as a single string
    """
    if normalise:#TODO: this dosn't normalise the value it just does the error
        error = sig_fig(error, 1)

    if units is None:
        return "{} \u00B1 {}".format(value, float(error))
    else:
        return "({} \u00B1 {}) {}".format(value, error, units)

def sig_fig(num: Decimal, digits: int):
    """
    Rounds a number to a set number of significant figures
    """
    num = Decimal(num)

    if np.abs(num) >= 1:
        power = 0
        while np.abs(num) > 10:
            power += 1
            num /= 10

    else:
        power = 0
        while np.abs(num) < 1:
            power -= 1
            num *= 10

    # Return number to 10^digits * 10^0
    num = true_round(num * 10**(Decimal(digits - 1)), 0) * 10**-(Decimal(digits - 1)) * 10**Decimal(power)

    return num

def standard_form(num: Decimal):
    """
    Determines the value and power for the standard form representation of a number
    """
    num = Decimal(num)
    power = 0

    if num >= 1:
        new_num = None
        new_power = None
        while num > 1:
            new_num = num
            new_power = power

            new_power += 1
            new_num /= 10

            if new_num < 1:
                break
            else:
                num = new_num
                power = new_power

    else:
        while num < 1:
            power -= 1
            num *= 10
            if num > 1:
                break

    return num, power

def standard_form_string(num: Decimal, numberSigFig = None, latex = False):
    """
    Determines the standard form representation of a number and represents it as a string
    """
    number, power = standard_form(num)

    template = "${}\\times10^{{{}}}$" if latex else "{} * 10^{}"

    return template.format(float(sig_fig(number, numberSigFig) if numberSigFig is not None else number), power) if power != 0 else str(float(sig_fig(number, numberSigFig) if numberSigFig is not None else number))

def standard_form_string_if_nessessary(num: Decimal, numberSigFig = None):
    if np.abs(num) >= 9999 or np.abs(num) < 0.001:
        return standard_form_string(num, numberSigFig)
    else:
        return str(float(sig_fig(num, numberSigFig) if numberSigFig is not None else num))

def true_round(number: Decimal, nDigits: int = None):
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