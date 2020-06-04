# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

from biosim.animals import Animal, Herbivore


class TestAnimal:

    def test_herbivore_age(self):
        tim = Herbivore()
        assert tim.age == 0

    def test_update_age(self):
        carl = Herbivore()
        carl.update_age()
        assert carl.age == 1

    def test_birth_weight(self):
        john = Herbivore()
        assert john.weight >= 0



