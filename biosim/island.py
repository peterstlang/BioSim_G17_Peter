# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

from biosim.landscape import Lowland, Highland, Desert, Water
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
        :param island_map_as_string: multi line string
        the map is created using a designated method
        """
        island_map_as_string = textwrap.dedent(island_map_as_string)
        self.island = self.create_map(island_map_as_string)
        # self.rgb_map = self.create_rgb_map(island_map_as_string)

    def create_map(self, multi_line_string):
        """
        The map is created. First we do a bunch of checks to ensure
        that the map we get is actually a valid map. Then the map is created
        :param multi_line_string: multi line string
        :return: nested list
        The map is created as a list of lists
        """
        # type_of_landscape = {'W': Water, 'L': Lowland, 'H': Highland, 'D': Desert}

        multi_line_string = multi_line_string.strip()
        list_of_lists = [list(cel) for cel in multi_line_string.splitlines()]

        top_row = list_of_lists[0]
        bottom_row = list_of_lists[-1]
        left_col = [cellcol[0] for cellcol in list_of_lists]
        right_col = [cellcol[-1] for cellcol in list_of_lists]

        if set(top_row + bottom_row + left_col + right_col) != {'W'}:
            raise ValueError('edges has to be water!')

        first_length = len(list_of_lists[0])
        for listof in list_of_lists:
            if len(listof) != first_length:
                raise ValueError('Map is not of equal length')

        for listof in list_of_lists:
            for strings in listof:
                if strings not in ['W', 'L', 'H', 'D']:
                    raise ValueError('Invalid landscape')

        cells_object_list_of_list = []
        for i, row in enumerate(list_of_lists):
            one_d_list = []
            for j, cell in enumerate(row):
                one_d_list.append(self.type_of_landscape[list_of_lists[i][j]]())
            cells_object_list_of_list.append(one_d_list)

        return cells_object_list_of_list

    def populate_cells(self, population):
        """
        The population is taken in and placed in the cells on the island.
        :param population:
        """

        for cell_coord in population:
            x, y = cell_coord.get('loc')
            self.island[x][y].place_animals(cell_coord.get('pop'))

    def annual_cycle(self, input_island):
        """
        The entire cycle is handled. This will repeat once every year
        :param input_island: the map
        """
        self.animals_feed_all(input_island)
        self.animals_procreate(input_island)
        self.start_migration(input_island)
        self.animals_age(input_island)
        self.animals_weightloss(input_island)
        self.animals_die(input_island)

    @staticmethod
    def get_adjacent_cells(current_cell_coord):
        """
        The coordinates of the current cell is taken in,
        and the four adjacent cells are returned
        :param current_cell_coord: tuple
        :return: a list of the 4 adjacent cells
        """
        x, y = current_cell_coord
        four_adj_cells = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return four_adj_cells

    def start_migration(self, input_island):
        """
        This handles how animals migrate. First we ensure that the animals can migrate
        by setting the has_migrated flag to false. Due to the way my island is set up
        we need the triple for-loops.
        It then checks that the cell is habitable, then it proceeds to migrate the animals
        Lastly the animals are removed from the current cell and added to the one they have
        migrated too.
        :param input_island: nested list
        """
        for row, rows_of_cell_obj in enumerate(input_island):
            for col, cel in enumerate(rows_of_cell_obj):
                for anim in cel.herbivore + cel.carnivore:
                    anim.set_has_migrated(False)

        for row, rows_of_cell_obj in enumerate(input_island):
            for col, cel in enumerate(rows_of_cell_obj):

                if cel.habitable_cell:
                    adjacent_cord = self.get_adjacent_cells((row, col))
                    adjacent_cells = [input_island[row][col] for row, col in adjacent_cord]
                    animals_dct = cel.migration(adjacent_cells)
                    for migrating_cell, values in animals_dct.items():
                        if migrating_cell.habitable_cell and values:
                            migrating_cell.add_migrated_animals(values)
                            cel.remove_animals(values)

    @staticmethod
    def animals_feed_all(input_island):
        """
        Here we iterate through all the cells and feed everyone
        in each cell
        :param input_island: the island
        """
        for cel in np.asarray(input_island).flatten():
            cel.feed_animals()

    @staticmethod
    def animals_procreate(input_island):
        """
        Here we iterate through all the cells and procreate
        all the animals in each cell
        :param input_island: the island
        """
        for cel in np.asarray(input_island).flatten():
            cel.procreation_animals()

    @staticmethod
    def animals_age(input_island):
        """
        Here we iterate through all the cells and
        age the animals
        :param input_island: the island
        """
        for cel in np.asarray(input_island).flatten():
            cel.aging_animals()

    @staticmethod
    def animals_weightloss(input_island):
        """
        Here we iterate through all the cells and
        make the animals lose weight
        :param input_island: the island
        """
        for cel in np.asarray(input_island).flatten():
            cel.animals_yearly_weight_loss()

    @staticmethod
    def animals_die(input_island):
        """
        Here we iterate through all the cells and
        make the animals die
        :param input_island: the island
        """
        for cel in np.asarray(input_island).flatten():
            cel.animals_die()

    def get_num_animals_per_species(self):
        """
        The number of animals per species is given
        :return: Dict
        Returns a dictionary with key: Animal species, and value: len of each list
        """

        animals_per_species = {}
        num_herbs = 0
        num_carns = 0

        for cell in np.asarray(self.island).flatten():
            num_herbs += cell.num_herbs
            num_carns += cell.num_carns

        animals_per_species['Herbivore'] = num_herbs
        animals_per_species['Carnivore'] = num_carns

        return animals_per_species

    def total_num_animals(self):
        """
        This lets us check the total number of animals on the island
        :return: int
        """
        num_animals = 0
        for cell in np.asarray(self.island).flatten():
            num_animals += cell.total_num_animals()

        return num_animals

# if __name__ == "__main__":
#    I = Island("""
#    WWWW
#    WHHW
#    WLLW
#    WWWW""")
#    for cell in np.asarray(I.island).flatten():
#        print(cell)

# Spør Ta om place_animals endringen og hvordan det påvirker resten

# print( np.asarray(I.island).shape)

# I.island[1][1].herbivores = [Herbivore() for _ in range(50)]
# print(len(I.island[1][1].herbivores))

# I.start_migration()
# print(len(I.island[1][1].herbivores))
