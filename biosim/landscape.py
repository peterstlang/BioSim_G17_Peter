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

    @classmethod
    def set_parameters(cls, parameters):
        pass

    def __init__(self):
        self.fodder = 0
        self.herbivores = []

    def grow_fodder(self):
        pass

    def place_animals(self, list_of_animals):
        pass

    def feed_herbivores(self):
        for herb in self.herbivores:
            food_available = self.fodder
            herb.eat(food_available)
            self.fodder -= food_available

    def feed_carnivores(self):
        pass

    def procreation_herbivores(self):
        herb_offpsring = []


    def aging_animals(self):
        for animals in self.herbivores:
            animals.update_age()

    def animals_weight_loss(self):
        pass

    def animals_die(self):
        pass

    def get_num_animals(self):
        pass


class Water(Cell):
    pass


class Desert(Cell):
    pass


class Lowland(Cell):
    pass


class Highland(Cell):
    pass
