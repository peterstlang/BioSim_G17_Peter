# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'
import numpy as np
from biosim.animals import Animal, Herbivore, Carnivore
import operator
import matplotlib.pyplot as plt


# np.random.seed(1)


class Cell:
    """
    Cell superclass.
    This is where animals will reside and the yearly cycle will occur
    """
    parameters = {}

    @classmethod
    def set_parameters(cls, parameters):
        """
        Allows the user to set their own parameters
        :param parameters: dict
        """

        if not isinstance(parameters, dict):
            raise TypeError('parameters must be of type dict')

        cls.parameters.update(parameters)

    def __init__(self):
        """
        constructor for Cell superclass.
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
        Takes a list of animals and place them in the cell.
        :param list_animals: list
        """
        if not isinstance(list_animals, list):
            raise TypeError('list_animals myst be type list')

        for animal in list_animals:
            if animal.__class__.__name__ == 'Herbivore':
                self.herbivores.append(animal)
            if animal.__class__.__name__ == 'Carnivore':
                self.carnivores.append(animal)

    def remove_animals(self, animallist):
        """

        :param animal: class instance
        :return:
        """
        for anim in animallist:
            if anim.__class__.__name__ == 'Herbivore':
                self.herbivores.remove(anim)
            if anim.__class__.__name__ == 'Carnivore':
                self.carnivores.remove(anim)

    def feed_herbivores(self):
        """
        Feeds Herbivores in the cell until their is no fodder, or hungry
        herbivores left
        """
        np.random.shuffle(self.herbivores)

        for herb in self.herbivores:
            food_available = self.fodder
            food_eaten = herb.eat(food_available)
            self.fodder -= food_eaten

    def feed_carnivores(self):
        """
        Feeds Carnivores in the cell until all carnivores have eaten
        or there are no herbivores left. The fittest carnivores eat first and
        they try to kill/eat the herbivores with the lowest fitness
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
        This method will mate the animals and add the offspring
        to the list of animals
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
        ages the animals in a cell
        """
        for herb in self.herbivores:
            herb.update_age()

        for carn in self.carnivores:
            carn.update_age()

    def animals_yearly_weight_loss(self):
        """
        Updates the weight of the animals in a cell
        """
        for herb in self.herbivores:
            herb.yearly_weight_loss()

        for carn in self.carnivores:
            carn.yearly_weight_loss()

    def animals_die(self):
        """
        Checks if any of the animals die or not.
        If an animal dies it is removed from the respective list.
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
        Gives the user a tuple. The left most values are the amount
        of herbivores in a cell and the rightmost is carnivores.
        :return: tuple
        """
        return len(self.herbivores), len(self.carnivores)

    def get_remaining_fodder(self):
        """
        Returns the amount of fodder left in a cell.
        :return:
        """
        return self.fodder

    def migration(self, adj_cells):
        """
        This method takes an animal and calculates the probability for it
        to move. If it decides to move it will pick one of the four
        neighbouring cells at random and move

        :return:
        """

        anims_that_migrate = {}
        anim_list = self.carnivores + self.herbivores
        for anim in anim_list:
            if anim.will_move() and not anim.animals_has_migrated:
                destination_cell = np.random.choice(adj_cells)
                print(destination_cell)
                if destination_cell in anims_that_migrate.keys():
                    anims_that_migrate[destination_cell].append(anim)
                else:
                    anims_that_migrate[destination_cell] = [anim]

        for anim in anim_list:
            anim.set_has_migrated(True)
            # Do this using a fucntion in animal class

        return anims_that_migrate


class Water(Cell):
    """
    Water subclass
    """

    habitable_cell = False

    def __init__(self):
        """

        """
        super().__init__()


class Desert(Cell):
    """
    Desert subclass
    """

    habitable_cell = True

    def __init__(self):
        """

        """
        super().__init__()


class Lowland(Cell):
    """
    Lowland subclass
    """
    habitable_cell = True
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
    habitable_cell = True
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

# if __name__ == "__main__":
# This code was written by Professor Hans
#    seeds = range(200, 240)
#    years = 250
#    mean_counts = np.zeros((len(seeds), 2))
#    for sn, seed in enumerate(seeds):
#        np.random.seed(seed)
#        c = Lowland()
#        herbs = list()
#        for i in range(50):
#            herbs.append(Herbivore(5, 20))
#        carns = list()
#        for i in range(20):
#            carns.append(Carnivore(5, 20))
#        c.place_animals(herbs)
#        num_animals = np.zeros((years, 2))
#        for i in range(years):
#            if i == 50:
#                c.place_animals(carns)
#            c.feed_animals()
#            c.procreation_animals()
#            c.aging_animals()
#            c.animals_yearly_weight_loss()
#            c.animals_die()
#            num_animals[i, :] = c.get_num_animals()
#        mean_counts[sn, :] = num_animals[150:, :].mean(axis=0)
#        plt.plot(num_animals)
#    mean_counts = mean_counts[mean_counts[:, 0].argsort()]
#    print(mean_counts)
#    plt.show()
