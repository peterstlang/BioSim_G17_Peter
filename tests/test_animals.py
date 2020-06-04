# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

from biosim.animals import Animal, Herbivore


class TestAnimal:

    def test_herbivore_age(self):
        Tim = Herbivore()
        assert Tim.age == 0

    def test_update_age(self):
        carl = Animal()
        carl.update_age()
        assert carl.age == 1
