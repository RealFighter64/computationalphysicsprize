import math
import numpy as np

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    if np.linalg.norm(vector) != 0:
        return vector / np.linalg.norm(vector)
    else:
        print("Wait what", vector)
        return np.array([1, 0])

class Particle:
    """ A single particle object for use in the sound simulation. """

    def __init__(self, position, size, mass, velocity):
        self.position = position
        self.size = size
        self.mass = mass
        self.velocity = velocity

    def distance(self, part):
        """ Get the distance between this particle and another one. """
        return np.sqrt((self.position[0]-part.position[0])**2 + (self.position[1]-part.position[1])**2)

    def set_vel(self, vel):
        """ Sets the velocity of the particle. """
        self.velocity = vel

    def add_vel(self, vel):
        """ Add the velocity to the current velocity of the particle. """
        self.velocity += vel

    @staticmethod
    def collide(self, part, frameRate=15):
        """ Collides two particles together """
        dist = Particle.distance(self, part)
        collDist = self.size + part.size
        if dist <= collDist:
            part.resolveBounce(self,part,overlap=dist<collDist, frameRate=frameRate)
        else:
            pass

    @staticmethod
    def resolveBounce(part1, part2, overlap=False, frameRate=15):
        """ Resolves the bounce velocity between two particles. """
        v1, v2 = part1.velocity, part2.velocity
        p1, p2 = part1.position, part2.position
        m1, m2 =     part1.mass,     part2.mass

        # Total Velocity
        vt = v1 + v2

        # The point of contact between the two particles.
        unit_norm = p2 - p1
        unit_norm = unit_vector(unit_norm)
        unit_tan = np.array([-unit_norm[1],unit_norm[0]])

        # The velocity vectors put in the context of the two new unit vectors.
        v1n = np.dot(unit_norm,v1)
        v1t = np.dot( unit_tan,v1)
        v2n = np.dot(unit_norm,v2)
        v2t = np.dot( unit_tan,v2)

        v1t_prime_scal = v1t
        v2t_prime_scal = v2t

        # The scale factor for the collision for each particle.
        v1n_prime_scal = (v1n*(m1 - m2) + 2*m2*v2n)/(m1 + m2)
        v2n_prime_scal = (v2n*(m2 - m1) + 2*m1*v1n)/(m1 + m2)

        # The new velocity components for each particle.
        v1n_prime = v1n_prime_scal*unit_norm
        v1t_prime = v1t_prime_scal* unit_tan
        v2n_prime = v2n_prime_scal*unit_norm
        v2t_prime = v2t_prime_scal* unit_tan

        # The new velocity vectors for the particles.
        v1_prime = v1n_prime + v1t_prime
        v2_prime = v2n_prime + v2t_prime

        # New total velocity
        vt_prime = v1_prime + v2_prime
        #print(vt_prime)

        # Update the velocities.
        part1.set_vel(v1_prime)
        part2.set_vel(v2_prime)

    def unstick(part1, part2):
        """ Makes sure that the two particles don't overlap and get stuck. """
        v1, v2 = part1.velocity, part2.velocity
        p1, p2 = part1.position, part2.position

        unit_norm = p2 - p1
        unit_norm = unit_vector(unit_norm)

        # Distance between the two particles.
        dist = np.linalg.norm(p1 - p2)

        # Expected distance between the two particles.
        collDist = part1.size + part2.size

        if dist < collDist:
            # Find the midpoint between the two particles.
            midpoint = unit_norm * (dist / 2)
            p1_prime = p1
            p2_prime = p2
            overlap = collDist - dist
            
            # Snap the two particles outside of each other's radius.
            p1_prime = p1 - unit_norm * overlap
            p2_prime = p2 + unit_norm * overlap

            # Set the particles' new positions.
            part1.position = p1_prime
            part2.position = p2_prime

    def momentum(self):
        """ Get the momentum of the particles. """
        return self.mass * self.velocity
    
    def reflect(self, wallPos, wallVelocity, wallMass=1):
        """ Reflect the particles off of the walls. """
        if self.position[0] + self.size >= 10 or self.position[0] - self.size <= wallPos:
            if self.position[0] + self.size >= 10:
                self.position[0] = 10 - self.size
                self.velocity = np.array([-self.velocity[0], self.velocity[1]])
            elif self.position[0] - self.size <= wallPos:
                self.position[0] = wallPos + self.size
                # Slightly different from the others, because the moving wall has momentum that it passes onto the other particles.
                self.velocity = np.array([wallVelocity*wallMass/self.mass, self.velocity[1]])
            
        if self.position[1] + self.size >= 10 or self.position[1] - self.size <= -10:
            if self.position[1] + self.size >= 10:
                self.position[1] = 10 - self.size
            elif self.position[1] - self.size <= -10:
                self.position[1] = -10 + self.size
            self.velocity = np.array([self.velocity[0], -self.velocity[1]])

    def move(self, time, frameRate, reflect=False, wallPos=-10, wallVelocity=0):
        """ Move the particles by their velocity vectors. """
        self.position = self.position + self.velocity * (time / frameRate)