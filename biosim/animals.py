# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

import numpy as np


class Animal:

    """
    This is documentation for the Animal class
    """

    parameters = {}

    @classmethod
    def set_parameters(cls, new_parameters):
        """
        This method allows the user to set the parameters for
        the animals themselves, if they dont want the default ones.
        Only the values can be changed.

        :param new_parameters: dict
        The dictionary shall have the parameters as keys and the
        values should be ints or floats, this is ensured by raising
        errors if anything is wrong.
        """

        if not isinstance(new_parameters, dict):
            raise TypeError('Parameters must be of type dict')

        # Heavily inspired by the biolab project
        for key in new_parameters:
            if key not in cls.parameters:
                raise KeyError('Invalid parameter name: ' + key)

        cls.parameters.update(new_parameters)

    def __init__(self, age=0, weight=None):
        """
        Constructor for the Animal superclass

        :param age: Has to be a positive int

        :param weight: can be of either int or float, but has to be positive
        """

        if not isinstance(age, int):
            raise TypeError('age must be of type int')

        if age < 0:
            raise ValueError('age must be a positive integer')

        if weight is not None:
            if not isinstance(weight, (float, int)):
                raise TypeError('weight must be of type float or int')
            if weight < 0:
                raise ValueError('weight must be a positive number')

        self.age = age
        if weight is None:
            self.weight = self.weight_at_birth()
        else:
            self.weight = weight
        self.fitness = self.compute_fitness()

        self.animals_has_migrated = False

    @staticmethod
    def compute_q(sign, x, x_half, phi):
        """
        q is computed, and will be used when fitness is computed

        :param sign: int, float
        is 1/(1.0) or -1/(-1.0)

        :param x: int, float

        :param x_half: int, float

        :param phi: int, float

        :return: q, which is used when computing fitness.
        """

        return 1 / (1 + np.exp(sign * phi * (x - x_half)))

    def compute_fitness(self):
        """
        The fitness is calculated, we use q and the animals parameters
        to determine the fitness of the animal

        :return: the fitness is of type float
        """

        if self.weight == 0:
            self.fitness = 0
        else:
            p = self.parameters
            fit = self.compute_q(+1, self.age, p['a_half'], p['phi_age']) * \
                self.compute_q(-1, self.weight, p['w_half'], p['phi_weight'])
            return fit

    def recalculate_fitness(self):
        """
        recalculates and updates fitness based on
        new and updated values of age, weight and the parameters.
        Most of the processes animals go through will affect its fitness
        which is why we need to recalculate it on several occasions
        """

        self.fitness = self.compute_fitness()

    def update_age(self):
        """
        For each year that passes the animals will age 1 year
        """

        self.age += 1
        self.recalculate_fitness()

    def will_move(self):
        """
        This method doesn't actually make the animals migrate,
        it only decide whether or not it will actually move and is called
        upon later

        :return: bool
        If its False the animals simply stay in the cell, if its True
        The animals will migrate to one of four adjacent cells
        """

        prob_move = self.parameters['mu'] * self.fitness
        random_num = np.random.random()
        # return True
        return prob_move > random_num

    def weight_at_birth(self):
        """
        If a new animal is born or the age is put at 0
        (aka the animal placed is a newborn),
        We will assign a weight from a normal distribution.
        """
        return np.random.normal(self.parameters['w_birth'],
                                self.parameters['sigma_birth'])

    def give_birth(self, num_animals):
        """
        Here we calculate the probability for an animal to give birth.
        We also check a weight condition.

        :param num_animals: How many animals there are, type int
        if there are less than 2 no animals will be born, but that
        condition is checked in landscape

        :return: bool
        If its False no animal is born, if its True an animal is born
        each animal can only give birth once per year.
        """

        p = self.parameters
        random_num = np.random.random()
        prob_birth = np.min([1, p['gamma'] * self.fitness * (num_animals - 1)])
        if self.weight < p['zeta'] * (p['w_birth'] + p['sigma_birth']):
            return False
        else:
            return random_num < prob_birth

    def yearly_weight_loss(self):
        """
        The animals will lose an amount of weight each year
        based on certain parameters. The fitness is recalculated after
        """

        self.weight -= self.weight * self.parameters['eta']
        self.recalculate_fitness()

    def weight_after_birth(self, weight):
        """
        After an animal has given birth, the weight is updated
        and the fitness recalculated

        :param weight: int, float
        """

        self.weight -= self.parameters['xi'] * weight
        self.recalculate_fitness()

    def death(self):
        """
        The animals will die if their weight is 0 or less
        (although it shouldn't be less than 0). If it has a positive weight
        the probability of death is calculated by certain parameters

        :return: bool
        True means the animal dies, False means it lives
        """

        if self.weight <= 0:
            return True
        else:
            prob_death = self.parameters['omega'] * (1 - self.fitness)
            random_num = np.random.random()
            return prob_death > random_num

    def set_has_migrated(self, boolean):
        """
        This method is used later in the program. When animals migrate we need
        to make sure that they only migrate once. This function is called upon
        and set either True or False, depending on whether they have migrated
        or not

        :param boolean: bool
        This is set to False before the animal migrates, and will be updated
        to True as soon as it has migrated
        """

        self.animals_has_migrated = boolean


