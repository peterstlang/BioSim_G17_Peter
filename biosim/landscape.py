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
        """

        :param parameters:
        :return:
        """

        if not isinstance(parameters, dict):
            raise TypeError('parameters must be of type dict')

        cls.parameters.update(parameters)

    def __init__(self):
        """

        """
        self.fodder = 0
        self.herbivores = []
        self.carnivores = []

    def grow_fodder(self):
        """

        :return:
        """
        pass

    def place_animals(self, list_animals):
        """

        :param list_animals:
        :return:
        """
        if not isinstance(list_animals, list):
            raise TypeError('list_animals myst be type list')

        for animal in list_animals:
            self.herbivores.append(animal)

    def remove_animals(self, animal):
        """

        :param animal:
        :return:
        """
        animal_to_remove = self.herbivores
        animal_to_remove.remove(animal)

    def feed_herbivores(self):
        """

        :return:
        """
        np.random.shuffle(self.herbivores)

        for herb in self.herbivores:
            food_available = self.fodder
            food_eaten = herb.eat(food_available)
            self.fodder -= food_eaten

    def feed_carnivores(self):
        """

        :return:
        """
        pass

    def feed_animals(self):
        """
        This method handles the entire feeding cycle for all animals
        :return:
        """
        self.grow_fodder()
        self.feed_herbivores()
        self.feed_carnivores()

    def procreation_herbivores(self):
        """

        :return:
        """
        herb_offspring = []
        num_adult_herbs = len(self.herbivores)

        if num_adult_herbs >= 2:
            for herb in self.herbivores:
                new_offspring = herb.give_birth(num_adult_herbs)
                if new_offspring:
                    child = Herbivore()
                    herb_offspring.append(child)
                    herb.weight_after_birth(child.weight)

        self.herbivores.extend(herb_offspring)

    def aging_animals(self):
        """

        :return:
        """
        for herbs in self.herbivores:
            herbs.update_age()

    def animals_yearly_weight_loss(self):
        """

        :return:
        """
        for herbs in self.herbivores:
            herbs.yearly_weight_loss()

    def animals_die(self):
        """

        :return:
        """
        dead_herbivores = []
        for herb in self.herbivores:
            if herb.death():
                dead_herbivores.append(herb)
        for dead_herb in dead_herbivores:
            self.herbivores.remove(dead_herb)
        return dead_herbivores

    def get_num_animals(self):
        """

        :return:
        """
        return len(self.herbivores)

    def get_remaining_fodder(self):
        """
        Returns the amount of fodder left in a cell.
        :return:
        """
        return self.fodder

    def migration(self):
        """

        :return:
        """
        pass


class Water(Cell):
    """

    """
    def __init__(self):
        """

        """
        pass


class Desert(Cell):
    """

    """
    def __init__(self):
        """

        """
        pass


class Lowland(Cell):
    """

    """
    parameters = {'f_max': 800.0}

    def __init__(self):
        """

        """
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_fodder(self):
        """

        :return:
        """
        self.fodder = self.parameters['f_max']


class Highland(Cell):
    """

    """
    parameters = {'f_max': 300.0}

    def __init__(self):
        """

        """
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_fodder(self):
        """

        :return:
        """
        self.fodder = self.parameters['f_max']


if __name__ == "__main__":
    c = Lowland()
    h1 = Herbivore()
    h2 = Herbivore()
    h3 = Herbivore()
    h4 = Herbivore()
    h5 = Herbivore()
    h6 = Herbivore()
    h7 = Herbivore()
    h8 = Herbivore()
    h_list = [h1, h2, h3, h4, h5, h6, h7, h8]
    c.place_animals(h_list)
    #print(c.get_num_animals())
    #c.animals_die()
    #print(c.get_num_animals())
    # print(c.get_remaining_fodder())
    # c.feed_herbivores()
    # print(c.get_remaining_fodder())
    # print(c.get_num_animals())
    # print(c.get_remaining_fodder())
    for j in range(10):
        for i in range(200):
            c.feed_animals()
            c.procreation_herbivores()
            c.aging_animals()
            c.animals_yearly_weight_loss()
            c.animals_die()
        print(c.get_num_animals())

    print(h1.age)
    print(h1.weight)
