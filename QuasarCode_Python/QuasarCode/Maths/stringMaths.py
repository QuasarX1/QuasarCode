def parseTokens(string: str):
    elements = string.split(" ")
    updatedElements = [elements[0]]
    for i in range(1, len(elements)):
        if elements[i][-1].isalnum() and elements[i - 1][-1].isalnum():
            updatedElements.append("*")
        updatedElements.append(elements[i])
        
    tokens = []
    for item in updatedElements:
        if len(item) > 1:
            # Keep numbers together
            if item.isnumeric():
                tokens.append(item)

            # Split letters out with a * between
            elif item.isalpha():
                tokens.append(item[0])
                for i in range(1, len(item)):
                    tokens.append("*")
                    tokens.append(letter)

            # If the element isn't purely alpha or numeric but is alphanumeric (e.g. 2a)
            elif not item.isalpha() and not item.isnumeric():
                newToken = ""
                for character in item:
                    if newToken == "":
                        newToken += character

                    elif newToken[-1].isalpha() and character.isnumeric() \
                    or newToken[-1].isnumeric() and character.isalpha() \
                    or newToken[-1].isalpha() and character.isalpha():
                        tokens.append(newToken)
                        tokens.append("*")
                        newToken = character

                    elif newToken[-1].isalnum() and not character.isalnum() \
                    or not newToken[-1].isalnum() and character.isalnum():
                        tokens.append(newToken)
                        newToken = character

                    else:
                        newToken += character

                tokens.append(newToken)


            else:# Contains symbols
                newToken = ""
                for character in item:
                    if newToken == "":
                        newToken += character

                    else:
                        if newToken[-1].isnumeric() and character.isnumeric() \
                        or newToken[-1].isalpha() and character.isalpha() \
                        or not newToken[-1].isalnum() and not character.isalnum():
                            newToken += character

                        else:
                            tokens.append(newToken)
                            newToken = character

                tokens.append(newToken)

        else:
            tokens.append(item)

    return tokens

def findVariables(tokens: list):
    variables = []
    for token in tokens:
        if token.isalpha() and token not in variables:
            variables.append(token)

    return variables

def checkValid(tokens: list):
    if (not tokens[0].isalnum() and tokens[0] != "-") or (not tokens[-1].isalnum()):
        return False
    
    lastWasAlnum = True
    for i in range(1, len(tokens)):
        if lastWasAlnum == tokens[i].isalnum():
            return False
        else:
            lastWasAlnum = not lastWasAlnum

    return True

def runMaths(string: list, variables: dict = {}):
    local = {"result": None}
    exec("result = " + string, variables, local)
    return local["result"]

def solveMaths(tokens: list, variables: dict = {}):
    pass

def intergrate(string: str, wrt: str = "x", fromValue = None, toValue = None):
    sections = string.split(["(", ")"])
    containsVariable = [section.contains(wrt) for section in sections]
    sections = [parseTokens(section) for section in sections]

    resultSections = []
    for i in range(len(sections)):
        if containsVariable[i]:
            pass

        else:
            resultSections.append(sections[i] + wrt)

    if fromValue == None and toValue == None:
        return "" + "+c"

    else:
        return ""

def differentiate(string: str, wrt: str = "x"):
    sections = string.split(["(", ")"])
    containsVariable = [section.contains(wrt) for section in sections]
    sections = [parseTokens(section) for section in sections]

    resultSections = []
    for i in range(len(sections)):
        if containsVariable[i]:
            pass

        else:
            resultSections.append("0")

    return ""

class MathsParse(object):
    def __init__(self, string, variables = {}):
        self.tokens = parseTokens(string)

        self.variables = variables
        for var in findVariables(self.tokens):
            if var not in self.variables.keys():
                self.variables[var] = None

        

        self.__string = ""
        self.__stringWithSpaces = ""
        for token in self.tokens:
            self.__string += token
            self.__stringWithSpaces += " "
            self.__stringWithSpaces += token

        self.__stringWithSpaces = self.__stringWithSpaces[1:]

    def run(self):
        if checkValid(self.tokens):
            return runMaths(self.__string, self.variables)
        else:
            return None

    def __str__(self):
        return self.__stringWithSpaces

equ = MathsParse("2a +b", {"a": 1, "b": 2})
print(equ)
print(equ.run())

print()

equ = MathsParse(input("Input equasion:\n    >>> "))
print(equ)
print(equ.run())