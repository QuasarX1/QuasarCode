import re
from QuasarCode.Tools.networking import URI, URL

# No "isBool" exists as any object can be converted to a boolean

def isCharacter(testCase):
    return isString(testCase) and len(str(testCase)) == 1

def isString(testCase):
    try:
        str(testCase)
        return True
    except:
        return False

def isAlpha(testCase):
    return isString(testCase) and re.match("^[a-zA-Z_']+$", testCase) is not None

def isInt(testCase):
    try:
        int(testCase)
    except:
        return False

    return re.match("^[0-9\-]+$", str(testCase)) is not None

def isFloat(testCase):
    try:
        float(testCase)
    except:
        return False

    return re.match("^[0-9\.\-]+$", str(testCase)) is not None

def inRange(testCase, lower, upper, inside = True):
    if upper == lower:
        raise ValueError("The arguments for paramiters min and max are the same. They must be different as min is inclusive and max is exclusive.")

    return (lower <= testCase) and (testCase < upper) == inside

def isEven(testCase):
    return float(testCase // 2) == float(testCase / 2)

def isOdd(testCase):
    return not isEven(testCase)

def isFactor(testCase, value):
    return isInt(testCase) and isInt(value) and testCase != 0 and isInt(value / testCase)

def isMultiple(testCase, value):
    return isInt(testCase) and isInt(value) and value != 0 and isInt(testCase / value)

def isEmail(testCase):
    return isString(testCase) and re.match("^(mailto:)?[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)?@[a-zA-Z]+(\.[a-zA-Z]+)+$", str(testCase)) is not None

def isURL(testCase):#TODO: some avalable characters still missing
    return isURI(testCase) and re.match("^https?:", str(testCase)) is not None

def isURI(testCase):
    #                                        |scheme              |authority                                                                                                              |path                                               |query                                                               |fragment
    return isString(testCase) and re.match("^[a-z][a-z1-9\+\.\-]*:(//([a-zA-Z1-9%]+(\.[a-zA-Z1-9%]+)*(:[a-zA-Z1-9%]+)?@)?(([a-zA-Z1-9%]+(\.[a-zA-Z1-9%]+)+)|(\[[a-z1-9]{4}(:[a-z1-9]{4}){7}\]))?(:[0-9]+)?)?(/[a-zA-Z0-9%]+(/[a-zA-Z0-9%]+)+(/|\.[a-zA-Z0-9%]+)?)(\?[a-zA-Z0-9%]+=[a-zA-Z0-9%]+((\&|;)[a-zA-Z0-9%]+=[a-zA-Z0-9%]+)*)?(#[a-zA-Z1-9%]+)?$", str(testCase)) is not None
    #                                                                |userinfo                         |host                                                                  |port

def isURIScheme(testCase):
    isString(testCase) and re.match("^[a-z][a-z1-9\+\.\-]*:", str(testCase)) is not None

def isURIAuthority(testCase):
    pass

def isURIPath(testCase):
    pass

def isURIQuery(testCase):
    pass

def isURIFragment(testCase):
    pass