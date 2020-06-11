# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'
import numpy as np

np.random.seed(1)
from biosim.animals import Animal, Herbivore, Carnivore
import operator
import matplotlib.pyplot as plt


class Cell:
    """
    Cell superclass.
    This is where animals will reside and the yearly cycle will occur
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
            if animal.__class__.__name__ == 'Herbivore':
                self.herbivores.append(animal)
            if animal.__class__.__name__ == 'Carnivore':
                self.carnivores.append(animal)

    def remove_animals(self, animal):
        """

        :param animal:
        :return:
        """
        pass

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
        sorted(self.carnivores, key=operator.attrgetter("fitness"), reverse=True)
        sorted(self.herbivores, key=operator.attrgetter("fitness"))

        for carn in self.carnivores:
            dead_herbs = carn.eat_a_herb(self.herbivores)
            surviving_herbs = [herb for herb in self.herbivores if herb not in dead_herbs]
            self.herbivores = surviving_herbs
            sorted(self.herbivores, key=operator.attrgetter("fitness"))

            # Finne en annen måte å oppdatere self.herbivores

    def feed_animals(self):
        """
        This method handles the entire feeding cycle for all animals
        :return:
        """
        self.grow_fodder()
        self.feed_herbivores()
        self.feed_carnivores()

    def procreation_animals(self):
        """

        :return:
        """
        # ønsker å bruke denne metoden for begge arter.
        # Må finne en god løsning for dette.
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

        carn_offspring = []
        num_adult_carns = len(self.carnivores)

        if num_adult_carns >= 2:
            for carn in self.carnivores:
                new_offspring = carn.give_birth(num_adult_carns)
                if new_offspring:
                    child = Carnivore()
                    carn_offspring.append(child)
                    carn.weight_after_birth(child.weight)

        self.carnivores.extend(carn_offspring)

    def aging_animals(self):
        """

        :return:
        """
        for herbs in self.herbivores:
            herbs.update_age()

        for carns in self.carnivores:
            carns.update_age()

    def animals_yearly_weight_loss(self):
        """

        :return:
        """
        for herbs in self.herbivores:
            herbs.yearly_weight_loss()

        for carns in self.carnivores:
            carns.yearly_weight_loss()

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

        dead_carnivores = []
        for carn in self.carnivores:
            if carn.death():
                dead_carnivores.append(carn)
        for dead_carn in dead_carnivores:
            self.carnivores.remove(dead_carn)

    def get_num_animals(self):
        """

        :return:
        """
        return len(self.herbivores), len(self.carnivores)

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
    Water subclass
    """

    def __init__(self):
        """

        """
        super().__init__()


class Desert(Cell):
    """
    Desert subclass
    """

    def __init__(self):
        """

        """
        super().__init__()


class Lowland(Cell):
    """
    Lowland subclass
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
    Highland subclass
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
    herbs = list()
    for i in range(50):
        herbs.append(Herbivore(5, 20))

    carns = list()
    for i in range(20):
        carns.append(Carnivore(5, 20))

    c.place_animals(herbs)
    # print(c.get_num_animals())
    # c.animals_die()
    # print(c.get_num_animals())
    # print(c.get_remaining_fodder())
    # c.feed_herbivores()
    # print(c.get_remaining_fodder())
    # print(c.get_num_animals())
    # print(c.get_remaining_fodder())
    num_animals = []

    for i in range(250):
        if i == 50:
            c.place_animals(carns)
        c.feed_animals()
        c.procreation_animals()
        c.aging_animals()
        c.animals_yearly_weight_loss()
        c.animals_die()

        num_animals.append(c.get_num_animals())
        print('herbivores, carnivores: ', c.get_num_animals())
# plt.plot(num_animals)

# plt.show()
# print(h1.weight)

# print(h1.age)
# print(h1.weight)
