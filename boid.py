"""
Implementation of Craig W. Reynolds' bird flocking
behavior simulation in python using the p5 library

boid.py provides the Boid class to create
and maintain individual boids in a  flock.

Author: Sarah Hancock
"""

# Note: user must install p5 (pip install p5)
from p5 import *
from enum import Enum
from sklearn.neighbors import KDTree
import numpy as np

class Status(Enum):
    S = (255, 255, 255)
    I = (255, 0, 0)
    R = (0, 0, 255)
    D = (25, 25, 25)

class Boid():
    """
    individual organisms of the flock/herd/school could be
    birds, sheep, or fish, etc. so we will refer to them as "boids"
    """
    def __init__(self, x, y, width, height):
        """
        init for an individual boid: establishing
        its position, velocity, and acceleration
        :param: x The x coordinate for the position of the boid
        :param: y The y coordinate for the position of the boid
        :param: width The width of the environment
        :param: height The height of the environment
        """

        # so the boid knows the width of its environment
        self.width = width
        # so the boid knows the height of its environment
        self.height = height

        #position
        self.position = Vector(x, y)
        #velocity
        vec = (np.random.rand(2) - 0.5)*15
        #vec = vec / np.sum(vec)
        print(np.sum(vec))
        self.velocity = Vector(*vec)
        #acceleration
        vec = (np.random.rand(2) - 0.5)/2
        self.acceleration = Vector(*vec)

        ## The following attributes of
        # max force affects strength of separation and cohesion vectors
        self.max_force = 0.5
        # setting max speed helps give smoother movement
        self.max_speed = 10
        # the max distance when another boid can still be considered "local"
        self.perception = 10

        ### SIR STATUS ###
        self.status = Status.S

    def set_status(self, status):
        self.status = status

    def show(self):
        """
        shows a boid's current position in the environment
        with "beak" pointed in the direction of its velocity
        """
        # Insert Status Check + Coloring
        
        stroke(*self.status.value)
        fill(*self.status.value)
        circle((self.position.x, self.position.y), radius = 7)


    def update(self, neighbor_tree, boids):
        """
        update boid's position and velocity
        """
        # update position
        self.position += self.velocity
        # update velocity
        # self.velocity += self.acceleration
        # # limit max speed
        # if np.linalg.norm(self.velocity) > self.max_speed:
        #     self.velocity = (self.velocity /
        #                      np.linalg.norm(self.velocity)*self.max_speed)
        
        # If a neighboring boid is infected, infect this boid.
        # TODO: Flip check from Infected --> Susceptible at tipping point
        if self.status == Status.I:
            neighbors = self.get_nearest_neighbor(neighbor_tree)
            print(neighbors)
            for neighbor_index in neighbors:
                if boids[neighbor_index].status == Status.S:
                    boids[neighbor_index].set_status(Status.I)
                    break


    def edges(self):
        """
        when boid leaves the environment, have it reappear on the opposite side
        if runs off the top, reappear on the bottom
        if runs off the side, reappear on the other side
        """
        # check side boundaries
        if self.position.x > self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width

        # check top and bottom boundaries
        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height

    # def apply_behaviour(self, boids):
    #     """
    #     applies the 3 key behaviors as stated by Craig W. Reynolds
    #     :param: boids The list of all boid objects
    #     """
    #     # enforce separation of boids
    #     separation = self.separation(boids)
    #     # adjust alignment of boids
    #     alignment = self.align(boids)
    #     # promote cohesion of boids
    #     cohesion = self.cohesion(boids)

    #     sep_weight = 1
    #     al_weight = 1
    #     co_weight = 1.5

    #     # can adjust the weights of each of these vals to change flock behavior
    #     total_force = (separation*sep_weight
    #                    + alignment*al_weight
    #                    + cohesion*co_weight)
    #     # adjust accelaration by applying all forces
    #     self.acceleration = total_force

    # def separation(self, boids):
    #     """
    #     Steers a single boid away from running into local boids within
    #     its perception. This helps boids avoid running into eachother
    #     :param: boids The list of all boid objects
    #     :returns: steering A vector which acts as a force to guide separation
    #     """
    #     steering = Vector(*np.zeros(2))
    #     total = 0
    #     avg_vector = Vector(*np.zeros(2))

    #     for boid in boids:
    #         # check each boid in the current boid's perception range.
    #         distance = np.linalg.norm(boid.position - self.position)
    #         if self.position != boid.position and distance < self.perception:
    #             diff = self.position - boid.position
    #             # difference should be inversly proportional to distance
    #             # the closer boids have a higher impact than the further boids
    #             diff /= distance
    #             avg_vector += diff
    #             total += 1
    #     # only adjust steering force when there are
    #     # nearby boids to affect flight direction
    #     if total > 0:
    #         avg_vector = Vector(*avg_vector)

    #         steering = avg_vector - self.velocity
    #         # adjust norm based on max_force
    #         if np.linalg.norm(steering) > self.max_force:
    #             steering = (steering) * self.max_force

    #     return steering


    # def align(self, boids):
    #     """
    #     Steers a single boid to match average velocity of local
    #     boids within its perception. This promotes alignment of the flock
    #     :param: boids The list of all boid objects
    #     :returns: steering A vector which acts as a force to guide alignment
    #     """
    #     steering = Vector(*np.zeros(2))
    #     total = 0
    #     avg_vec = Vector(*np.zeros(2))

    #     for boid in boids:
    #         # check if the other boid is within current boid's perception range
    #         if np.linalg.norm(boid.position - self.position) < self.perception:
    #             avg_vec += boid.velocity
    #             total += 1
    #     # only adjust steering force when there are
    #     # nearby boids to affect flight direction
    #     if total > 0:
    #         avg_vec /= total
    #         avg_vec = Vector(*avg_vec)
    #         avg_vec = (avg_vec /np.linalg.norm(avg_vec)) * self.max_speed
    #         steering = avg_vec - self.velocity

    #     return steering


    # def cohesion(self, boids):
    #     """
    #     Steer a single boid towards the center of mass of local biods
    #     within its perception. This promotes cohesion within the flock
    #     :param: boids The list of all boid objects
    #     :returns: steering A vector which acts as a force to guide cohesion
    #     """
    #     steering = Vector(*np.zeros(2))
    #     total = 0
    #     center_of_mass = Vector(*np.zeros(2))

    #     for boid in boids:
    #         # check if the other boid is within current boid's perception range
    #         if np.linalg.norm(boid.position - self.position) < self.perception:
    #             center_of_mass += boid.position
    #             total += 1
    #     # only adjust steering force when there are
    #     # nearby boids to affect flight direction
    #     if total > 0:
    #         center_of_mass /= total
    #         center_of_mass = Vector(*center_of_mass)
    #         vec_to_com = center_of_mass - self.position
    #         if np.linalg.norm(vec_to_com) > 0:
    #             vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
    #         steering = vec_to_com - self.velocity

    #         # adjust norm based on max_force
    #         if np.linalg.norm(steering)> self.max_force:
    #             steering = (steering /np.linalg.norm(steering)) * self.max_force

    #     return steering

#### METHODS WRITEN BY CALEB AND MAR ####
    def get_nearest_neighbor(self, kdt, radius=50):
        neighbors = kdt.query_radius(np.array([self.position[:-1]]), r=radius)
        return neighbors[0]

def make_neighbor_tree(boids):
    positions = np.array([boid.position[:-1] for boid in boids])
    return KDTree(positions)