class Herbivore(Animal):
    """
    Herbivore subclass
    """

    parameters = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05,
                  'a_half': 40.0, 'phi_age': 0.6, 'w_half': 10.0, 'phi_weight':
                      0.1, 'mu': 0.25, 'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                  'omega': 0.4, 'F': 10.0}

    def __init__(self, age=0, weight=None):
        """
        subclass constructor, inherits from the superclass
        """

        super().__init__(age, weight)

    def eat(self, food_available):
        """
        This method will make the Herbivore eats. It makes sure that
        if the fodder left is less than its appetite, it only eats the
        remaining fodder. If not it eats until it's full. It also recalculates
        the fitness when its done eating

        :param food_available: int, float
        the amount of fodder

        :return: int, float
        How much the animal has eaten
        """

        if food_available < self.parameters['F']:
            food_eaten = food_available
        else:
            food_eaten = self.parameters['F']
        self.weight += self.parameters['beta'] * food_eaten
        self.recalculate_fitness()
        return food_eaten


class Carnivore(Animal):
    """
    Carnivore subclass
    """

    parameters = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
                  'eta': 0.125, 'a_half': 40.0, 'phi_age': 0.3, 'w_half':
                      4.0, 'phi_weight': 0.4, 'mu': 0.4, 'gamma': 0.8, 'zeta':
                      3.5, 'xi': 1.1, 'omega': 0.8, 'F': 50.0, 'DeltaPhiMax':
                      10.0}

    def __init__(self, age=0, weight=None):
        """
        subclass constructor, inherits from the Superclass
        """

        super().__init__(age, weight)

    def will_kill_herb(self, herb):
        """
        checks several conditions to see if a Carnivore
        can/and or will kill a herbivore. This is called upon
        when the carnivore starts to eat.

        :param herb: An instance of Herbivore

        :return: bool
        The kill is successful if it returns True.
        """

        random_num = np.random.random()
        if self.fitness <= herb.fitness:
            return False
        elif 0 < (self.fitness - herb.fitness) < self.parameters['DeltaPhiMax']:
            return ((self.fitness - herb.fitness)
                    / self.parameters['DeltaPhiMax']) > random_num
        else:
            return True

    def eat_a_herb(self, sorted_herb_list):
        """
        The carnivores checks if it kills a herbivore.
        If it doess kill, it will eat the herbivore until there is
        nothing left, or the Carnivore is full

        :param sorted_herb_list: sorted list
        It gets a list of herbivores that is sorted by fitness,
        from lowest to highest. The ones with lowest gets killed and eaten
        first

        :return: list
        a list of surviving herbivores
        """

        dead_herbs = []
        surv_herbs = []
        eaten_amount = 0
        for herb in sorted_herb_list:
            if self.will_kill_herb(herb):
                eats = min(herb.weight, self.parameters['F'] - eaten_amount)
                eaten_amount += eats
                self.weight += self.parameters['beta'] * eats
                self.recalculate_fitness()
                dead_herbs.append(herb)
            else:
                surv_herbs.append(herb)

            if eaten_amount >= self.parameters['F']:
                break
        return surv_herbs
