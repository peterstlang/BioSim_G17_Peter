# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

import numpy as np
import matplotlib.pyplot as plt


class Visuals:
    """
    The class for all the visuals and plots
    """

    def __init__(self):
        """
        Constructor for visuals
        """
        self.fig = plt.figure(figsize=(32, 20))
        self.steps = 0
        self.herb_data_list = []
        self.carn_data_list = []

        self.heatmap_herb = None
        self.herb_axis = None
        self.heatmap_carn = None
        self.carn_axis = None
        self.island_axis = None
        self.line_plot_axis = None
        self.year_counter = None
        self.changing_year = None

    def set_plots(self, rgb_map=None):
        """

        :param rgb_map:
        :return:
        """
        plt.axis('off')

        self.heatmap_herb = self.fig.add_axes([0.1, 0.2, 0.35, 0.3])  # llx, lly, w, h
        self.heatmap_herb.title.set_text('Heatmap of Herbi')
        self.heatmap_herb.set_yticklabels([])
        self.heatmap_herb.set_xticklabels([])

        self.heatmap_carn = self.fig.add_axes([0.55, 0.2, 0.35, 0.3])  # llx, lly, w, h
        self.heatmap_carn.title.set_text('Heat of Carni')
        self.heatmap_carn.set_yticklabels([])
        self.heatmap_carn.set_xticklabels([])

        self.island_axis = self.fig.add_axes([0.1, 0.65, 0.35, 0.3])  # llx, lly, w, h
        self.island_axis.title.set_text('Island Map')
        self.island_axis.set_yticklabels([])
        self.island_axis.set_xticklabels([])
        self.island_axis.imshow(rgb_map)

        self.line_plot_axis = self.fig.add_axes([0.55, 0.65, 0.35, 0.3])
        plt.pause(1)

        self.year_counter = self.fig.add_axes([0.4, 0.5, 0.05, 0.05])
        self.year_counter.axis('off')
        self.changing_year = self.year_counter.text(0.2, 0.5, "Year: " + str(0)
                                                    , fontdict={'weight': 'bold', 'size': 16})

    def update_year(self):
        self.steps += 1
        self.changing_year.set_text("Year: " + str(self.steps))

    def update_heat_maps(self, anim_distribution_dict=None):
        """
        Updates the heat map as the animals move along the island
        :param anim_distribution_dict:
        :return:
        """

        if self.herb_axis is None:
            self.herb_axis = self.heatmap_herb.imshow(anim_distribution_dict['Herbivore'],
                                                      interpolation='nearest',
                                                      cmap="Greens", vmin=0, vmax=200)
            self.heatmap_herb.figure.colorbar(self.herb_axis, ax=self.heatmap_herb,
                                              orientation='horizontal',
                                              fraction=0.07, pad=0.04)
        else:
            self.herb_axis.set_data(anim_distribution_dict['Herbivore'])

        if self.carn_axis is None:
            self.carn_axis = self.heatmap_carn.imshow(anim_distribution_dict['Carnivore'],
                                                      interpolation='nearest',
                                                      cmap="OrRd", vmin=0, vmax=200)
            self.heatmap_carn.figure.colorbar(self.carn_axis, ax=self.heatmap_carn,
                                              orientation='horizontal',
                                              fraction=0.07, pad=0.04)
        else:
            self.carn_axis.set_data(anim_distribution_dict['Carnivore'])

        plt.pause(1)

    def update_line_plt(self, num_animals_per_species):
        """

        :param num_animals_per_species:
        :return:
        """

        self.herb_data_list.append(num_animals_per_species['Herbivore'])
        self.carn_data_list.append(num_animals_per_species['Carnivore'])
        length = len(self.carn_data_list)
        xlist = list(np.arange(length))

        self.line_plot_axis.set_xlabel('Years')
        self.line_plot_axis.set_ylabel('Number of Species')
        self.line_plot_axis.plot(xlist, self.herb_data_list, '-', color='g')
        self.line_plot_axis.plot(xlist, self.carn_data_list, '-', color='r')
