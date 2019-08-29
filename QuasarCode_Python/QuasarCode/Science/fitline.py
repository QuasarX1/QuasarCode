from scipy import stats
from scipy.optimize import least_squares
import math
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
Figure = object# Partial initialisation to allow circular reference for type hints. See EOF for import
from QuasarCode.Science.data import errorString, standardFormStringIfNessessary

class LineType(Enum):
    none = 0
    straight = 1,# mx + c
    quadratic = 2,# ax^2 + bx + c
    cubic = 3,# ax^3 + bx^2 + cx + d
    quartic = 4,# ax^4 + bx^3 + cx^2 + dx + e
    power = 5,# ax^b + c
    exponential = 6,# a e^(bx) + c
    logarithmic = 7,# a e^(bx) + c where b is negitive
    sin = 8,# a sin(bx + c)


class LineOfBestFit(object):
    """
    """

    def __init__(self, lineType: LineType = LineType.straight, graph: Figure = None, initialFitVariables: dict = None, customFitMethods: list = None):
        self.lineType = lineType
        self.graph: Figure = graph

        if initialFitVariables is None:
            if self.lineType == LineType.straight:
                self.initialFitVariables = {"m": 1.0, "c": 1.0}
            elif self.lineType == LineType.quadratic:
                self.initialFitVariables = {"a": 1.0, "b": 1.0, "c": 1.0}
            elif self.lineType == LineType.cubic:
                self.initialFitVariables = {"a": 1.0, "b": 1.0, "c": 1.0, "d": 1.0}
            elif self.lineType == LineType.quartic:
                self.initialFitVariables = {"a": 1.0, "b": 1.0, "c": 1.0, "d": 1.0, "e": 1.0}
            elif self.lineType == LineType.power:
                self.initialFitVariables = {"a": 1.0, "b": 1.0, "c": 1.0}
            elif self.lineType == LineType.exponential:
                self.initialFitVariables = {"a": 1.0, "b": 1.0, "c": 1.0}
            elif self.lineType == LineType.logarithmic:
                self.initialFitVariables = {"a": 1.0, "b": -1.0, "c": 1.0}
            elif self.lineType == LineType.sin:
                self.initialFitVariables = {"a": 1.0, "b": 1.0, "c": 1.0}
        else:
            self.initialFitVariables = initialFitVariables

        if customFitMethods is None:
            if self.lineType == LineType.straight:
                self.fitLine = LineOfBestFit.fitLine_straight
                self.fitError = LineOfBestFit.fitError_straight
            elif self.lineType == LineType.quadratic:
                self.fitLine = LineOfBestFit.fitLine_quadratic
                self.fitError = LineOfBestFit.fitError_quadratic
            elif self.lineType == LineType.cubic:
                self.fitLine = LineOfBestFit.fitLine_cubic
                self.fitError = LineOfBestFit.fitError_cubic
            elif self.lineType == LineType.quartic:
                self.fitLine = LineOfBestFit.fitLine_quartic
                self.fitError = LineOfBestFit.fitError_quartic
            elif self.lineType == LineType.power:
                self.fitLine = LineOfBestFit.fitLine_power
                self.fitError = LineOfBestFit.fitError_power
            elif self.lineType == LineType.exponential or lineType == LineType.logarithmic:
                self.fitLine = LineOfBestFit.fitLine_exponential
                self.fitError = LineOfBestFit.fitError_exponential
            elif self.lineType == LineType.sin:
                self.fitLine = LineOfBestFit.fitLine_sin
                self.fitError = LineOfBestFit.fitError_sin
        else:
            self.fitLine = customFitMethods[0]
            self.fitError = customFitMethods[1]

        self.fit_X = None
        self.fit_Y = None
        self.fittingOutput = None
        self.fitVariables = {}
        self.fitQuality = None

        self.runFit()

    def runFit(self):
        """
        Runs the fitting algorithem with the current fit atributes

        Credits:
            Tim Greenshaw
            Christopher Rowe
        """

        if self.graph is None:
            raise AttributeError("The \"graph\" property was not set as no figure has been linked.")

        initialValues = []
        self.fitVariables = {}

        if self.lineType == LineType.straight:
            #self.fit, self.fittingOutput, self.fitVariables["m"], self.fitVariables["c"], self.fitQuality = plotStraightLineGraph(graph.x, graph.y, graph.xError, graph.yError, "", False, [self.initialFitVariables["c"], self.initialFitVariables["m"]])
            initialValues = [self.initialFitVariables["c"], self.initialFitVariables["m"]]
        elif self.lineType == LineType.quadratic:
            initialValues = [self.initialFitVariables["c"], self.initialFitVariables["b"], self.initialFitVariables["a"]]
        elif self.lineType == LineType.cubic:
            initialValues = [self.initialFitVariables["d"], self.initialFitVariables["c"], self.initialFitVariables["b"], self.initialFitVariables["a"]]
        elif self.lineType == LineType.quartic:
            initialValues = [self.initialFitVariables["e"], self.initialFitVariables["d"], self.initialFitVariables["c"], self.initialFitVariables["b"], self.initialFitVariables["a"]]
        elif self.lineType == LineType.power:
            initialValues = [self.initialFitVariables["c"], self.initialFitVariables["b"], self.initialFitVariables["a"]]
        elif self.lineType == LineType.exponential or self.lineType == LineType.logarithmic:
            initialValues = [self.initialFitVariables["c"], self.initialFitVariables["b"], self.initialFitVariables["a"]]
        elif self.lineType == LineType.sin:
            initialValues = [self.initialFitVariables["c"], self.initialFitVariables["b"], self.initialFitVariables["a"]]


        numberOfPoints = np.size(self.graph.x)
        out = least_squares(self.fitError, initialValues, args=(self.graph.x, self.graph.y, self.graph.xError if self.graph.xError is not None else 0, self.graph.yError if self.graph.yError is not None else 0))

        if not out.success:
            #raise RuntimeWarning("Fit failed.")
            self.fittingOutput = "Fit failed."
            self.fitQuality = math.inf
            self.fitVariables = {}
            for key in self.initialFitVariables:
                self.fitVariables[key] = None
            return
            

        output = ""

        finalValues = out.x

        # Calculate chi^2 per point, summed chi^2 and chi^2/NDF (Number of Degrees of Freedom)
        chiList = self.fitError(finalValues, self.graph.x, self.graph.y, self.graph.xError if self.graph.xError is not None else 0, self.graph.yError if self.graph.yError is not None else 0)**2
        chiSquared = np.sum(chiList)
        NDF = numberOfPoints - 2#TODO: check this - overide option?
        reducedChiSquared = chiSquared/NDF

        output += "\nFit quality:" \
                + "\n    chi Squared per point:\n        " + str(chiList) \
                + "\n\n    chi Squared = {}".format(standardFormStringIfNessessary(chiSquared, 5)) \
                + "\n    chi Squared / NDF = {}".format(standardFormStringIfNessessary(reducedChiSquared, 5)) \
                + "\n\n    Final Fit Variables:\n        " + str(finalValues) \
                + "\n\n    y:\n        " + str(self.graph.y) \
                + "\n\n    dx:\n        " + str(self.graph.xError) \
                + "\n\n    dy:\n        " + str(self.graph.yError)

        # Compute covariance
        jMat = out.jac
        jMat2 = np.dot(jMat.T, jMat)
        detJmat2 = np.linalg.det(jMat2)

        finalErrors = []
        if detJmat2 < 1E-32:
            for i in range(len(finalValues)):
                finalErrors.append(0.0)

            output += "\n\nValue of determinat detJmat2 " + str(detJmat2) + "\nMatrix singular, error calculation failed."

        else:
            covar = np.linalg.inv(jMat2)
            for i in range(len(finalValues)):
                finalErrors.append(np.sqrt(covar[i, i]))
            
        # Calculate fitted function values
        #self.fit = self.fitLine(finalValues, self.graph.x)
        self.fit_X = np.linspace(min(self.graph.x), max(self.graph.x), 1000000)
        self.fit_Y = self.fitLine(finalValues, self.fit_X)
        
        self.fitQuality = reducedChiSquared

        lastIndex = len(finalValues) - 1
        for i, key in enumerate(self.initialFitVariables):
            self.fitVariables[key] = (finalValues[lastIndex - i], finalErrors[lastIndex - i])

        output += "\n\nParameters returned by fit:"

        for key in self.fitVariables:
            output += "\n    " + str(key) + " = " + errorString(self.fitVariables[key][0], standardFormStringIfNessessary(self.fitVariables[key][1]))

        self.fittingOutput = output

    @staticmethod
    def fitLine_straight(p: list, x):
        """
        Calculates a y value for a straight line
        y_guess = mx + c

        p: [c, m]

        Credits:
            Tim Greenshaw
            Christopher Rowe
        """
        f = p[1]*x + p[0]
        return f
    
    @staticmethod
    def fitError_straight(p: list, x, y, xerr, yerr):
        """
        Calculates the error for a straight line
        error = (y - y_guess) / sqrt(dy^2 + m^2 * dx^2)

        p: [c, m]

        Credits:
            Tim Greenshaw
        """
        if not (isinstance(xerr, int) and xerr == 0) and not (isinstance(xerr, int) and yerr == 0):
            e = (y - LineOfBestFit.fitLine_straight(p, x)) / np.sqrt(yerr**2 + p[1]**2 * xerr**2)
        else:
            e = y - LineOfBestFit.fitLine_straight(p, x)

        return e

    @staticmethod
    def fitLine_quadratic(p: list, x):
        """
        Calculates a y value for a quadratic curve
        y_guess = ax^2 + bx + c

        p: [c, b, a]
        """
        f = p[2] * x**2 + p[1] * x + p[0]
        return f
    
    @staticmethod
    def fitError_quadratic(p: list, x, y, xerr, yerr):
        """
        Calculates the error for a quadratic curve
        error = (y - y_guess) / sqrt(dy^2 + dx^2)

        p: [c, b, a]
        """
        predicted_y = LineOfBestFit.fitLine_quadratic(p, x)
        if not (isinstance(xerr, int) and xerr == 0) and not (isinstance(xerr, int) and yerr == 0):
            e = (y - predicted_y) / np.sqrt(xerr**2 + yerr**2)
        else:
            e = y - LineOfBestFit.fitLine_quadratic(p, x)
        return e

    @staticmethod
    def fitLine_cubic(p: list, x):
        """
        Calculates a y value for a cubic curve
        y_guess = ax^3 + bx^2 + cx + d

        p: [d, c, b, a]
        """
        f = p[3] * x**3 + p[2] * x**2 + p[1] * x + p[0]
        return f
    
    @staticmethod
    def fitError_cubic(p: list, x, y, xerr, yerr):
        """
        Calculates the error for a cubic curve
        error = (y - y_guess) / sqrt(dy^2 + dx^2)

        p: [d, c, b, a]
        """
        predicted_y = LineOfBestFit.fitLine_cubic(p, x)
        if not (isinstance(xerr, int) and xerr == 0) and not (isinstance(xerr, int) and yerr == 0):
            e = (y - predicted_y) / np.sqrt(xerr**2 + yerr**2)
        else:
            e = y - LineOfBestFit.fitLine_cubic(p, x)
        return e

    @staticmethod
    def fitLine_quartic(p: list, x):
        """
        Calculates a y value for a quartic curve
        y_guess = ax^4 + bx^3 + cx^2 + dx + e

        p: [e, d, c, b, a]
        """
        f = p[4] * x**4 + p[3] * x**3 + p[2] * x**2 + p[1] * x + p[0]
        return f
    
    @staticmethod
    def fitError_quartic(p: list, x, y, xerr, yerr):
        """
        Calculates the error for a quartic curve
        error = (y - y_guess) / sqrt(dy^2 + dx^2)

        p: [e, d, c, b, a]
        """
        predicted_y = LineOfBestFit.fitLine_quartic(p, x)
        if not (isinstance(xerr, int) and xerr == 0) and not (isinstance(xerr, int) and yerr == 0):
            e = (y - predicted_y) / np.sqrt(xerr**2 + yerr**2)
        else:
            e = y - LineOfBestFit.fitLine_quartic(p, x)
        return e

    @staticmethod
    def fitLine_power(p: list, x):
        """
        Calculates a y value for a power curve
        y_guess = ax^b + c

        p: [c, b, a]
        """
        f = p[2] * x**p[1] + p[0]
        return f
    
    @staticmethod
    def fitError_power(p: list, x, y, xerr, yerr):
        """
        Calculates the error for a power curve
        error = (y - y_guess) / sqrt(dy^2 + dx^2)

        p: [c, b, a]
        """
        predicted_y = LineOfBestFit.fitLine_power(p, x)
        if not (isinstance(xerr, int) and xerr == 0) and not (isinstance(xerr, int) and yerr == 0):
            e = (y - predicted_y) / np.sqrt(xerr**2 + yerr**2)
        else:
            e = y - LineOfBestFit.fitLine_power(p, x)
        return e

    @staticmethod
    def fitLine_exponential(p: list, x):
        """
        Calculates a y value for an exponential curve (make b negitive for a logarithmic line)
        y_guess = a e^(bx) + c

        p: [c, b, a]
        """
        f = p[2] * np.exp(p[1] * x) + p[0]
        return f
    
    @staticmethod
    def fitError_exponential(p: list, x, y, xerr, yerr):
        """
        Calculates the error for an exponential curve (make b negitive for a logarithmic line)
        error = (y - y_guess) / sqrt(dy^2 + dx^2)

        p: [c, b, a]
        """
        predicted_y = LineOfBestFit.fitLine_exponential(p, x)
        if not (isinstance(xerr, int) and xerr == 0) and not (isinstance(xerr, int) and yerr == 0):
            e = (y - predicted_y) / np.sqrt(xerr**2 + yerr**2)
        else:
            e = y - LineOfBestFit.fitLine_exponential(p, x)
        return e

    @staticmethod
    def fitLine_sin(p: list, x):
        """
        Calculates a y value for a sine curve
        y_guess = a sin(bx + c)

        p: [c, b, a]
        """
        f = p[2] * np.sin(p[1] * x + p[0])
        return f
    
    @staticmethod
    def fitError_sin(p: list, x, y, xerr, yerr):
        """
        Calculates the error for a sine curve
        error = (y - y_guess) / sqrt(dy^2 + dx^2)

        p: [c, b, a]
        """
        predicted_y = LineOfBestFit.fitLine_sin(p, x)
        if not (isinstance(xerr, int) and xerr == 0) and not (isinstance(xerr, int) and yerr == 0):
            e = (y - predicted_y) / np.sqrt(xerr**2 + yerr**2)
        else:
            e = y - LineOfBestFit.fitLine_sin(p, x)
        return e



