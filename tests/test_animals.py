# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

from biosim.animals import Animal, Herbivore


class TestAnimal:

    def test_herbivore_age(self):
        h = Herbivore()
        assert h.age == 0

    def test_update_age(self):
        h = Herbivore()
        h.update_age()
        assert h.age == 1

    def test_birth_weight(self):
        h = Herbivore()
        assert h.weight >= 0

    def test_yearly_weight_loss(self):
        h = Herbivore(age=1, weight=7)
        h.yearly_weight_loss()
        assert h.weight < 7
