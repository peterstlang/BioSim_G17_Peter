# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

import numpy as np


class Animal:
    """
    This is the superclass we will be using for all animals and it will contain
    methods that applies to both herbivores and carnivores
    """
    parameters = {}

    @classmethod
    def set_parameters(cls, new_parameters):
        """
        This method allows the user to set the parameters for
        the animals themselves, if they dont want the default ones.
        Only the values can be changed.
        :param new_parameters: dict
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
        :param age:  int
        :param weight: int, float
        """
        # need some more additions but will add at a later point
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
        this function computes q, which will be used when we compute the
        fitness off the animal.
        :param sign: int, float
        is 1/(1.0) or -1/(-1.0)
        :param x: int, float
        :param x_half: int, float
        :param phi: int, float
        :return: q which is used when computing fitness.
        """
        return 1 / (1 + np.exp(sign * phi * (x - x_half)))

    def compute_fitness(self):
        """
        This method computes the animals fitness using q
        and the parameters.
        :return: float
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
        new and updated values of age and weight.
        A lot of things affect the fitness, which is
        why we need this function
        """
        self.fitness = self.compute_fitness()

    def update_age(self):
        """
        This method updates the animals age for every year that passes
        """
        self.age += 1
        self.recalculate_fitness()

    def will_move(self):
        """
        This method calculates the chance of an animal to move to a
        different cell. This method doesn't decide which square.
        :return: bool
        """

        prob_move = self.parameters['mu'] * self.fitness
        random_num = np.random.random()
        return prob_move > random_num

    def weight_at_birth(self):
        """
        If a new animal is born or the age is put at 0,
        this will assign a weight
        :return: int, float
        """
        return np.random.normal(self.parameters['w_birth'],
                                self.parameters['sigma_birth'])

    def eat(self, food_available):
        """
        This method handles how Herbivores eat.
        :param food_available: int, float
        :return: int, float
        """
        if food_available < self.parameters['F']:
            food_eaten = food_available
        else:
            food_eaten = self.parameters['F']
        self.weight += self.parameters['beta'] * food_eaten
        self.recalculate_fitness()
        return food_eaten

    def give_birth(self, num_animals):
        """
        Determines whether or not 2 animals will give birth to offspring.
        :param num_animals: int
        :return: bool
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
        This method deals with how much weight an animal loses each year.
        """
        self.weight -= self.weight * self.parameters['eta']
        self.recalculate_fitness()

    def weight_after_birth(self, weight):
        """
        Recalculates the weight after an animal has given birth
        :param weight: int, float
        """
        self.weight -= self.parameters['xi'] * weight
        self.recalculate_fitness()

    def death(self):
        """
        Decides whether or not an animal will die
        :return: bool
        """
        if self.weight <= 0:
            return True
        else:
            prob_death = self.parameters['omega'] * (1 - self.fitness)
            random_num = np.random.random()
            return prob_death > random_num

    def set_has_migrated(self, boolean):
        """

        :param boolean: bool
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
        Herbivore subclass constructor
        """
        super().__init__(age, weight)


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
        Carnivore subclass constructor
        """
        super().__init__(age, weight)

    def eat_a_herb(self, sorted_herb_list):
        """
        The carnivores eats the herbivores that have been killed
        :param sorted_herb_list: sorted list
        :return: list
        a list of the herbivores
        """
        dead_herbs = []
        eaten_amount = 0
        for herb in sorted_herb_list:
            if self.will_kill_herb(herb):
                eaten_amount += herb.weight
                self.weight += self.parameters['beta'] * herb.weight
                self.recalculate_fitness()
                dead_herbs.append(herb)
            if eaten_amount >= self.parameters['F']:
                break
        return dead_herbs

    def will_kill_herb(self, herb):
        """
        decides whether or not a Carnivore will be able to kill
        a herbivore.
        :param herb: class instance
        :return: bool
        """
        random_num = np.random.random()
        if self.fitness <= herb.fitness:
            return False
        elif 0 < (self.fitness - herb.fitness) < self.parameters['DeltaPhiMax']:
            return ((self.fitness - herb.fitness)
                    / self.parameters['DeltaPhiMax']) > random_num
        else:
            return True
