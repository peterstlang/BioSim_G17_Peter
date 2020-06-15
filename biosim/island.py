# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

from biosim.landscape import Water, Lowland, Highland, Desert
from biosim.animals import Herbivore, Carnivore
import numpy as np
import textwrap


class Island:
    """
    The island class.
    """
    type_of_landscape = {'W': Water, 'L': Lowland, 'H': Highland, 'D': Desert}
    valid_landscape_types = (Lowland, Highland, Desert)
    anim_species = {'Herbivore': Herbivore, 'Carnivore': Carnivore}

    def __init__(self, island_map_as_string):
        """
        The island class constructor
        :param map:
        """
        island_map_as_string = textwrap.dedent(island_map_as_string)
        self.island = self.create_map(island_map_as_string)

    def create_map(self, multi_line_string):
        # type_of_landscape = {'W': Water, 'L': Lowland, 'H': Highland, 'D': Desert}

        multi_line_string = multi_line_string.strip()
        list_of_lists = [list(cell) for cell in multi_line_string.splitlines()]
        # print(list_of_lists)
        cells_object_list_of_list = []
        for i, row in enumerate(list_of_lists):
            for j, cell in enumerate(row):
                cells_object_list_of_list.append(
                    self.type_of_landscape[list_of_lists[i][j]])

        return cells_object_list_of_list

    def populate(self, population):
        pass

    def annual_cycle(self):
        pass

    def get_adjacent_cells(self, current_cell_coord):
        """

        :param current_cell_coord:
        :return: a list of the 4 adjacent cells
        """
        x, y = current_cell_coord
        four_adj_cells = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return four_adj_cells

        #list_adj_cell = []
        #for cell in four_adj_cells:
        #    for coord in cell:
        #        list_adj_cell.append(coord)



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


if __name__ == "__main__":
    I = Island("""
    WWWW
    WHHW
    WLLW
    WWWW""")

    I.get_adjacent_cells((1, 1))
