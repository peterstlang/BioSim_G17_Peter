# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'
import numpy as np
from biosim.animals import Animal, Herbivore, Carnivore
import operator
import matplotlib.pyplot as plt
#np.random.seed(1)


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
        for anim in animal:
            if anim.__class__.__name__ == 'Herbivore':
                self.herbivores.remove(anim)
            if anim.__class__.__name__ == 'Carnivore':
                self.carnivores.remove(anim)


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
        self.carnivores.sort(key=operator.attrgetter("fitness"), reverse=True)
        self.herbivores.sort(key=operator.attrgetter("fitness"))

        for carn in self.carnivores:
            dead_herbs = carn.eat_a_herb(self.herbivores)
            surviving_herbs = [herb for herb in self.herbivores if herb not in dead_herbs]
            self.herbivores = surviving_herbs
            self.herbivores.sort(key=operator.attrgetter("fitness"))

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
        for herb in self.herbivores:
            herb.update_age()

        for carn in self.carnivores:
            carn.update_age()

    def animals_yearly_weight_loss(self):
        """

        :return:
        """
        for herb in self.herbivores:
            herb.yearly_weight_loss()

        for carn in self.carnivores:
            carn.yearly_weight_loss()

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

    def migration(self, anim_list):
        """
        This method takes an animal and calculates the probability for it
        to move. If it decides to move it will pick one of the four
        neighbouring cells at random and move

        :return:
        """
        #for anim in anim_list:
        #    if anim.will_move():
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
    # This code was written by Professor Hans
    seeds = range(200, 240)
    years = 250
    mean_counts = np.zeros((len(seeds), 2))
    for sn, seed in enumerate(seeds):
        np.random.seed(seed)
        c = Lowland()
        herbs = list()
        for i in range(50):
            herbs.append(Herbivore(5, 20))
        carns = list()
        for i in range(20):
            carns.append(Carnivore(5, 20))
        c.place_animals(herbs)
        num_animals = np.zeros((years, 2))
        for i in range(years):
            if i == 50:
                c.place_animals(carns)
            c.feed_animals()
            c.procreation_animals()
            c.aging_animals()
            c.animals_yearly_weight_loss()
            c.animals_die()
            num_animals[i, :] = c.get_num_animals()
        mean_counts[sn, :] = num_animals[150:, :].mean(axis=0)
        plt.plot(num_animals)
    mean_counts = mean_counts[mean_counts[:, 0].argsort()]
    print(mean_counts)
    plt.show()
