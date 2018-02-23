import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as pyplot
pyplot.rcParams['animation.ffmpeg_path'] = 'C:\\Users\\William\\Programming\\ffmpeg\\bin\\ffmpeg.exe'
import matplotlib.animation as animation
import numpy as np

import math
from itertools import combinations
from sys import argv

from particle import Particle
import render
import heatmap

# Constants
frameRate = 15
gasConstant = 8.3144598 # The Gas Constant, R, for use in calculating the particles' average velocity.
numberOfParticles = 500 # The number of particles in the whole 10x10 grid
temperature = 100.0
molarMass = 29.0
zoomFactor = 1
particleVelocity = math.sqrt((3*gasConstant*temperature)/molarMass) * zoomFactor

# Set the random seed, for reproduceability.
np.random.seed(110110475)

# Set up a list of particles.
particles = []

def getYComp(xComp, up):
    """ Gets the Y Component of the velocity vectors given an x component, so that the magnitude will
        always be equal to particleVelocity """
    if up: yMod = 1
    else: yMod = -1
    return math.sqrt(1 - xComp**2)  * yMod

# Populate the list with particles.
for i in range(0, numberOfParticles):
    partPos = np.random.rand(2)
    partPos = partPos * [20, 20] + [-10, -10]
    partVelX, up = np.random.rand(2) * [2, 2] + [-1, -1]
    partVel = np.array([partVelX, getYComp(partVelX, up>0)]) * particleVelocity
    part = Particle(partPos, 0.3, 1, partVel)
    particles.append(part)

# Initialize the render process.
render.init(particles, -10)

# Set the initial position of the left wall.
wallPos = -9.5

def animate(k):
    """ Animates the particles, but doesn't render them yet. """

    global wallPos
    f = 5 # The frequency of the wall's movements (in Hz)
    a = 1 # The amplitude of the wave (in units)
    frequency = (f * math.pi) / frameRate # The real frequency, modified by the frame rate and pi.
    wallVelocity = frequency*a*np.cos(frequency*k) # The wall's velocity - allows me to give it momentum.
    wallPos = wallPos + wallVelocity # Move the wall by its velocity.

    # Movement, Collision and Reflection
    for i in range(0, len(particles)):
        # Move every particle along its velocity vector.
        particles[i].move(1, frameRate, wallPos=wallPos, wallVelocity=wallVelocity)
    for i, j in combinations(range(0, len(particles)), 2):
        # Collide each particle and make sure they aren't stuck inside it.
        Particle.collide(particles[i], particles[j])
        Particle.unstick(particles[i], particles[j])
    for i in range(0, len(particles)):
        # Reflect the particles on the walls.
        particles[i].reflect(wallPos, wallVelocity, wallMass=10)
    return wallPos

def anim(k):
    """ Animates and renders the frame. """
    print("Animating frame", k)
    wallPos = animate(k)
    return render.animate(particles, wallPos)

def init():
    """ Initializes the rendering process. """
    return render.start(particles)

# Set up the Writer object to render the animation to a file.
Writer = animation.writers['ffmpeg']
writer = Writer(fps=frameRate, metadata=dict(artist='Me'), bitrate=1800)

# Set up the animation.
ani = animation.FuncAnimation(render.figure(), anim, int(argv[1]), init_func=init, interval=1/frameRate)

# Start the rendering process!
ani.save('parts.mp4', writer=writer)
