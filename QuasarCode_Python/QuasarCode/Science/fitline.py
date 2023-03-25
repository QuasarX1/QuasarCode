from scipy import stats
from scipy.optimize import least_squares
import math
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
IAutomaticFigure = object# Partial initialisation to allow circular reference for type hints. See EOF for import
from QuasarCode.Science.data import errorString, standardFormStringIfNessessary

class LineType(Enum):
    """
    An enumeration listing the valid line types used by the LineOfBestFit class.
    """

    none = 0
    straight = 1,# mx + c
    quadratic = 2,# ax^2 + bx + c
    cubic = 3,# ax^3 + bx^2 + cx + d
    quartic = 4,# ax^4 + bx^3 + cx^2 + dx + e
    power = 5,# ax^b + c
    exponential = 6,# a e^(bx) + c
    logarithmic = 7,# a e^(bx) + c where b is negitive
    sin = 8,# a sin(bx + c)
    #gaussian = 9,# TODO: add this
    custom = 9


class LineOfBestFit(object):
    """
    Calculates and stores a line of best fit using an associated Figure object holding the data and optional errors.

    Arguments:
        Figure figure -> the accociated Figure object with the data needed to calculate the fit.

        LineType lineType -> The type of line to be created. Use LineType.custom for custom options.
                                (Defualt is LineType.straight)

        dict initialFitVariables -> A dictionary containing the fit variables and their starting value used to
                                    overide he defults or to specify a custom fit. Variables should be in oposite
                                    order to that expected by the fitting functions i.e. m then c for y = m * x + c (Defult is None)

        list customFitMethods -> A list with two items: [the fitting function, the error function] (Defult is None)

    A custom fit can be produced by specifying the lineType argument as LineType.custom and then specifying the fit
    variables and providing the fitting functions. LineOfBestFit.createGenericErrorFunc allows a fit function to be
    specified to produce a generic error function. Resulting customFitMethods for this would be
    [fitFunc, errorFunc] or [fitFunc, LineOfBestFit.createGenericErrorFunc(fitFunc)]
    """

    def __init__(self, figure: IAutomaticFigure, lineType: LineType = LineType.straight, initialFitVariables: dict = None, customFitMethods: list = None):
        self.lineType = lineType
        self.figure: Figure = figure

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
            elif self.lineType == LineType.custom:
                raise ValueError("No fit variables were provided. This is required for a custom fit.")
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
            elif self.lineType == LineType.custom:
                raise ValueError("No fit functions were provided. This is required for a custom fit.")
        else:
            if not isinstance(customFitMethods, list):
                raise TypeError("The value provided for the argument of customFitMethods was not a list.")
            elif len(customFitMethods) != 2:
                raise ValueError("The value provided for the argument of customFitMethods had {} elements. It must have exactly 2.".format(len(customFitMethods)))

            self.fitLine = customFitMethods[0]
            self.fitError = customFitMethods[1]

        self.fit_X = None
        self.fit_Y = None
        self.fittingOutput = None
        self.fitVariables = {}
        self.fitQuality = None

        self.runFit()

    def runFit(self, linePoints = 1000000):
        """
        Runs the fitting algorithem with the current fit atributes

        Arguments:
            int linePoints -> the number of x values to use within the min to max range of
                                the data points in order to create the fit line. (Defult is 1,000,000)

        Credits:
            Tim Greenshaw
            Christopher Rowe
        """

        if not isinstance(linePoints, int):
            raise TypeError("The value provided for the argument \"linePoints\" was not of type int.")
        elif linePoints <= 0:
            raise ValueError("The number of points must be a non zero positive value.")

        if not isinstance(self.figure, IAutomaticFigure):
            raise AttributeError("The \"figure\" property was not set as no valid figure has been linked.")

        initialValues = []
        self.fitVariables = {}

        # In the event that the line type none was specified - don't create a line.
        if self.lineType == LineType.none or self.lineType is None:
            self.fittingOutput = "Fit type \"none\" specified. No fit generated."
            self.fitQuality = math.inf
            for key in self.initialFitVariables:
                self.fitVariables[key] = None
            self.fit_X = None
            self.fit_Y = None
            return

        # Set the initial values for the specified type of line
        elif self.lineType == LineType.straight:
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
        elif self.lineType == LineType.custom:
            initialValues = [self.initialFitVariables[key] for key in self.initialFitVariables]
            initialValues.reverse()


        numberOfPoints = np.size(self.figure.get_x())
        out = least_squares(self.fitError, initialValues, args=(self.figure.get_x(), self.figure.get_y(), self.figure.get_xError() if self.figure.get_xError() is not None else 0, self.figure.get_yError() if self.figure.get_yError() is not None else 0))

        if not out.success:
            #raise RuntimeWarning("Fit failed.")
            self.fittingOutput = "Fit failed."
            self.fitQuality = math.inf
            self.fitVariables = {}
            for key in self.initialFitVariables:
                self.fitVariables[key] = None
            self.fit_X = None
            self.fit_Y = None
            return
            

        output = ""

        finalValues = out.x

        # Calculate chi^2 per point, summed chi^2 and chi^2/NDF (Number of Degrees of Freedom)
        chiList = self.fitError(finalValues, self.figure.get_x(), self.figure.get_y(), self.figure.get_xError() if self.figure.get_xError() is not None else 0, self.figure.get_yError() if self.figure.get_yError() is not None else 0)**2
        chiSquared = np.sum(chiList)
        NDF = numberOfPoints - 2#TODO: check this - overide option?
        reducedChiSquared = chiSquared/NDF

        output += "\nFit quality:" \
                + "\n    chi Squared per point:\n        " + str(chiList) \
                + "\n\n    chi Squared = {}".format(standardFormStringIfNessessary(chiSquared, 5)) \
                + "\n    chi Squared / NDF = {}".format(standardFormStringIfNessessary(reducedChiSquared, 5)) \
                + "\n\n    Final Fit Variables:\n        " + str(finalValues) \
                + "\n\n    y:\n        " + str(self.figure.get_y()) \
                + "\n\n    dx:\n        " + str(self.figure.get_xError()) \
                + "\n\n    dy:\n        " + str(self.figure.get_yError())

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
        self.fit_X = np.linspace(min(self.figure.get_x()), max(self.figure.get_x()), linePoints)
        self.fit_Y = self.fitLine(finalValues, self.fit_X)
        
        self.fitQuality = reducedChiSquared

        lastIndex = len(finalValues) - 1
        for i, key in enumerate(self.initialFitVariables):
            self.fitVariables[key] = (finalValues[lastIndex - i], finalErrors[lastIndex - i])

        output += "\n\nParameters returned by fit:"

        for key in self.fitVariables:
            output += "\n    " + str(key) + " = " + errorString(self.fitVariables[key][0], self.fitVariables[key][1])

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
            Christopher Rowe
        """
        #if not (isinstance(xerr, int) and xerr == 0) and not (isinstance(yerr, int) and yerr == 0):
        #    e = (y - LineOfBestFit.fitLine_straight(p, x)) / np.sqrt(yerr**2 + p[1]**2 * xerr**2)
        #else:
        #    e = y - predicted_y

        #return e
        return LineOfBestFit.__fitError_generic(LineOfBestFit.fitLine_straight, p, x, y, xerr, yerr, lambda p, x, y, xerr, yerr: np.sqrt(yerr**2 + p[1]**2 * xerr**2))

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
        error = (y - y_guess) / sqrt(dy^2 + (ax + b) dx^2)

        p: [c, b, a]
        """
        return LineOfBestFit.__fitError_generic(LineOfBestFit.fitLine_quadratic, p, x, y, xerr, yerr, lambda p, x, y, xerr, yerr: np.sqrt(yerr**2 + (p[2] * x + p[1])**2 * xerr**2))

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
        error = (y - y_guess) / sqrt(dy^2 + (ax^2 + bx + c) dx^2)

        p: [d, c, b, a]
        """
        return LineOfBestFit.__fitError_generic(LineOfBestFit.fitLine_cubic, p, x, y, xerr, yerr, lambda p, x, y, xerr, yerr: np.sqrt(yerr**2 + (p[3] * x**2 + p[2] * x + p[1])**2 * xerr**2))

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
        error = (y - y_guess) / sqrt(dy^2 + (ax^3 + bx^2 + cx + d) dx^2)

        p: [e, d, c, b, a]
        """
        return LineOfBestFit.__fitError_generic(LineOfBestFit.fitLine_quartic, p, x, y, xerr, yerr, lambda p, x, y, xerr, yerr: np.sqrt(yerr**2 + (p[4] * x**3 + p[3] * x**2 + p[2] * x + p[1])**2 * xerr**2))

    @staticmethod
    def fitLine_power(p: list, x):
        """
        Calculates a y value for a power curve
        y_guess = a x^b + c

        p: [c, b, a]
        """
        f = p[2] * x**p[1] + p[0]
        return f
    
    @staticmethod
    def fitError_power(p: list, x, y, xerr, yerr):
        """
        Calculates the error for a power curve
        error = (y - y_guess) / sqrt(dy^2 + a b x^(b-1) dx^2)

        p: [c, b, a]
        """
        return LineOfBestFit.__fitError_generic(LineOfBestFit.fitLine_power, p, x, y, xerr, yerr, lambda p, x, y, xerr, yerr: np.sqrt(yerr**2 + (p[2] * p[1] * x**(p[1] - 1)) * xerr**2))

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
        error = (y - y_guess) / sqrt(dy^2 + a b e^(bx) dx^2)

        p: [c, b, a]
        """
        return LineOfBestFit.__fitError_generic(LineOfBestFit.fitLine_exponential, p, x, y, xerr, yerr, lambda p, x, y, xerr, yerr: np.sqrt(yerr**2 + (p[2] * p[1] * np.exp(p[1] * x)) * xerr**2))

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
        error = (y - y_guess) / sqrt(dy^2 + a b sin(bx + c) dx^2)

        p: [c, b, a]
        """
        #return LineOfBestFit.__fitError_generic(LineOfBestFit.fitLine_sin, p, x, y, xerr, yerr, lambda p, x, y, xerr, yerr: np.sqrt(yerr**2 + (p[2] * p[1] * np.cos(p[1] * x + p[0])) * xerr**2))
        LineOfBestFit.__fitError_generic(LineOfBestFit.fitLine_sin, p, x, y, xerr, yerr, lambda p, x, y, xerr, yerr: np.sqrt(yerr**2 + (p[2] * p[1] * np.cos(p[1] * x + p[0])) * xerr**2))

    @staticmethod
    def __fitError_generic(fitFunction, p: list, x, y, xerr, yerr, combineErrors = lambda p, x, y, xerr, yerr: np.sqrt(xerr**2 + yerr**2)):
        """
        Calculates the error for a specified function
        error = (y - y_guess) / e where by defualt e is: sqrt(dy^2 + dx^2)

        The error calculation should be e^2 = (δF/δx yerr)^2 + (δF/δy yerr)^2
                                            = (δF/δx yerr)^2 + yerr^2           as the diferential of F(x) with respect to y is 1
        """
        predicted_y = fitFunction(p, x)
        if not (isinstance(xerr, int) and xerr == 0) and not (isinstance(yerr, int) and yerr == 0):
            e = (y - predicted_y) / combineErrors(p, x, y, xerr, yerr)
        else:
            e = y - predicted_y
        return e

    @staticmethod
    def createGenericErrorFunc(fitFunction, combineErrors = lambda p, x, y, xerr, yerr: np.sqrt(xerr**2 + yerr**2)):
        """
        Wraps a fitting function inside the generic error function.
        Use this to utilise the generic fitting function with a custom fit.
        """
        return lambda p, x, y, xerr, yerr: __fitError_generic(fitFunction, p, x, y, xerr, yerr, combineErrors)



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

from QuasarCode.Science.figure import IAutomaticFigure