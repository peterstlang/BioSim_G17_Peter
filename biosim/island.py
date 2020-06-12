# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

from biosim.landscape import Cell, Water, Lowland, Highland, Desert
from biosim.animals import Animal, Herbivore, Carnivore
import numpy as np


class Island:
    """
    The island class.
    """
    type_of_landscape = {'W': Water, 'L': Lowland, 'H': Highland, 'D': Desert}
    valid_landscape_types = (Lowland, Highland, Desert)

    def __init__(self, island_map_as_string):
        """
        The island class constructor
        :param map:
        """
        self.island = self.create_map(island_map_as_string)

    def populate(self, population):
        pass

    def annual_cycle(self):
        pass

    def get_adjacent_cells(self, current_cell_coord):
        """

        :param current_cell_coord:
        :return: a list of the 4 adjacent cells
        """
        pass

    def animals_feed_all(self):
        pass

    def animals_procreate(self):
        pass

    def animals_migrate(self):
        pass

    def animals_age(self):
        pass

    def animals_weightloss(self):
        pass

    def animals_die(self):
        pass