#def fitLine(p, x):
#    '''
#    Straight line
#    '''
#    f = p[0] + p[1]*x
#    return f
##
#def fitError(p, x, y, xerr, yerr):
#    '''
#    Error function for straight line fit
#    '''
#    e = (y - fitLine(p, x))/(np.sqrt(yerr**2 + p[1]**2*xerr**2))
#    return e
##
## Set initial values of fit parameters, run fit

#def plotStraightLineGraph(x, y, xErr, yErr, title, saveName = "fig.png", plotData = True, initialValues = [1.0, -1.0]):
#    """
#    returns: fitData, output, (mVal, mErr), (cVal, cErr), redchisq

#    Credits:
#        Tim Greenshaw
#    """
#    output = ""

#    nLen = np.size(x)

#    xData = x
#    yData = y
#    xError = xErr
#    yError = yErr

#    nPoints = nLen

#    pInit = initialValues
#    out = least_squares(fitError, pInit, args=(xData, yData, xError, yError))
#    #
#    fitOK = out.success
#    #
#    # Test if fit failed
#    if not fitOK:
#        output += "\n "
#        output += "\nFit failed"
#    else:
#        #
#        # get output
#        pFinal = out.x
#        cVal = pFinal[0]
#        mVal = pFinal[1]
#        #
#        #   Calculate chis**2 per point, summed chi**2 and chi**2/NDF
#        chiarr = fitError(pFinal, xData, yData, xError, yError)**2
#        chisq = np.sum(chiarr)
#        NDF = nPoints - 2
#        redchisq = chisq/NDF
#    #
#        np.set_printoptions(precision = 3)
#        output += "\n "
#        output += "\nFit quality:"
#        output += "\nchisq per point = \n " + str(chiarr)
#        output += "\nchisq = {:5.2f}, chisq/NDF = {:5.2f}.".format(chisq, redchisq)
#        output += "\n pFinal: "+str(pFinal)+" y: "+str(yData)
#        output += "\n dx: "+str(xError)+" dy: "+str(yError)
#        #
#        # Compute covariance
#        jMat = out.jac
#        jMat2 = np.dot(jMat.T, jMat)
#        detJmat2 = np.linalg.det(jMat2)
#        #
#        if detJmat2 < 1E-32:
#            output += "\nValue of determinat detJmat2 " + str(detJmat2)
#            output += "\nMatrix singular, error calculation failed."
#            output += "\n "
#            output += "\nParameters returned by fit:"
#            output += "\nIntercept = {:5.2f}".format(cVal)
#            output += "\nGradient = {:5.2f}".format(mVal)
#            output += "\n "
#            cErr = 0.0
#            mErr = 0.0
#        else:
#            covar = np.linalg.inv(jMat2)
#            cErr = np.sqrt(covar[0, 0])
#            mErr = np.sqrt(covar[1, 1])
#            #
#            output += "\n "
#            output += "\nParameters returned by fit:"
#            output += "\nIntercept (Sin theta i) = {:5.2f} +- {:5.2f}".format(cVal, cErr)
#            output += "\nGradient () = {:5.2f} +- {:5.2f}".format(mVal, mErr)
#            output += "\n "
#        #
#        # Calculate fitted function values
#        fitData = fitLine(pFinal, xData)
#        #
        
        
#    # Plot data
#    if plotData:
#        fig = plt.figure(figsize = (8, 6))
#        plt.title(title)
#        plt.xlabel('Radius squared (m^2)')
#        plt.ylabel('Period squared (s^2)')
#        plt.errorbar(xData, yData, xerr = xError, yerr = yError, fmt='r', \
#                    linestyle = '', label = "Data") 
#        plt.plot(xData, fitData, color = 'b', linestyle = '-', label = "Fit")
#        #plt.xlim(1.0, 7.0)
#        #plt.ylim(0.0, 3.0)
#        plt.grid(color = 'g')
#        plt.legend(loc = 2, prop={'size': 20})

#        plt.savefig(saveName)
#        plt.show()
    
#    return fitData, output, (mVal, mErr), (cVal, cErr), redchisq

from QuasarCode.Science.figure import Figure