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
import numpy as np
from population import *
from population import Person
from population import make_neighbor_tree
# Initialize window dimensions
height = 500
width = 500

# Initialize population
pop_size = 50
population = [Person(np.random.rand()*width, np.random.rand()*height, width, height) for _ in range(pop_size)]
population[round(np.random.rand() * pop_size)].set_status(Status.I)  # 

# Initialize the frame counter for timeline of spread
frame_index = 0

def setup():
    """
    Set up the dimensions for the environment for the
    people
    """
    size(width,height)

def draw():
    """
    Draw the state at each frame of where the people are
    in their environment
    """
    # Increment the frame counter
    global frame_index
    frame_index += 1 
    # Set the background to black
    background(0,0,0)

    # Calculate the spatially ordered tree for the
    # population
    neighbor_tree = make_neighbor_tree(population)
        
    # Iterate through the population to show each person,
    # update the velocity and status of each person
    # depending on collisions, and update the velocity
    # if a person collided with the edge of the 
    # environment
    for person in population:
        person.show()
        person.update(neighbor_tree, population)
        person.edge_check()
run()