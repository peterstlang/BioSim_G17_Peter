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
    def set_parameters(cls, parameters):
        cls.parameters.update(parameters)
        # Check if its a dict
        # Check if the parameters are legal

    def __init__(self, age=0, weight=None):
        """
        Constructor for the Animal superclass
        :param age:
        :param weight:
        """
        # need some more additions but will add at a later point
        self.age = age
        if weight is None:
            self.weight = self.weight_at_birth()
        else:
            self.weight = weight
        self.fitness = self.compute_fitness()


    @staticmethod
    def compute_q(sign, x, x_half, phi):
        """
        this function computes q, which will be used when we compute the
        fitness off the animal.
        :param sign:
        :param x:
        :param x_half:
        :param phi:
        :return:
        """
        return 1 / (1 + np.exp(sign * phi * (x - x_half)))

    def compute_fitness(self):
        """
        This method uses q to compute the fitness of an animal
        :param age:
        :param weight:
        :param p:
        :return:
        """
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
        :return:
        """
        self.fitness = self.compute_fitness(self.age, self.weight,
                                            self.parameters)

    def update_age(self):
        """
        This method updates the animals age for every year that passes
        :return: updated year
        """
        self.age += 1

    def will_move(self):
        """
        This method calculates the chance of an animal to move to a
        different cell. This method doesn't decide which square.
        :return:
        """

        prob_mig = self.parameters['mu'] * self.fitness
        random_num = np.random.random()
        return prob_mig > random_num

    def weight_at_birth(self):
        return np.random.normal(self.parameters['w_birth'],
                                self.parameters['sigma_birth'])

    def eat(self, food_available):
        """

        :param food_available:
        :return:
        """
        if food_available < self.parameters['F']:
            food_eaten = food_available
        else:
            food_eaten = self.parameters['F']
        self.weight += self.parameters['beta'] * food_eaten
        self.recalculate_fitness()
        return food_eaten

    def give_birth(self, num_animals):
        if num_animals < 2:
            return False
        p = self.parameters
        rand_num = np.random.random()
        prob_birth = np.min(1, p['gamma'] * self.fitness * (num_animals - 1))
        if self.weight < p['zeta'] * (['w_birth'] + ['sigma_birth']):
            return False
        else:
            return rand_num < prob_birth

    def weight_loss_per_year(self):
        """
        This method deals with how much weight an animal loses each year.
        :return:
        """
        self.weight -= self.weight * self.parameters['eta']
        self.recalculate_fitness()

    def weight_after_birth(self, weight):
        """

        :param weight:
        :return:
        """
        self.weight -= self.parameters['xi'] * weight
        self.recalculate_fitness()

    def death(self):
        """

        :return:
        """
        if self.weight <= 0:
            return True
        else:
            prob_death = self.parameters['omega'] * (1 - self.fitness)
            random_num = np.random.random()
            return prob_death > random_num


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


if __name__ == "__main__":
    h = Herbivore(age=1, weight=7)
    print(h.fitness)
    print(h.age)
    print(h.weight)
