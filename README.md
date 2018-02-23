## Computational Physics Prize - William Gooch

This solution to the problem works by simulating individual particles, allowing them to
collide and then moving a wall back and forth in order to oscillate them. The moving patterns
in the background are a pressure map made in order to show the patterns of sound travelling
through the particles.

#### Running the program
Unfortunately, the simulation, due to the limitations of Python and the methods of rendering
and calculation used, cannot run in real-time. The program must be run in advance, producing
a video file with the animation on it. Sadly the program takes a very long time to run, so
in order to help demostrate the capabilities of the program, I've pre-rendered some animations
put in a folder called 'examples'.

The program requires both numpy and matplotlib be installed on your local version of Python.
To run it, just type:

    python main.py <number of particles> <particle size> <number of frames>

The program runs at 15 frames per second.
