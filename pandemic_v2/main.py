"""
Implementation of Craig W. Reynolds' bird flocking
behavior simulation in python using the p5 library

Author: Sarah Hancock
"""
from p5 import *
import numpy as np
from boid import *


width = 1200 # width of screen environment for boids
height = 750 # height of screen environment for boids


# Create flock of boids from initiating multiple boids at once
flock_size = 100
flock = [Boid(np.random.rand(1)*width, np.random.rand(1)*height, width, height) for _ in range(flock_size)]
flock[round(np.random.rand() * flock_size)].set_status(Status.I)

def setup(): 
    """
    set up dimensions for the screen environment
    """
    #this happens just once
    size(width, height) # set the size of the environment

def draw():
    """
    draw the current state of all boids in the environment
    this happens every time frame
    """
    background(30, 100, 110) # background color

    neighbor_tree = make_neighbor_tree(flock)
    for boid in flock:
        boid.show()
        # boid.apply_behaviour(flock)
        boid.update(neighbor_tree, flock)  #TODO: During update, check for collisions
        boid.edges()
run()
