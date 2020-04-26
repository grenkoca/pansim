"""
Inspired by 3Blue1Brown's simulation of the COVID 19
pandemic as well as code by Sarah Hancock for the
implementation 
"""

from p5 import *
from enum import Enum
import numpy as np

class Status(Enum):
    S = (255, 255, 255)
    I = (255, 0, 0)
    R = (0, 0, 255)
    D = (25, 25, 25)


class Person():
    