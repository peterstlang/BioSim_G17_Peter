# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

from biosim.animals import Animal, Herbivore, Carnvivore
from biosim.landscape import Cell, Water, Lowland, Highland,
import numpy as np


class Island:
    """
    The island class.
    """
    type_of_landscape = {'W': Water, 'L': Lowland, 'H': Highland, 'D': Desert}

    def __init__(self, map):
        """
        The island class constructor
        :param map:
        """
        map = np.array([map[1, -1]])

    def annual_cycle(self):
        pass
