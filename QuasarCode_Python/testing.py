import numpy as np

import QuasarCode as qc

x = np.array([1.3, 2.1, 2.8, 3.9, 5.2])
y = np.array([3.4, 4.6, 7.2, 8.5, 11.2])

dx = np.array([1, 1, 1, 1, 1])
dy = np.array([1, 1, 1, 1, 1])

testGraph = qc.Science.graph.Figure(x, y, dx, dy, size = None, title = "A test graph", xLabel = "X-Axis", yLabel = "Y-Axis", saveName = "testingFigure.png")
testGraph.createFitLine()
testGraph.plot()
testGraph.save()
#testGraph.show()# TODO: window hangs

m = testGraph.fit.fitVariables["m"]
c = testGraph.fit.fitVariables["c"]

print(m[0], m[1])
print(c[0], c[1])

print(qc.Science.data.errorString(m[0], m[1]))
print(qc.Science.data.errorString(c[0], c[1]))

print(qc.Science.data.sigFig(1235, 3))

qc.pause()