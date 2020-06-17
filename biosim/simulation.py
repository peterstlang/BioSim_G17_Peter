# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Lowland, Highland, Desert, Water
from biosim.island import Island
from biosim.visuals import Visuals
import numpy as np
import pandas as pd


class BioSim:

    def __init__(self, island_map, ini_pop, seed,
                 ymax_animals=None, cmax_animals=None,
                 hist_specs=None, img_base=None, img_fmt="png"):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. ’png’
        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
        {’Herbivore’: 50, ’Carnivore’: 20}
        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
        {’weight’: {’max’: 80, ’delta’: 2}, ’fitness’: {’max’: 1.0, ’delta’: 0.05}}
        Permitted properties are ’weight’, ’age’, ’fitness’.
        If img_base is None, no figures are written to file.
        Filenames are formed as
        ’{}_{:05d}.{}’.format(img_base, img_no, img_fmt)
        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self.current_year = -1
        self.final_year = None
        self.island = Island(island_map).island
        # self.rgb_map = Island.create_rgb_map(island_map)

        if ymax_animals is None:
            ymax_animals = 20000

        self.ymax = ymax_animals

        if cmax_animals is None:
            cmax_herb = 20000
            cmax_carn = 20000
        else:
            cmax_herb = cmax_animals['Herbivore']
            cmax_carn = cmax_animals['Carnivore']

        self.cmax_herb = cmax_herb
        self.cmax_carn = cmax_carn

        self.add_population(ini_pop)
        self.seed = np.random.seed(seed)
        self.img_fmt = img_fmt

        self.visuals = Visuals()

        self.visuals.set_plots(rgb_map=self.rgb_map(island_map))

    @staticmethod
    def set_animal_parameters(species, params):
        """
        Set parameters for animal species.
        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == "Herbivore":
            Herbivore.set_parameters(params)
        if species == "Carnivore":
            Carnivore.set_parameters(params)

    @staticmethod
    def set_landscape_parameters(landscape, params):
        """
        Set parameters for landscape type.
        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape == "L":
            Lowland.set_parameters(params)
        elif landscape == "H":
            Highland.set_parameters(params)
        else:
            raise ValueError('Lowland and Highland are the'
                             'only ones that can have different parameters')

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.
        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)
        Image files will be numbered consecutively.
        """
        # self.x_axis_limit += num_years
        i = Island("WW")
        for yr in range(num_years):
            self.current_year += 1
            i.annual_cycle(self.island)

            # print( self.heatmap_of_population() )
            self.visuals.update_heat_maps(anim_distribution_dict=self.heatmap_of_population()
                                          )
            self.visuals.update_line_plt(self.heat_num_animals)

            self.visuals.update_year()

    def map_length(self):
        """
        The length of each map axis is calculated
        :return: 2 int
        We get the horizontal and vertical length of the map

        """
        lines = self.inserted_map.strip()
        lines = lines.split('\n')
        x_map = len(lines[0])
        y_map = len(lines)
        return x_map, y_map

    def rgb_map(self, str_raw_val):
        """
        The colored island map that is displayed in the plot
        is created, this code is heavily inspired by Hans' code in
        the example directory
        :param str_raw_val:
        :return:
        """
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow
        map_rgb = [[rgb_value[col] for col in row]
                   for row in str_raw_val.splitlines()]

        return map_rgb

    def heatmap_of_population(self):
        """

        :return: dict
        """
        row_num = np.shape(self.island)[0]
        column_num = np.shape(self.island)[1]

        h_matrix = np.zeros((row_num, column_num))
        c_matrix = np.zeros((row_num, column_num))

        for row, lines in enumerate(self.island):
            for col, cell in enumerate(lines):
                # print(cell.herb_list)
                h_matrix[row][col] = len(cell.herbivore)
                c_matrix[row][col] = len(cell.carnivore)

        animal_distribution_dict = {"Herbivore": h_matrix, "Carnivore": c_matrix}
        return animal_distribution_dict

    def add_population(self, population):
        """
        Add a population to the island
        :param population: List of dictionaries specifying population
        """
        # self.island.populate_cells(population)

        for cell_coord in population:
            x, y = cell_coord.get('loc')
            self.island[x][y].place_animals(cell_coord.get('pop'))

    @property
    def year(self):
        """Last year simulated."""
        return self.current_year

    @property
    def heat_num_animals(self):
        """Total number of animals on island."""
        total_herbivores = sum(sum(self.heatmap_of_population()['Herbivore']))
        total_carnivores = sum(sum(self.heatmap_of_population()['Carnivore']))
        animal_count_dict = {"Herbivore": total_herbivores, "Carnivore": total_carnivores}
        print(animal_count_dict)
        return animal_count_dict
        # return self.island.total_num_animals()

    @property
    def num_animals(self):
        """Total number of animals on island."""
        sum = 0
        for key, values in self.heat_num_animals.items():
            sum += values
        return sum

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return self.heat_num_animals

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        pass

# if __name__ == "__main__":
# i = Island('WW')
# print(i.create_rgb_map('WW'))
