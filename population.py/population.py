"""
Inspired by 3Blue1Brown's simulation of the COVID 19
pandemic as well as code by Sarah Hancock for the
implementation of Craig W. Reynolds' bird flocking
behavior simulation.

We use the p5 library for graphics and collision
detection.

Authors: Marianna Ghirardelli and Caleb Grenko
"""

from p5 import *
from enum import Enum
import numpy as np
from sklearn.neighbors import NearestNeighbors

class Status(Enum):
    # Color for susceptible people will be white
    S = (255, 255, 255)
    # Color for infected people will be red
    I = (255, 0, 0)
    # Color for recovered people will be blue
    R = (0, 0, 255)
    # Color for deceased people will be dark gray
    D = (25, 25, 25)


class Person():
    """
    This class represents the individual people within our
    population who is susceptible, infected, recovered,
    or deceased.
    """

    def __init__(self, x, y, width, height):
        """
        Initialization for the individual people.  This
        establishes the position, velocity, and
        acceleration of the individual people.
        Parameters:
            x - the x coordinate for the position of the person
            y - the y coordinate for the position of the person
            width - the width of the environment
            height - the height of the environment
        """

        # The person needs to know the constraints of
        # its environment
        self.width = width
        self.height = height

        # Set the position of the person
        self.position = Vector(x,y)

        # Set the velocity of the person.  In one
        # simulation in which everyone is free to move,
        # we randomize but normalize each velocity vector
        # so everyone moves at the same speed
        velocity = (np.random.rand(2) - 0.5)*15
        self.velocity = Vector(*velocity)

        # In other simulations, ... IMPLEMENT OTHER
        # SIMULATIONS VELOCITY PATTERNS

        # Set the SIRD status
        self.status = Status.S

    def set_status(self, status):
        """
        Sets the status of a person according to the
        SIRD model
        Parameters:
            status - the new status to be set
        """
        self.status = status

    def show(self):
        """
        Shows the person's current position in the
        environment.  Each person is going to be
        represented as a circle.  The color will depend on
        their SIRD status
        """
        stroke(*self.status.value)
        fill(*self.status.value)
        circle((self.position.x, self.position.y), radius = 7)

    def update(self, neighbor_tree, population):
        """
        Updates the position and status of each person
        in the population each round
        Parameters:
            neighbor_tree -     the KDTree that contains
                                the population spatially
                                ordered
            population -    the list of all people objects
                            in the environment
        """
        # Update the position
        self.position += self.velocity

        # If a neighboring person is infected, infect
        # the current person
        # TODO: Flip check from Infect --> Susceptible
        # at tipping point
        if self.status == Status.S:
            neighbors = self.get_nearest_neighbor(neighbor_tree)
            for neighbor_index in neighbors:
                if boids[neighbor_index].status == Status.I:
                    self.set_status(Status.I)
                    # TODO: x% change of getting infected per
                    # infected neighbor
                    break

    def get_nearest_neighbors(self, kdt, radius=100):
        """
        Finds the nearest neighbors to a person within a
        certain radius according to the KDTree that
        spatially ordered the people in the environment.
        Parameters:
            kdt -   the KDTree that contains the people
                    in spatial order
            radius -    the radius around the person.
                        This is by default 100, but could
                        be increased or decreased as
                        desired
        Returns:
            a list of the neighbors within the radius
        """
        neighbors = kdt.query_radius(np.array([self.position[:-1]]), r = radius)
        return neighbors[0][1:]

def make_neighbor_tree(population):
    """
    Makes the spatially ordered tree of people
    Parameter:
        population -    The list of people in the
                        population
    Returns:
        the tree of the population spatially ordered
    """
    positions = np.array([boi.poisition[:-1] for boid in boids])
    return KDTree(positions)
