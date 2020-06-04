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

    def __init__(self, age=0, weight=None):
        """
        Animal class constructor.
        :param age: int
        :param weight: int or float
        """
        self.age = age

    @staticmethod
    def compute_q(oneplusmin, x, x_half, phi):
        return 1 / (1 + np.exp(oneplusmin * phi * (x - x_half)))

    @classmethod
    def compute_fitness(cls, age, weight, p):
        fitness = cls.compute_q(+1, age, p['a_half'], p['phi_age']) * \
                  cls.compute_q(-1, weight, p['w_half'], p['phi_weight'])
        return fitness


class Herbivore(Animal):
    """
    Herbivore subclass
    """

    def __init__(self, age=0, weight=None):
        """
        Herbivore subclass constructor
        """
        super().__init__(age, weight)

    parameters = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05,
                  'a_half': 40.0, 'phi_age': 0.6, 'w_half': 10.0, 'phi_weight':
                      0.1, 'mu': 0.25, 'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                  'omega': 0.4, 'F': 10.0}


class Carnivore(Animal):
    """
    Carnivore subclass
    """
    def __init__(self, age=0, weight=None):
        """
        Carnivore subclass constructor
        """
        super().__init__(age, weight)

    parameters = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
                  'eta': 0.125, 'a_half': 40.0, 'phi_age': 0.3, 'w_half':
                  4.0, 'phi_weight': 0.4, 'mu': 0.4, 'gamma': 0.8, 'zeta':
                  3.5, 'xi': 1.1, 'omega': 0.8, 'F': 50.0, 'DeltaPhiMax':
                  10.0}
