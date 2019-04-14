from scipy import stats
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
Figure = object# Partial initialisation to allow circular reference for type hints. See EOF for import

class LineType(Enum):
    straight = 0


class LineOfBestFit(object):
    """
    """

    def __init__(self, lineType: LineType = LineType.straight, graph: Figure = None, initialFitVariables = None, customFitMethods: list = None):
        self.lineType = lineType
        self.graph: Figure = graph

        if initialFitVariables is None:
            if lineType == LineType.straight:
                self.initialFitVariables = {"m": 1.0, "c": 1.0}
        else:
            self.initialFitVariables = initialFitVariables

        if customFitMethods is None:
            if lineType == LineType.straight:
                self.fitLine = LineOfBestFit.fitLine_straight
                self.fitError = LineOfBestFit.fitError_straight
        else:
            self.fitLine = customFitMethods[0]
            self.fitError = customFitMethods[1]

        self.fit = None
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


        output = ""

        nLen = np.size(self.graph.x)

        nPoints = nLen

        pInit = initialValues
        out = least_squares(fitError, pInit, args=(self.graph.x, self.graph.y, self.graph.xError, self.graph.yError))
        
        fitOK = out.success
        
        # Test if fit failed
        if not fitOK:
            output += "\n "
            output += "\nFit failed"
        else:
            # get output
            pFinal = out.x
            cVal = pFinal[0]
            mVal = pFinal[1]
            
            #   Calculate chis**2 per point, summed chi**2 and chi**2/NDF
            chiarr = fitError(pFinal, self.graph.x, self.graph.y, self.graph.xError, self.graph.yError)**2
            chisq = np.sum(chiarr)
            NDF = nPoints - 2
            redchisq = chisq/NDF
            
            np.set_printoptions(precision = 3)
            output += "\n "
            output += "\nFit quality:"
            output += "\nchisq per point = \n " + str(chiarr)
            output += "\nchisq = {:5.2f}, chisq/NDF = {:5.2f}.".format(chisq, redchisq)
            output += "\n pFinal: "+str(pFinal)+" y: "+str(self.graph.y)
            output += "\n dx: "+str(self.graph.xError)+" dy: "+str(self.graph.yError)
            
            # Compute covariance
            jMat = out.jac
            jMat2 = np.dot(jMat.T, jMat)
            detJmat2 = np.linalg.det(jMat2)
            
            if detJmat2 < 1E-32:
                output += "\nValue of determinat detJmat2 " + str(detJmat2)
                output += "\nMatrix singular, error calculation failed."
                output += "\n "
                output += "\nParameters returned by fit:"
                output += "\nIntercept = {:5.2f}".format(cVal)
                output += "\nGradient = {:5.2f}".format(mVal)
                output += "\n "
                cErr = 0.0
                mErr = 0.0
            else:
                covar = np.linalg.inv(jMat2)
                cErr = np.sqrt(covar[0, 0])
                mErr = np.sqrt(covar[1, 1])
                
                output += "\n "
                output += "\nParameters returned by fit:"
                output += "\nIntercept (Sin theta i) = {:5.2f} +- {:5.2f}".format(cVal, cErr)
                output += "\nGradient () = {:5.2f} +- {:5.2f}".format(mVal, mErr)
                output += "\n "
            
            # Calculate fitted function values
            fitData = fitLine(pFinal, self.graph.x)
        
        self.fit = fitData
        self.fittingOutput = output
        self.fitVariables["m"] = (mVal, mErr)
        self.fitVariables["c"] = (cVal, cErr)
        self.fitQuality = redchisq

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
        e = (y - fitLine(p, x)) / (np.sqrt(yerr**2 + p[1]**2 * xerr**2))
        return e



def fitLine(p, x):
    '''
    Straight line
    '''
    f = p[0] + p[1]*x
    return f
#
def fitError(p, x, y, xerr, yerr):
    '''
    Error function for straight line fit
    '''
    e = (y - fitLine(p, x))/(np.sqrt(yerr**2 + p[1]**2*xerr**2))
    return e
#
# Set initial values of fit parameters, run fit

def plotStraightLineGraph(x, y, xErr, yErr, title, saveName = "fig.png", plotData = True, initialValues = [1.0, -1.0]):
    """
    returns: fitData, output, (mVal, mErr), (cVal, cErr), redchisq

    Credits:
        Tim Greenshaw
    """
    output = ""

    nLen = np.size(x)

    xData = x
    yData = y
    xError = xErr
    yError = yErr

    nPoints = nLen

    pInit = initialValues
    out = least_squares(fitError, pInit, args=(xData, yData, xError, yError))
    #
    fitOK = out.success
    #
    # Test if fit failed
    if not fitOK:
        output += "\n "
        output += "\nFit failed"
    else:
        #
        # get output
        pFinal = out.x
        cVal = pFinal[0]
        mVal = pFinal[1]
        #
        #   Calculate chis**2 per point, summed chi**2 and chi**2/NDF
        chiarr = fitError(pFinal, xData, yData, xError, yError)**2
        chisq = np.sum(chiarr)
        NDF = nPoints - 2
        redchisq = chisq/NDF
    #
        np.set_printoptions(precision = 3)
        output += "\n "
        output += "\nFit quality:"
        output += "\nchisq per point = \n " + str(chiarr)
        output += "\nchisq = {:5.2f}, chisq/NDF = {:5.2f}.".format(chisq, redchisq)
        output += "\n pFinal: "+str(pFinal)+" y: "+str(yData)
        output += "\n dx: "+str(xError)+" dy: "+str(yError)
        #
        # Compute covariance
        jMat = out.jac
        jMat2 = np.dot(jMat.T, jMat)
        detJmat2 = np.linalg.det(jMat2)
        #
        if detJmat2 < 1E-32:
            output += "\nValue of determinat detJmat2 " + str(detJmat2)
            output += "\nMatrix singular, error calculation failed."
            output += "\n "
            output += "\nParameters returned by fit:"
            output += "\nIntercept = {:5.2f}".format(cVal)
            output += "\nGradient = {:5.2f}".format(mVal)
            output += "\n "
            cErr = 0.0
            mErr = 0.0
        else:
            covar = np.linalg.inv(jMat2)
            cErr = np.sqrt(covar[0, 0])
            mErr = np.sqrt(covar[1, 1])
            #
            output += "\n "
            output += "\nParameters returned by fit:"
            output += "\nIntercept (Sin theta i) = {:5.2f} +- {:5.2f}".format(cVal, cErr)
            output += "\nGradient () = {:5.2f} +- {:5.2f}".format(mVal, mErr)
            output += "\n "
        #
        # Calculate fitted function values
        fitData = fitLine(pFinal, xData)
        #
        
        
    # Plot data
    if plotData:
        fig = plt.figure(figsize = (8, 6))
        plt.title(title)
        plt.xlabel('Radius squared (m^2)')
        plt.ylabel('Period squared (s^2)')
        plt.errorbar(xData, yData, xerr = xError, yerr = yError, fmt='r', \
                    linestyle = '', label = "Data") 
        plt.plot(xData, fitData, color = 'b', linestyle = '-', label = "Fit")
        #plt.xlim(1.0, 7.0)
        #plt.ylim(0.0, 3.0)
        plt.grid(color = 'g')
        plt.legend(loc = 2, prop={'size': 20})

        plt.savefig(saveName)
        plt.show()
    
    return fitData, output, (mVal, mErr), (cVal, cErr), redchisq

from QuasarCode.Science.graph import Figure