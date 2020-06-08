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
        cls.parameters.update(parameters)

    def __init__(self):
        self.fodder = 0
        self.herbivores = []

    def grow_fodder(self):
        pass

    def randomise_herb_list(self):
        our_list = self.herbivores
        np.random.shuffle(our_list)
        return our_list

    def place_animals(self, list_animals):
        if not isinstance(list_animals, list):
            raise TypeError('list_animals myst be type list')

        for animal in list_animals:
            self.herbivores.append(animal)

    def remove_animals(self, animal):
        animal_to_remove = self.herbivores
        animal_to_remove.remove(animal)

    def feed_herbivores(self):
        random_herb_list = self.randomise_herb_list()

        for herb in random_herb_list:
            food_available = self.fodder
            food_eaten = herb.eat(food_available)
            self.fodder -= food_eaten

    def feed_carnivores(self):
        pass

    def feed_animals(self):
        self.grow_fodder()
        self.feed_herbivores()
        self.feed_carnivores()

    def procreation_herbivores(self):
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
        for herbs in self.herbivores:
            herbs.update_age()

    def animals_yearly_weight_loss(self):
        for herbs in self.herbivores:
            herbs.yearly_weight_loss()

    def animals_die(self):
        dead_herbivores = []
        for herb in self.herbivores:
            if herb.death():
                dead_herbivores.append(herb)
        for dead_herb in dead_herbivores:
            self.herbivores.remove(dead_herb)
        return dead_herbivores

    def get_num_animals(self):
        return len(self.herbivores)

    def get_remaining_fodder(self):
        return self.fodder

    def migration(self):
        pass


class Water(Cell):
    def __init__(self):
        pass


class Desert(Cell):
    def __init__(self):
        pass


class Lowland(Cell):
    parameters = {'f_max': 800.0}

    def __init__(self):
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_fodder(self):
        self.fodder = self.parameters['f_max']


class Highland(Cell):
    parameters = {'f_max': 300.0}

    def __init__(self):
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_fodder(self):
        self.fodder = self.parameters['f_max']


if __name__ == "__main__":
    #c = Lowland()
    #h1 = Herbivore()
    #h2 = Herbivore()
    #h3 = Herbivore()
    #h4 = Herbivore()
    #h5 = Herbivore()
    #h_list = [h1, h2, h3, h4, h5]
    #c.place_animals(h_list)
    #print(c.get_num_animals())
    #print(c.get_remaining_fodder())
    #for i in range(50):
    #    c.feed_animals()
    #    c.procreation_herbivores()
    #    c.aging_animals()
    #    c.animals_yearly_weight_loss()
    #    c.animals_die()

    #print(c.get_num_animals())
    #print(c.get_remaining_fodder())


    # print(h1.age)
