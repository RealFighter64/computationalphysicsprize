import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.path import Path
from matplotlib.collections import PatchCollection, LineCollection
import matplotlib.animation as animation
import numpy as np
import heatmap

class UpdatablePatchCollection(PatchCollection):
    """ A matplotlib PatchCollection that can be updated and animated. """
    def __init__(self, patches, *args, **kwargs):
        self.patches = patches
        PatchCollection.__init__(self, patches, *args, **kwargs)

    def get_paths(self):
        self.set_paths(self.patches)
        return self._paths

def figure():
    """ Gets the current figure. """
    global fig
    return fig

def init(particles, wallPos):
    """ Initializes the renderer. """
    global fig, ax, patches, coll, wall, heat

    # Create a figure.
    fig = plt.figure()
    # Add two axes to the figure, one for the particles and one for the heatmap.
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    heat = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    # Set the proportions of the axes.
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal', 'box')
    heat.set_xlim(-10, 10)
    heat.set_ylim(-10, 10)
    heat.set_aspect('equal', 'box')

    # Initialize a list of patches.
    patches = []

    # Fill the patch list with circles corresponding to the particles.
    for i in range(0, len(particles)):
        part = particles[i]
        patches.append(Circle(tuple(part.position), part.size))

    # Create a collection for all of the patches.
    coll = UpdatablePatchCollection(patches, alpha=1)

    # Add the collection to the axes.
    ax.add_collection(coll)

    # Plot the wall to see it moving.
    wall, = ax.plot([wallPos]*20, np.linspace(-10, 10, 20))

    # Initialize the heatmap.
    heatmap.init(particles, heat)

def start(particles):
    """ Start the rendering process. """
    global coll, linecoll, wall
    return coll, wall, heatmap.start()

def animate(particles, wallPos):
    """ Animate a single frame. """
    global fig, ax, patches, coll, wall, heat
    
    # Change the patches' positions to the new particles' positions.
    for i in range(0, len(particles)):
        patches[i].center = tuple(particles[i].position)
    
    # Change the position of the wall.
    wall.set_xdata(wallPos)
    return coll, wall, heatmap.animate(particles, heat)

def show():
    # Show the plot to the screen - for live simulation only.
    plt.show()

