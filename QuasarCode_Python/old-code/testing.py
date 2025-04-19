import numpy as np
import random

import QuasarCode as qc

def f_lin(x, *args):# Straight
    return args[0] * x + args[1]

def f_quad(x, *args):# Quartic
    return args[0] * x**4 + args[1] * x**3 + args[2] * x**2 + args[3] * x + args[4]

def f_exp(x, *args):# Exp
    return args[0] * np.exp(args[1] * x) + args[2]

def f_sin(x, *args):# Exp
    return args[0] * np.sin(args[1] * x) + args[2]

##x = np.array([1.3, 2.1, 2.8, 3.9, 5.2])
##y = np.array([3.4, 4.6, 7.2, 8.5, 11.2])

#dx = np.array([1, 1, 1, 1, 1])
#dy = np.array([1, 1, 1, 1, 1])

points = 10
xRange = [0, 10]

x = np.empty(points)
y_lin = np.empty(points)
y_quad = np.empty(points)
y_exp = np.empty(points)
y_sin = np.empty(points)

dx = np.empty(points)
dy = np.empty(points)
#dx = None
#dy = None

for i, xValue in enumerate(np.linspace(xRange[0], xRange[1], points, endpoint = False)):
    x[i] = xValue
    y_lin[i] = f_lin(xValue, 2, 1) + (random.randint(-15, 15) / 100)
    y_quad[i] = f_quad(i, 0, 0, 1, 0, -2) + (random.randint(-15, 15) / 100)
    #y_quad[i] = f_quad(i, 4, 20, 0, 0, -2) + (random.randint(-15, 15) / 100)
    y_exp[i] = f_exp(i, 1, 0.05, -3) + (random.randint(-15, 15) / 100)
    y_sin[i] = f_sin(xValue, 1, 1, 0) + (random.randint(-15, 15) / 100)
    dx[i] = random.randint(5, 15) / 10
    dy[i] = random.randint(5, 15) / 10

#print(x)
#print(y)


#testFigure = qc.Science.Figure(x, y, dx, dy, size = None, title = "A test graph", xLabel = "X-Axis", yLabel = "Y-Axis", saveName = "testingFigure.png")
#testFigure.createFitLine(qc.Science.LineType.sin)
#testFigure.plot()
##testFigure.save()
#testFigure.show()# TODO: window hangs


testFigure = qc.Science.Figure(x, y_lin, dx, dy, size = None, title = "A test graph", xLabel = "X-Axis", yLabel = "Y-Axis", saveName = "testingFigure.png")
testFigure.createFitLine(qc.Science.LineType.straight)

testFigure2 = qc.Science.Figure(x, y_sin, dx, dy, size = None, fitLine = qc.Science.LineType.straight, title = "A test graph", xLabel = "X-Axis", yLabel = "Y-Axis", saveName = "testingFigure.png")
testFigure2.createFitLine(qc.Science.LineType.sin)
testFigure2.createFitLine(qc.Science.LineType.quadratic, clearOthers = False, color = "g")

testManualFigure = qc.Science.ManualFigure()
testManualFigure.addInstruction(qc.Science.DrawInstruction.plot, x, y_lin, color = "r")
testManualFigure.addInstruction(qc.Science.DrawInstruction.scatter, x, y_lin)
testManualFigure.plot()
testManualFigure.show()

testGraph = qc.Science.Graph(figures = [testFigure, testFigure2, testManualFigure], data = [[x, y_lin], [x, y_lin, dx, dy], [x, y_lin, dx, dy, None, qc.Science.LineType.straight]], shape = (3, 2), size = (8, 7))
testGraph.plot()
#testGraph.save()
testGraph.show()# TODO: window hangs

testFigure.plot()
testFigure.show()


print()

try:
    print(testFigure2.getFittingOutput())
except:
    pass

qc.pause()