# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

from biosim.animals import Animal, Herbivore, Carnivore


class TestAnimal:

    def test_constructor(self):
        h = Herbivore()
        c = Carnivore()
        assert isinstance(h, Herbivore)
        assert isinstance(c, Carnivore)

    def test_subclass(self):
        h = Herbivore()
        c = Carnivore()
        assert issubclass(h.__class__, Animal)
        assert issubclass(c.__class__, Animal)

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
