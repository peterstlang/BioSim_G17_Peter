# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

from biosim.animals import Animal, Herbivore, Carnivore
import numpy as np


class Cell:
    """
    cell superclass
    """
    parameters = {}

    def __init__(self):
        self.fodder = 0
        self.animals_in_cell = {}

    @classmethod
    def set_parameters(cls):
        pass

    def grow_fodder(self):
        pass

    def feed_animals(self):
        pass

    def procreation(self):
        pass

    def aging_animals(self):
        pass

    def animals_weight_loss(self):
        pass

    def animals_die(self):
        pass


class Water(Cell):
    pass


class Desert(Cell):
    pass


class Lowland(Cell):
    pass


class Highland(Cell):
    pass
