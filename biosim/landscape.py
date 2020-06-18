# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'
import numpy as np
from biosim.animals import Herbivore, Carnivore
import operator


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
        self.herbivore = []
        self.carnivore = []
        self.habitable_cell = True

    def grow_fodder(self):
        """
        This happens in the subclass so its
        just passed here
        """
        pass

    def add_migrated_animals(self, listofanim):
        """
        This method is used in the migration,
        it takes a list of animals and extend the corresponding list
        :param listofanim: list
        the animals has to be sorted in a list
        """
        if self.habitable_cell:
            herbs = [anim for anim in listofanim if anim.__class__.__name__ == 'Herbivore']
            carns = [anim for anim in listofanim if anim.__class__.__name__ == 'Carnivore']
            self.herbivore.extend(herbs)
            self.carnivore.extend(carns)

    def place_animals(self, list_animals):
        """
        Takes a list of animals and place them in the cell.
        :param list_animals: list
        """
        if not isinstance(list_animals, list):
            raise TypeError('list_animals myst be type list')

        for animal in list_animals:

            age = animal['age']
            weight = animal['weight']
            species = animal['species']

            if species == 'Herbivore':
                self.herbivore.append(Herbivore(age, weight))
            elif species == 'Carnivore':
                self.carnivore.append(Carnivore(age, weight))
            else:
                raise KeyError('must be either herbivore or carnivore')

    def remove_animals(self, animallist):
        """
        This method takes a list of animals and removes
        them from the cell
        :param animallist: list
        """
        for anim_to_remove in animallist:
            if anim_to_remove.__class__.__name__ == 'Herbivore':
                self.herbivore.remove(anim_to_remove)
            if anim_to_remove.__class__.__name__ == 'Carnivore':
                self.carnivore.remove(anim_to_remove)

    def feed_herbivores(self):
        """
        Feeds Herbivores in the cell until their is no fodder, or hungry
        herbivores left
        """
        np.random.shuffle(self.herbivore)

        for herb in self.herbivore:
            food_available = self.fodder
            food_eaten = herb.eat(food_available)
            self.fodder -= food_eaten

    def feed_carnivores(self):
        """
        Feeds Carnivores in the cell until all carnivores have eaten
        or there are no herbivores left. The fittest carnivores eat first and
        they try to kill/eat the herbivores with the lowest fitness
        """
        self.carnivore.sort(key=operator.attrgetter("fitness"), reverse=True)
        self.herbivore.sort(key=operator.attrgetter("fitness"))

        for carn in self.carnivore:
            self.herbivore = carn.eat_a_herb(self.herbivore)

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
        herb_offspring = []
        num_adult_herbs = len(self.herbivore)

        if num_adult_herbs > 1:
            for herb in self.herbivore:
                new_offspring = herb.give_birth(num_adult_herbs)
                if new_offspring:
                    child = Herbivore()
                    herb_offspring.append(child)
                    herb.weight_after_birth(child.weight)

        self.herbivore.extend(herb_offspring)

        carn_offspring = []
        num_adult_carns = len(self.carnivore)

        if num_adult_carns > 1:
            for carn in self.carnivore:
                new_offspring = carn.give_birth(num_adult_carns)
                if new_offspring:
                    child = Carnivore()
                    carn_offspring.append(child)
                    carn.weight_after_birth(child.weight)

        self.carnivore.extend(carn_offspring)

    def aging_animals(self):
        """
        ages the animals in a cell
        """
        for herb in self.herbivore:
            herb.update_age()

        for carn in self.carnivore:
            carn.update_age()

    def animals_yearly_weight_loss(self):
        """
        Updates the weight of the animals in a cell
        """
        for herb in self.herbivore:
            herb.yearly_weight_loss()

        for carn in self.carnivore:
            carn.yearly_weight_loss()

    def animals_die(self):
        """
        Checks if any of the animals die or not.
        If an animal dies it is removed from the respective list.
        :return:
        """
        dead_herbivores = []
        for herb in self.herbivore:
            if herb.death():
                dead_herbivores.append(herb)
        for dead_herb in dead_herbivores:
            self.herbivore.remove(dead_herb)

        dead_carnivores = []
        for carn in self.carnivore:
            if carn.death():
                dead_carnivores.append(carn)
        for dead_carn in dead_carnivores:
            self.carnivore.remove(dead_carn)

    def get_remaining_fodder(self):
        """
        Returns the amount of fodder left in a cell.
        :return: int
        The amount of fodder is given as an int
        """
        return self.fodder

    def migration(self, adj_cells):
        """
        An empty dictionary is created and a list of all the animals are
        created
        :param adj_cells: 4 tuples
        :return: dict
        The empty dictionary is returned with each of the
        adjacent cells as keys and the animals in each cell as values
        the values are in list form
        """

        anims_that_migrate = {}
        anim_list = self.carnivore + self.herbivore
        for anim in anim_list:
            if anim.will_move() and not anim.animals_has_migrated:
                destination_cell = np.random.choice(adj_cells)
                if destination_cell in anims_that_migrate.keys():
                    anims_that_migrate[destination_cell].append(anim)
                else:
                    anims_that_migrate[destination_cell] = [anim]

        for anim in anim_list:
            anim.set_has_migrated(True)

        return anims_that_migrate


class Water(Cell):
    """
    Water subclass
    """

    def __init__(self):
        """
        constructor for the water subclass
        """
        super().__init__()
        self.habitable_cell = False


class Desert(Cell):
    """
    Desert subclass
    """

    def __init__(self):
        """
        constructor for the desert subclass
        """
        super().__init__()


class Lowland(Cell):
    """
    Lowland subclass
    """
    parameters = {'f_max': 800.0}

    def __init__(self):
        """
        constructor for the lowland subclass
        We set the parameters since fodder can grow here
        """
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_fodder(self):
        """
        Sets the amount of fodder equal to the parameter
        its 800 by default but can be changed
        """
        self.fodder = self.parameters['f_max']


class Highland(Cell):
    """
    Highland subclass
    """
    parameters = {'f_max': 300.0}

    def __init__(self):
        """
        constructor for the highland subclass
        We set the parameters since fodder can grow here
        """
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_fodder(self):
        """
        Sets the amount of fodder equal to the parameter
        its 300 by default but can be changed
        """
        self.fodder = self.parameters['f_max']
