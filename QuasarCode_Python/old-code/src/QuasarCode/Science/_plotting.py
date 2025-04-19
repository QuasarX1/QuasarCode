import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon

def polygon_y_error_region(x_coordinates, y_upper_coordinates, y_lower_coordinates, axis = None, **plotting_kwargs):

    poly = Polygon(np.concatenate((np.array([[x_coordinates[i], y_lower_coordinates[i]] for i in range(len(x_coordinates))], dtype = float),
                                   np.array([[x_coordinates[i], y_upper_coordinates[i]] for i in range(len(x_coordinates) - 1, -1, -1)], dtype = float)),
                                  axis = 0),
                   closed = False,
                   **plotting_kwargs)
    
    if axis is not None:
        if axis == "default":
            plt.gca().add_patch(poly)
        else:
            axis.add_patch(poly)

    return poly

def polygon_x_error_region(x_left_coordinates, x_right_coordinates, y_coordinates, axis = None, **plotting_kwargs):

    poly = Polygon(np.concatenate((np.array([[x_left_coordinates[i], y_coordinates[i]] for i in range(len(y_coordinates))], dtype = float),
                                   np.array([[x_right_coordinates[i], y_coordinates[i]] for i in range(len(y_coordinates) - 1, -1, -1)], dtype = float)),
                                  axis = 0),
                   closed = False,
                   **plotting_kwargs)
    
    if axis is not None:
        if axis == "default":
            plt.gca().add_patch(poly)
        else:
            axis.add_patch(poly)

    return poly
