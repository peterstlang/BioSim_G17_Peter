# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

import numpy as np
import matplotlib.pyplot as plt
from biosim.island import Island
from biosim.landscape import Lowland, Water, Highland, Desert
from biosim.animals import Herbivore, Carnivore


# This code is straight from bishnu, im gonna rewrite it, i just need to get an
# understanding of plotting

class Visuals:
    """
    The class for all the visuals and plots
    """

    def __init__(self):
        """
        The constructor for visuals
        """
        self.steps = 0
        self.herb_data = []
        self.carn_data = []

    def set_plots(self, rgb_map=None, herbi_list=None, carn_list=None):
        """
        This will set up all the visuals for the project
        :param rgb_map:
        :param herbi_list:
        :param carn_list:
        :return:
        """
        self.fig = plt.figure(figsize=(32, 20))
        plt.axis('off')

        # HeatMap
        self.heatmap_herb = self.fig.add_axes([0.1, 0.28, 0.35, 0.3])  # llx, lly, w, h
        self.herb_axis = None
        self.heatmap_herb.title.set_text('Heatmap of Herbi')
        self.heatmap_herb.set_yticklabels([])
        self.heatmap_herb.set_xticklabels([])

        self.heatmap_carn = self.fig.add_axes([0.55, 0.28, 0.35, 0.3])  # llx, lly, w, h
        self.carn_axis = None
        self.heatmap_carn.title.set_text('Heat of Carni')
        self.heatmap_carn.set_yticklabels([])
        self.heatmap_carn.set_xticklabels([])

        # Island RGBmap
        self.island_ax = self.fig.add_axes([0.1, 0.65, 0.35, 0.3])  # llx, lly, w, h
        self.island_ax.title.set_text('Island Map')
        self.island_ax.set_yticklabels([])
        self.island_ax.set_xticklabels([])
        # Let us create island at the beginning since it is constant
        self.island_ax.imshow(rgb_map)

        # Histo Fitness
        self.fit_ax = self.fig.add_subplot(6, 3, 16)
        self.fit_ax.title.set_text('Fitness Histogram')
        self.fit_axis = None
        self.age_ax = self.fig.add_subplot(6, 3, 17)
        self.age_ax.title.set_text('Age Histogram')

        self.wt_ax = self.fig.add_subplot(6, 3, 18)
        self.wt_ax.title.set_text('Weight Histogram')

        # Line Plot num animals
        self.line_ax = self.fig.add_axes([0.55, 0.65, 0.35, 0.3])
        plt.pause(1)

    def update_heat_maps(self, anim_distribution_dict=None):
        """
        Updates the heat map as the animals move along the island
        :param anim_distribution_dict:
        :return:
        """
        if self.herb_axis is None:
            self.herb_axis = self.heatmap_herb.imshow(anim_distribution_dict['Herbivore'],
                                                      interpolation='nearest',
                                                      cmap="Greens", vmin=0, vmax=50)
            self.heatmap_herb.figure.colorbar(self.herb_axis, ax=self.heatmap_herb,
                                              orientation='horizontal',
                                              fraction=0.07, pad=0.04)
        else:
            self.herb_axis.set_data(anim_distribution_dict['Herbivore'])

        if self.carn_axis is None:
            self.carn_axis = self.heatmap_carn.imshow(anim_distribution_dict['Carnivore'],
                                                      interpolation='nearest',
                                                      cmap="OrRd", vmin=0, vmax=50)
            self.heatmap_carn.figure.colorbar(self.carn_axis, ax=self.heatmap_carn,
                                              orientation='horizontal',
                                              fraction=0.07, pad=0.04)
        else:
            self.carn_axis.set_data(anim_distribution_dict['Carnivore'])

        plt.pause(1)

    def update_line_plt(self, num_animals_per_species):
        self.herb_data.append(num_animals_per_species['Herbivore'])
        self.carn_data.append(num_animals_per_species['Carnivore'])
        length = len(self.carn_data)
        xlist = list(np.arange(length))

        self.line_ax.set_xlabel('Years')
        self.line_ax.set_ylabel('Number of Species')
        self.line_ax.plot(xlist, self.herb_data, '-', color='g')
        self.line_ax.plot(xlist, self.carn_data, '-', color='r')

    # def update_fitness_plt(self, fit_list_herb=None, fit_list_carn=None):
    #    self.fit_ax.clear()
    #    self.fit_ax.title.set_text('Fitness Histo')
    #    self.fit_ax.hist(fit_list_herb, bins=10, histtype='step', color='g')
    #    self.fit_ax.hist(fit_list_carn, bins=10, histtype='step', color='r')

    # def update_age_plt(self, age_list_herb=None, age_list_carn=None):
    #    self.age_ax.clear()
    #    self.age_ax.title.set_text('Fitness Histo')
    #    self.age_ax.hist(age_list_herb, bins=10, histtype='step', color='g')
    #    self.age_ax.hist(age_list_carn, bins=10, histtype='step', color='r')

    # def update_weight_plt(self, weight_list_herb=None, weight_list_carn=None):
    #    self.wt_ax.clear()
    #    self.wt_ax.title.set_text('Fitness Histo')
    #    self.wt_ax.hist(weight_list_herb, bins=10, histtype='step', color='g')
    #    self.wt_ax.hist(weight_list_carn, bins=10, histtype='step', color='r')

    def update_all_plots(self, distribution=None, num_species_dict=None):
        """
        This will update all the plots as the animals move along the island
        :param distribution:
        :param num_species_dict:
        :return:
        """
        self.steps += 1

        if self.herb_axis is None:
            self.herb_axis = self.heatmap_herb.imshow(distribution[0],
                                                      interpolation='nearest',
                                                      cmap='Greens',
                                                      vmin=0,
                                                      vmax=50)
            self.heatmap_herb.figure.colorbar(self.herb_axis,
                                              ax=self.heatmap_herb,
                                              orientation='horizontal',
                                              fraction=0.07,
                                              pad=0.04)
        else:
            self.herb_axis.set_data(distribution[0])

        if self.carn_axis is None:
            self.carn_axis = self.heatmap_carn.imshow(distribution[1],
                                                      interpolation='nearest',
                                                      cmap='OrRd',
                                                      vmin=0,
                                                      vmax=50)
            self.heatmap_carn.figure.colorbar(self.carn_axis,
                                              ax=self.heatmap_carn,
                                              orientation='horizontal',
                                              fraction=0.07,
                                              pad=0.04)
        else:
            self.carn_axis.set_data(distribution[1])

        self.update_line_plt(num_species_dict)

        # self.update_fitness_plt(fit_list_herb, fit_list_carn )
        # self.update_age_plt(age_list_herb,  age_list_carn)
        # self.update_weight_plt(weight_list_herb,  weight_list_carn)

        plt.pause(1e-6)
