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
        """

        :param multi_line_string:
        :return:
        """
        # type_of_landscape = {'W': Water, 'L': Lowland, 'H': Highland, 'D': Desert}

        multi_line_string = multi_line_string.strip()
        list_of_lists = [list(cell) for cell in multi_line_string.splitlines()]

        top_row = list_of_lists[0]
        bottom_row = list_of_lists[-1]
        left_col = [cellcol[0] for cellcol in list_of_lists]
        right_col = [cellcol[-1] for cellcol in list_of_lists]

        if set(top_row + bottom_row + left_col + right_col) != {'W'}:
            raise ValueError('edges has to be water!')


        cells_object_list_of_list = []
        for i, row in enumerate(list_of_lists):
            one_d_list = []
            for j, cell in enumerate(row):
                one_d_list.append(self.type_of_landscape[list_of_lists[i][j]]())
            cells_object_list_of_list.append(one_d_list)

        # print(np.asarray(cells_object_list_of_list).shape)
        return cells_object_list_of_list

    def populate_cells(self, population):

        for cell_coord in population:
            x, y = cell_coord.get('loc')
            self.island[x][y].place_animals(cell_coord.get('pop'))

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

    def start_migration(self):
        for row, rows_of_cell_obj in enumerate(self.island):
            for col, cell in enumerate(rows_of_cell_obj):
                for anim in cell.herbivores + cell.carnivores:
                    anim.set_has_migrated(False)
                    # anim.animals_has_migrated = False # Do it through a function in animal class later

        for row, rows_of_cell_obj in enumerate(self.island):
            # print(rows_of_cell_obj)
            for col, cell in enumerate(rows_of_cell_obj):

                if cell.habitable_cell:
                    adjacent_cord = self.get_adjacent_cells((row, col))
                    adjacent_cells = [self.island[row][col] for row, col in adjacent_cord]
                    animals_dct = cell.migration(adjacent_cells)
                    for migrating_cell, values in animals_dct.items():
                        if values:
                            migrating_cell.place_animals(values)
                            cell.remove_animals(values)

                    # gets a dictionary of [cell1: [], cell2[] )
                    # cell1.add_immigrants()
                    # cell.remove_animals()

    # def animal_loc_after_migration(self, migrated_anims_dct):
    #    relocated_animals = []

    #    for cell in migrated_anims_dct.keys():
    #        if cell.habitable_cell:
    #            cell.values()

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
    print(I)

    # Spør Ta om place_animals endringen og hvordan det påvirker resten

    # print( np.asarray(I.island).shape)

    #I.island[1][1].herbivores = [Herbivore() for _ in range(50)]
    #print(len(I.island[1][1].herbivores))

    #I.start_migration()
    #print(len(I.island[1][1].herbivores))
