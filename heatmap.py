import numpy as np
from scipy.stats import gaussian_kde
import numpy.random
import matplotlib.pyplot as plt
import math

def init(particles, ax):
    global im
    animate(particles, ax)

def start():
    global im
    return im

def animate(particles, ax):
    global im
    parts = [[0., 1.], [1., 0.], [2., 0.]]

    # Populate the list with particles.
    for part in particles:
        # Slightly hack-y solution, just plot each particle multiple times depending on its velocity.
        if math.floor(np.linalg.norm(part.velocity)) > 10:
            for i in range(0, math.floor(np.linalg.norm(part.velocity) / 2)):
                parts.append(part.position)

    parts = np.array(parts)

    # Swap the axes of the array to create an array with distinct X and Y values.
    accParts = np.swapaxes(parts, 0, 1)

    # Create a gaussian Kernel Density Estimation to view the pressure.
    kde = gaussian_kde(accParts, "scott")

    # Evaluate the density estimation on a grid
    xgrid = np.linspace(-10, 10, 100)
    ygrid = np.linspace(-10, 10, 100)
    Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
    Z = kde.evaluate(np.vstack([Xgrid.ravel(), Ygrid.ravel()]))

    # Plot the result as an image
    im = ax.imshow(Z.reshape(Xgrid.shape),
            extent=[-10, 10, -10, 10],
            cmap='Oranges')

    return im
